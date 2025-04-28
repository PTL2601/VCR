import csv
import re


class KeywordComparator:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.keywords = self.load_keywords()

    def load_keywords(self):
        keywords = []
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    keywords.extend(row)
        except FileNotFoundError:
            print(f"Файл {self.csv_file_path} не найден.")
        return [keyword.strip().lower() for keyword in keywords]

    def compare_string(self, input_string):
        input_string = re.sub(r'[^\w\s]', '', input_string).lower()
        words = input_string.split()
        found_keywords = [word for word in words if word in self.keywords]
        return found_keywords


# Пример использования
#if __name__ == "__main__":
#    csv_file_path = "keywords.csv"  # Путь к вашему CSV файлу
#    comparator = KeywordComparator(csv_file_path)
#    input_string = "у меня принтер не работает"
#    found_keywords = comparator.compare_string(input_string)
#    print(f"Найденные ключевые слова: {found_keywords}")