# ner_model.py
import torch
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.ner import NERecognizer
from transformers import AutoTokenizer, AutoModelForTokenClassification

#========================================
# 1. صنف نموذج CAMeL Tools (الأساسي)
#========================================
class ArabicNER_CAMeL:
    def __init__(self):
        print("جاري تحميل CAMeL Tools...")
        self.recognizer = NERecognizer.pretrained()

    def extract_entities(self, text):
        tokens = simple_word_tokenize(text)
        labels = self.recognizer.predict_sentence(tokens)
        
        entities = []
        current_ent = None
        for idx, (tok, lab) in enumerate(zip(tokens, labels)):
            if lab == 'O':
                if current_ent:
                    entities.append(current_ent)
                    current_ent = None
                continue
            
            if lab.startswith('B-'):
                if current_ent:
                    entities.append(current_ent)
                current_ent = {
                    'text': tok,
                    'type': lab.split('-')[1],
                    'start_idx': idx,
                    'end_idx': idx
                }
            elif lab.startswith('I-'):
                if current_ent:
                    current_ent['text'] += ' ' + tok
                    current_ent['end_idx'] = idx
        
        if current_ent:
            entities.append(current_ent)
            
        return list(zip(tokens, labels)), entities

#========================================
# 2. صنف Helper لنماذج HuggingFace
# (هذا هو الصنف الذي كان ناقصاً ويسبب الخطأ)
#========================================
class HuggingFaceNER:
    def __init__(self, model_name):
        print(f"جاري تحميل {model_name}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForTokenClassification.from_pretrained(model_name)
            self.id2label = self.model.config.id2label
        except Exception as e:
            print(f"فشل تحميل {model_name}: {e}")
            raise ValueError(f"تعذر تحميل النموذج {model_name}. تأكد من الاتصال بالإنترنت وصحة الاسم.")

    def extract_entities(self, text):
        # 1. التجهيز
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # 2. التوقع
        predictions = torch.argmax(outputs.logits, dim=2)[0].tolist()
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

        clean_tokens = []
        clean_labels = []
        
        # 3. تنظيف التوكنز
        for token, prediction in zip(tokens, predictions):
            if token in ["[CLS]", "[SEP]", "[PAD]", "<s>", "</s>"]:
                continue
            
            label = self.id2label[prediction]
            
            # معالجة الرموز الخاصة بـ BERT (##)
            if token.startswith("##"):
                clean_tok = token.replace("##", "")
                if clean_tokens:
                    clean_tokens[-1] += clean_tok
                continue
            
            # معالجة الرموز الخاصة بـ SentencePiece (XLM-R / Electra)
            if token.startswith(" "): 
                clean_tok = token.replace(" ", "")
                clean_tokens.append(clean_tok)
                clean_labels.append(label)
                continue
                
            clean_tokens.append(token)
            clean_labels.append(label)

        # 4. تجميع الكيانات
        entities = []
        current_ent = None
        
        for idx, (tok, lab) in enumerate(zip(clean_tokens, clean_labels)):
            if lab == 'O':
                if current_ent:
                    entities.append(current_ent)
                    current_ent = None
                continue
            
            if lab.startswith('B-'):
                if current_ent:
                    entities.append(current_ent)
                current_ent = {
                    'text': tok,
                    'type': lab.split('-')[1],
                    'start_idx': idx,
                    'end_idx': idx
                }
            elif lab.startswith('I-'):
                if current_ent:
                    current_ent['text'] += ' ' + tok
                    current_ent['end_idx'] = idx
        
        if current_ent:
            entities.append(current_ent)

        return list(zip(clean_tokens, clean_labels)), entities

#========================================
# تعريف أصناف النماذج المختلفة
#========================================

class ArabicNER_mBERT(HuggingFaceNER):
    def __init__(self):
        super().__init__("Davlan/bert-base-multilingual-cased-ner-hrl")

class ArabicNER_DistilBERT(HuggingFaceNER):
    def __init__(self):
        super().__init__("Davlan/distilbert-base-multilingual-cased-ner-hrl")

class ArabicNER_XLMR(HuggingFaceNER):
    def __init__(self):
        super().__init__("Davlan/xlm-roberta-base-ner-hrl")

class ArabicNER_CamelBERT(HuggingFaceNER):
    def __init__(self):
        super().__init__("CAMeL-Lab/bert-base-arabic-camelbert-msa-ner")

class ArabicNER_GeneralBERT(HuggingFaceNER):
    def __init__(self):
        super().__init__("hatmimoha/arabic-ner")

class ArabicNER_CamelBERT_Mix(HuggingFaceNER):
    def __init__(self):
        super().__init__("CAMeL-Lab/bert-base-arabic-camelbert-mix-ner")

#========================================
# الصنف المجمع الرئيسي (مع ميزة إضافة النماذج)
#========================================
class ArabicNER:
    def __init__(self):
        # القائمة المبدئية للنماذج
        self.models = {
            "CAMeL Tools": ArabicNER_CAMeL(),
            "mBERT (Multilingual)": ArabicNER_mBERT(),
            "DistilBERT (Fast)": ArabicNER_DistilBERT(),
            "XLM-RoBERTa (Fosha)": ArabicNER_XLMR(),
            "CamelBERT (MSA)": ArabicNER_CamelBERT(),
            "General BERT (Hatmimoha)": ArabicNER_GeneralBERT(),
            "CamelBERT (Mix/Dialect)": ArabicNER_CamelBERT_Mix()
        }
        self.current_model_name = "CAMeL Tools"

    def set_model(self, model_name):
        if model_name in self.models:
            self.current_model_name = model_name
        else:
            raise ValueError(f"Model '{model_name}' not found.")

    def extract_entities(self, text):
        model = self.models[self.current_model_name]
        return model.extract_entities(text)

    # ======================================================
    # دالة إضافة نموذج جديد ديناميكياً (الميزة الجديدة)
    # ======================================================
    def add_custom_model(self, huggingface_path, display_name):
        """
        دالة لإضافة نموذج جديد ديناميكياً من رابط HuggingFace
        """
        print(f"جاري محاولة إضافة النموذج: {huggingface_path}")
        
        # نستخدم الكلاس العام HuggingFaceNER لتحميل أي رابط
        try:
            # هنا نستخدم HuggingFaceNER الذي أصبح الآن معرفاً في هذا الملف
            new_model = HuggingFaceNER(huggingface_path)
            self.models[display_name] = new_model
            return True
        except Exception as e:
            print(f"فشل إضافة النموذج: {e}")
            raise e