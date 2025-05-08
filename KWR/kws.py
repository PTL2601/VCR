from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)


class KWS:
    def __init__(self, input_text):
        self.input_text = input_text
        self.res = self.recog(input_text)
    def recog(self, input_text):
        # Инициализация компонентов Natasha
        emb = NewsEmbedding()
        segmenter = Segmenter()
        morph_vocab = MorphVocab()
        morph_tag = NewsMorphTagger(emb)
        # Создаём объект Doc и передаём текст
        doc = Doc(self.input_text)
        # Сегментация текста на токены
        doc.segment(segmenter)
        doc.tag_morph(morph_tag)

        # Морфологический разбор и лемматизация
        for token in doc.tokens:
            token.lemmatize(morph_vocab)

        # Получаем леммы всех слов
        lemmas = [token.lemma.lower() for token in doc.tokens]

        # Список ключевых слов в нормальной форме
        keywords = [
            "принтер", "проблема", "шум", "вентилятор", "кондиционер",
            "компьютер", "ноутбук", "сервер", "телефон", "сейф",
            "сканер", "монитор", "мышь", "клавиатура", "микрофон",
            "веб", "вебок", "камера", "краска", "сломаться", "не", "работать"
            "загружать", "загрузка", "войти", "входить", "печатать", "пускать"
            "фурычить", "неисправность", "новый", "ошибка", "перестать", "поломка"
            "сбой",
            ]

        # Поиск ключевых слов по леммам
        found_keywords = [kw for kw in keywords if kw in lemmas]
        if found_keywords.__len__() == 0:
            #print("Ключевые слова не найдены")
            return "Ключевые слова не найдены"
        else:
            #print(lemmas)
            #print("Найдены ключевые слова:", found_keywords)
            return found_keywords

#if __name__ == '__main__':
#    kws = KWS(input_text="")

