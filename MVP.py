from STT import id
from STT import stt as sptt
from KWR import kws
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER_1 = 'uploads_area1'
UPLOAD_FOLDER_2 = 'uploads_area2'

os.makedirs(UPLOAD_FOLDER_1, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_2, exist_ok=True)

app.config['UPLOAD_FOLDER_1'] = UPLOAD_FOLDER_1
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_2

ALLOWED_EXTENSIONS_1 = {'wav'}
ALLOWED_EXTENSIONS_2 = {'html'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# def recoq(audio, cdr):



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file1 = request.files.get('file1')
    file2 = request.files.get('file2')

    # Проверка первого файла
    if not file1 or file1.filename == '':
        return "Файл .wav не выбран", 400
    if not allowed_file(file1.filename, ALLOWED_EXTENSIONS_1):
        return "Разрешены только файлы .wav для первого файла", 400

    # Проверка второго файла
    if not file2 or file2.filename == '':
        return "Файл .html не выбран", 400
    if not allowed_file(file2.filename, ALLOWED_EXTENSIONS_2):
        return "Разрешены только файлы .html для второго файла", 400

    # Сохраняем файлы
    filename1 = secure_filename(file1.filename)
    file1.save(os.path.join(app.config['UPLOAD_FOLDER_1'], filename1))

    filename2 = secure_filename(file2.filename)
    file2.save(os.path.join(app.config['UPLOAD_FOLDER_2'], filename2))

    audio = f"uploads_area1/{filename1}"  # Контейнер для аудио
    cdr = f"uploads_area2/{filename2}"  # Контейнер для карточки

    # Контейнеры
    audio_file = audio
    caller_number_catch = cdr
    extractor = id.CallerNumberExtractor(caller_number_catch)  # Метод для кэча инфы с карты

    # ОТКРОЙ ПУТЬ ДО МОДЕЛИ
    ################################################################
    model_path = "E:/VKR/VKR actual/STT/Vosk/model"
    # model_path = "C:/Users/Denis Beryozkin/Desktop/local test"
    ################################################################

    stt = sptt.STT(audio_file, model_path)  # Метод расшифровки аудиофайла
    extractor.load_and_clean_html()  # Метод загрузки инфы с карты

    caller_number = extractor.extract_caller_number()  # Метод для распознания номера звонившего + контейнер
    recognized_text = stt.decode_audio()  # Метод для распознания текста + контейнер
    keywords = kws.KWS(recognized_text)  # Метод для получения ключевых слов
    keywords_tools = keywords.tools  # Контейнер для ключевых слов оборудования
    keywords_problems = keywords.problems  # Контейнер для ключевых слов поломки

    #    @app.route('/answer')
    #   def answer():
    #      return "<h1>Номер звонившего</h1>" \
    #            f"<h2>{caller_number}</h2>" \
    #           "<h1>Распознанные ключевые слова оборудования</h1>" \
    #          f"<h2>{keywords_tools}</h2>" \
    #         "<h1>Распознанные ключевые слова поломки</h1>" \
    #        f"<h2>{keywords_problems}</h2>" \
    #       "<h1>Распознанный текст</h1>" \
    #      f"<h2>{recognized_text}</h2>"
    sql_text = f"'UPDATE public.repair_request SET fault_type_id = {keywords_problems}, description = {recognized_text}, equipment_type = {keywords_tools}, phone_number = {caller_number}, recognized_by_ai = 'true' WHERE id = uuid')"
    return render_template('upload_success.html',
                           caller_number=caller_number,
                           keywords_tools=keywords_tools,
                           keywords_problems=keywords_problems,
                           recognized_text=recognized_text,
                           sql_text=sql_text)

with conn.cursor() as curs:
    curs.execute(
        '''
        INSERT INTO public.repair_request(
            id, user_id, room_id, equipment_id, fault_type_id, description,
            equipment_type, location_id, task_status, priority, user_support_id,
            is_draft, audio_file, phone_number, recognized_by_ai
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            user_id = EXCLUDED.user_id,
            room_id = EXCLUDED.room_id,
            equipment_id = EXCLUDED.equipment_id,
            fault_type_id = EXCLUDED.fault_type_id,
            description = EXCLUDED.description,
            equipment_type = EXCLUDED.equipment_type,
            location_id = EXCLUDED.location_id,
            task_status = EXCLUDED.task_status,
            priority = EXCLUDED.priority,
            user_support_id = EXCLUDED.user_support_id,
            is_draft = EXCLUDED.is_draft,
            audio_file = EXCLUDED.audio_file,
            phone_number = EXCLUDED.phone_number,
            recognized_by_ai = EXCLUDED.recognized_by_ai
        ''',
        (
            uuid, None, None, None, keywords_problems, recognized_text,
            keywords_tools, None, None, None, None, None, None, caller_number, True
        )
    )
conn.close()

if __name__ == '__main__':
    app.run(debug=True)
