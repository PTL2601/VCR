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
        self.tools = self.recog(input_text, "tools")
        self.problems = self.recog(input_text, "problems")
    def recog(self, input_text, OR):
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
        keywords_tools = [
            "принтер",  "вентилятор", "кондиционер",
            "компьютер", "ноутбук", "сервер", "телефон", "сейф",
            "сканер", "монитор", "мышь", "клавиатура", "микрофон",
            "веб", "вебок", "камера",
            ]
        keywords_problems = [
            "проблема", "шум", "не", "работать"
            "загружать", "загрузка", "войти", "входить", "печатать", "пускать"
            "фурычить", "неисправность", "новый", "ошибка", "перестать", "поломка"
            "сбой", "краска", "сломаться",
        ]

        # Поиск ключевых слов по леммам
        found_tools = [kw for kw in keywords_tools if kw in lemmas]
        found_problems = [kw for kw in keywords_problems if kw in lemmas]
        if found_tools.__len__() == 0 & found_problems.__len__() == 0:
            #print("Ключевые слова не найдены")
            return "Ключевые слова не найдены", "Ключевые слова не найдены"
        else:
            #print(lemmas)
            #print("Найдены ключевые слова техники:", found_tools)
            #print("Найдены ключевые слова проблем:", found_problems)
            if OR == "tools":
                return found_tools
            if OR == "problems":
                return found_problems

#if __name__ == '__main__':
    #kws = KWS(input_text="прошу устранить шумы передача звуковых сообщений по телефону филиппов пятьсот третий кабинет спасибо")
    #keywords_tools = kws.tools
    #keywords_problems = kws.problems
