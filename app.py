# app.py
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, filedialog
import sys
import pandas as pd
from ner_model import ArabicNER

ENTITY_COLORS = {
    'PER': 'light blue',
    'LOC': 'light green',
    'ORG': 'orange',
    'MISC': 'light yellow'
}

# =================================================================
# كلاس يحول مربع النص إلى شاشة CMD
# =================================================================
class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str_val):
        # نطلب من الواجهة تحديث النص (Thread-Safe)
        self.widget.after(0, self._write, str_val)

    def _write(self, str_val):
        try:
            self.widget.configure(state='normal')
            
            # معالجة خاصة لـ tqdm (شريط التحميل)
            # إذا كان النص يبدأ بـ \r فهذا يعني تحديث نفس السطر
            if '\r' in str_val:
                # نحذف السطر الأخير لنكتب مكانه
                # (هذا يجعل الشريط يتحرك مكانه ولا يملأ الشاشة)
                last_line_index = self.widget.index("end-1c linestart")
                self.widget.delete(last_line_index, "end-1c")
            
            self.widget.insert('end', str_val, self.tag)
            self.widget.see('end') # التمرير التلقائي للأسفل
            self.widget.configure(state='disabled')
        except:
            pass

    def flush(self):
        pass

# =================================================================
# التطبيق الرئيسي
# =================================================================
class NERApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arabic NER - Professional Platform")
        self.root.geometry("1100x750")

        try:
            self.ner = ArabicNER()
        except Exception as e:
            messagebox.showerror("خطأ حرج", f"فشل تهيئة البرنامج: {e}")
            return

        # ================= الجزء العلوي =================
        top_container = tk.Frame(root)
        top_container.pack(fill='x', padx=10, pady=5)

        tk.Label(top_container, text="النص المراد تحليله:", font=("Arial", 10, "bold")).pack(anchor='w')
        self.text_input = scrolledtext.ScrolledText(top_container, height=4, font=("Arial", 11))
        self.text_input.pack(fill='x', pady=5)
        self.text_input.insert("1.0", "أعلنت شركة أرامكو السعودية عن شراكة جديدة مع جوجل كلاود لإنشاء مركز بيانات في الدمام.")

        # شريط التحكم
        controls_frame = tk.Frame(top_container)
        controls_frame.pack(fill='x', pady=5)

        tk.Label(controls_frame, text="اختر النموذج:").pack(side='left')
        
        self.model_var = tk.StringVar(root)
        self.model_names = list(self.ner.models.keys())
        self.model_var.set(self.model_names[0])
        
        self.model_dropdown = tk.OptionMenu(controls_frame, self.model_var, *self.model_names, command=self.change_model)
        self.model_dropdown.pack(side='left', padx=10)

        # زر إضافة نموذج جديد
        tk.Button(controls_frame, text="➕ إضافة نموذج جديد", command=self.add_new_model_ui,
                  bg='#9C27B0', fg='white', font=("Arial", 9, "bold")).pack(side='left', padx=5)

        # زر التشغيل
        tk.Button(controls_frame, text="تشغيل (+)", command=self.run_and_add_column, 
                  bg='#4CAF50', fg='white', font=("Arial", 10, "bold")).pack(side='left', padx=10)

        # زر حفظ Excel
        tk.Button(controls_frame, text="📊 حفظ Excel", command=self.save_excel_with_chart,
                  bg='#2196F3', fg='white', font=("Arial", 10, "bold")).pack(side='left', padx=10)

        # زر مسح
        tk.Button(controls_frame, text="مسح", command=self.clear_columns,
                  bg='#f44336', fg='white').pack(side='right', padx=5)

        tk.Label(root, text="--- منطقة المقارنة ---", fg="gray").pack()

        # ================= الجزء السفلي =================
        self.canvas_container = tk.Frame(root)
        self.canvas_container.pack(fill='both', expand=True, padx=10, pady=5)
        self.canvas = tk.Canvas(self.canvas_container, bg="#f0f0f0")
        self.scrollbar = tk.Scrollbar(self.canvas_container, orient="horizontal", command=self.canvas.xview)
        self.columns_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.columns_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.columns_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.scrollable_window, height=e.height))

        self.all_results = []

    def change_model(self, selection):
        self.ner.set_model(selection)

    # =================================================================
    # نافذة "شاشة التحميل السوداء"
    # =================================================================
    def add_new_model_ui(self):
        hf_link = simpledialog.askstring("إضافة نموذج", "أدخل رابط النموذج (مثال: marefa-nlp/marefa-ner):")
        if not hf_link: return

        display_name = simpledialog.askstring("تسمية النموذج", "أدخل اسماً مختصراً للنموذج:")
        if not display_name: display_name = hf_link

        # 1. إنشاء نافذة منبثقة
        popup = tk.Toplevel(self.root)
        popup.title("Terminal Output")
        popup.geometry("600x400")
        
        # 2. تصميم النافذة لتشبه CMD (خلفية سوداء، نص أخضر)
        tk.Label(popup, text=f"جاري تنفيذ الأمر: Download {display_name}...", font=("Consolas", 10, "bold")).pack(anchor='w', padx=5, pady=5)
        
        console_text = scrolledtext.ScrolledText(popup, bg="black", fg="#00ff00", font=("Consolas", 10), state='disabled')
        console_text.pack(fill='both', expand=True, padx=5, pady=5)

        # 3. تحضير "الجواسيس" لنقل الكلام من النظام إلى النافذة
        # سنعيد توجيه stdout (للطباعة العادية) و stderr (لأشرطة التحميل والأخطاء)
        sys.stdout = TextRedirector(console_text, "stdout")
        sys.stderr = TextRedirector(console_text, "stderr")

        def download_task():
            print(f">>> Starting download process for: {hf_link}")
            print(">>> Please wait while HuggingFace downloads the files...")
            print("-----------------------------------------------------")
            
            try:
                # عملية التحميل الحقيقية
                self.ner.add_custom_model(hf_link, display_name)
                
                print("\n-----------------------------------------------------")
                print(">>> ✅ SUCCESS: Model downloaded and loaded!")
                print(">>> You can close this window now.")
                
                # عند النجاح
                self.root.after(0, lambda: self.on_download_success(display_name, popup))
                
            except Exception as e:
                print("\n>>> ❌ ERROR: Download failed!")
                print(f">>> Details: {e}")
                # لن نغلق النافذة فوراً لكي يقرأ المستخدم الخطأ
            finally:
                # (مهم جداً) إعادة قنوات الاتصال لوضعها الطبيعي
                # لكن في هذا التصميم، يمكننا تركها موجهة للنافذة حتى يتم إغلاقها
                # أو إعادتها هنا. للأمان سنعيدها عند إغلاق النافذة.
                pass

        # تشغيل الخيط
        t = threading.Thread(target=download_task, daemon=True)
        t.start()

        # عند إغلاق النافذة، نعيد النظام لطبيعته
        def on_close():
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            popup.destroy()
            
        popup.protocol("WM_DELETE_WINDOW", on_close)

    def on_download_success(self, display_name, popup):
        self.refresh_dropdown(display_name)
        messagebox.showinfo("نجاح", f"تم إضافة النموذج {display_name} للقائمة!")
        # نعيد النظام لطبيعته ونغلق النافذة
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        popup.destroy()

    def refresh_dropdown(self, new_selection):
        menu = self.model_dropdown["menu"]
        menu.delete(0, "end")
        self.model_names = list(self.ner.models.keys())
        for name in self.model_names:
            menu.add_command(label=name, command=tk._setit(self.model_var, name, self.change_model))
        self.model_var.set(new_selection)
        self.ner.set_model(new_selection)

    # ... (باقي الكود كما هو) ...
    def run_and_add_column(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text: return
        model_name = self.model_var.get()
        try:
            start = time.time()
            token_labels, entities = self.ner.extract_entities(text)
            elapsed = time.time() - start
            self.create_result_column(model_name, elapsed, token_labels, entities)
            self.all_results.append({"model": model_name, "time": elapsed, "entities": entities, "count": len(entities)})
            self.root.update_idletasks()
            self.canvas.xview_moveto(1.0)
        except Exception as e: messagebox.showerror("Error", str(e))

    def create_result_column(self, model_name, elapsed_time, token_labels, entities):
        col_frame = tk.Frame(self.columns_frame, bg="white", bd=2, relief="groove", width=250)
        col_frame.pack(side="left", fill="y", padx=5, pady=5)
        header_text = f"{model_name}\n⏱ {elapsed_time:.4f}s\n({len(entities)} Entities)"
        tk.Label(col_frame, text=header_text, bg="#e0e0e0", font=("Arial", 9, "bold"), pady=5).pack(fill="x")
        result_text = scrolledtext.ScrolledText(col_frame, width=30, height=20, font=("Arial", 10))
        result_text.pack(fill="both", expand=True, padx=2, pady=2)
        for tag, color in ENTITY_COLORS.items(): result_text.tag_config(tag, background=color)
        for tok, lab in token_labels:
            result_text.insert(tk.END, f"{tok}  [{lab}]\n")
            if lab != 'O':
                tag = lab.split('-')[1]
                if tag in ENTITY_COLORS: result_text.tag_add(tag, "end-2c linestart", "end-2c lineend")
        result_text.config(state=tk.DISABLED)

    def save_excel_with_chart(self):
        if not self.all_results: return
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if not path: return
        try:
            max_len = max(len(res['entities']) for res in self.all_results)
            data_detailed = {}
            for res in self.all_results:
                name = res['model']
                ents = [e['text'] for e in res['entities']] + ['']*(max_len-len(res['entities']))
                types = [e['type'] for e in res['entities']] + ['']*(max_len-len(res['entities']))
                data_detailed[f"{name} ({res['time']:.2f}s) - Text"] = ents
                data_detailed[f"{name} - Type"] = types
            df_detailed = pd.DataFrame(data_detailed)
            df_summary = pd.DataFrame({'Model': [r['model'] for r in self.all_results], 'Count': [r['count'] for r in self.all_results], 'Time': [r['time'] for r in self.all_results]})
            with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
                df_detailed.to_excel(writer, sheet_name='Data', index=False)
                df_summary.to_excel(writer, sheet_name='Analysis', index=False)
                wb = writer.book; ws = writer.sheets['Analysis']
                chart = wb.add_chart({'type': 'column'})
                chart.add_series({'values': ['Analysis', 1, 1, len(self.all_results), 1], 'categories': ['Analysis', 1, 0, len(self.all_results), 0], 'fill': {'color': 'blue'}})
                ws.insert_chart('E2', chart)
            messagebox.showinfo("Success", "Saved!")
        except Exception as e: messagebox.showerror("Error", str(e))

    def clear_columns(self):
        for w in self.columns_frame.winfo_children(): w.destroy()
        self.all_results = []

if __name__ == "__main__":
    root = tk.Tk()
    app = NERApp(root)
    root.mainloop()