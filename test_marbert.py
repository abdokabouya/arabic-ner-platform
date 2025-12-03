from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

# اسم النموذج الرسمي من الرابط الذي أرسلته
model_name = "UBC-NLP/MARBERTv2"

print(f"⏳ جاري محاولة تحميل النموذج: {model_name} ...")

try:
    # 1. تحميل الـ Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("✅ تم تحميل Tokenizer بنجاح!")

    # 2. تحميل النموذج (كنموذج NER)
    # ملاحظة: سيقوم هنا بإنشاء طبقة تصنيف عشوائية لأن النموذج أصلاً ليس لـ NER
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    print("✅ تم تحميل النموذج (Model) بنجاح!")

    # 3. تجربة بسيطة جداً
    text = "إيلون ماسك في دبي"
    inputs = tokenizer(text, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    print("\n--- تفاصيل النموذج ---")
    print(f"عدد الأصناف (Labels) الافتراضية: {len(model.config.id2label)}")
    print("النموذج يعمل، لكنه يحتاج لتدريب (Fine-tuning) ليعطي نتائج NER صحيحة.")

except Exception as e:
    print(f"\n❌ حدث خطأ أثناء التحميل: {e}")