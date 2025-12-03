from transformers import AutoTokenizer, AutoModelForTokenClassification

model_name = "Davlan/xlm-roberta-base-ner-hrl"

print("جاري محاولة تحميل Tokenizer...")
# هنا سيظهر الخطأ الحقيقي إذا كانت sentencepiece ناقصة
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("جاري محاولة تحميل النموذج...")
model = AutoModelForTokenClassification.from_pretrained(model_name)

print("✅ تم التحميل بنجاح!")