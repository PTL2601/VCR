from STT import id
from STT import stt
from KWR import kws
import psycopg2 as pg

# Подключение к БД
try:
    # Контейнер с подключением к БД
    conn = pg.connect(dbname='postgres', user='postgres', password='0000', host='localhost')
except: print("Не удалось подключиться к базе данных")  # При неудаче

# Контейнеры временные
audio = "57816563491305416.wav" # Контейнер для аудио
cdr = "cdr_description.html" # Контейнер для карточки

# ОТКРОЙ ПУТЬ ДО МОДЕЛИ
################################################################
# model_path = "E:/VKR/VKR actual/STT/Vosk/model"
# model_path = "C:/Users/Denis Beryozkin/Desktop/local test"
################################################################

# Контейнеры
audio_file = audio
caller_number_catch = cdr

extractor = id.CallerNumberExtractor(caller_number_catch)       # Метод для кэча инфы с карты

stt = stt.STT(audio_file, model_path)       # Метод расшифровки аудиофайла
extractor.load_and_clean_html()             # Метод загрузки инфы с карты


caller_number = extractor.extract_caller_number()       # Метод для распознания номера звонившего + контейнер
recognized_text = stt.decode_audio()                    # Метод для распознания текста + контейнер
keywords = kws.KWS(recognized_text)                     # Метод для получения ключевых слов
keywords_tools = keywords.tools                         # Контейнер для ключевых слов оборудования
keywords_problems = keywords.problems                   # Контейнер для ключевых слов поломки

# with conn.cursor() as curs:
#     curs.execute(
#         'INSERT INTO public.repair_request(id, user_id, room_id, equipment_id, fault_type_id, description, equipment_type, location_id, task_status, priority, user_support_id, is_draft, audio_file, phone_number, recognized_by_ai) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', ('testingVOSK', 'null', 'null', 'null', keywords_problems, recognized_text, keywords_tools, 'null', 'null', 'null', 'null', 'null', 'null', caller_number, 'true'))
# conn.close()