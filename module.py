from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.ner import NERecognizer

ner = NERecognizer.pretrained()

text = "ذهب الرئيس عبد المجيد تبون إلى العاصمة الجزائر لحضور اجتماع في جامعة الجزائر."

tokens = simple_word_tokenize(text)
entities = ner.predict_sentence(tokens)

for token, ent in zip(tokens, entities):
    print(token, " -> ", ent)
