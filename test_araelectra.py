from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

# اسم النموذج الرسمي لـ AraELECTRA (النسخة Discriminator هي المستخدمة للتدريب)
model_name = "aubmindlab/araelectra-base-discriminator"

print(f"⏳ جاري محاولة تحميل النموذج: {model_name} ...")

try:
    # 1. تحميل الـ Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("✅ تم تحميل Tokenizer بنجاح!")

    # 2. تحميل النموذج (كنموذج NER)
    # ملاحظة: هذا نموذج خام، لذا ستظهر رسالة تحذير بأن الأوزان غير مهيئة (Weights not initialized)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    print("✅ تم تحميل النموذج (Model) بنجاح!")

    # 3. تجربة بسيطة
    text = "الطقس جميل في الإسكندرية"
    inputs = tokenizer(text, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    print("\n--- تفاصيل النموذج ---")
    print(f"نوع النموذج: {type(model).__name__}")
    print(f"عدد الأصناف (Labels) الافتراضية: {len(model.config.id2label)}")
    print("النموذج يعمل تقنياً، لكنه (Base Model) ويحتاج لنموذج مدرب (Fine-tuned) لاستخراج الكيانات.")

except Exception as e:
    print(f"\n❌ حدث خطأ أثناء التحميل: {e}")