import os
import time
import vosk
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class STT:
    def __init__(self, modelpath: str = "model", samplerate: int = 16000):
        self.__REC__ = vosk.KaldiRecognizer(vosk.Model(modelpath), samplerate)
        self.__SAMPLERATE__ = samplerate

    def transcribe_audio(self, audio_file: str, output_file: str):
        """
        Распознает текст из аудиофайла и записывает его в output_file.
        """
        with open(audio_file, "rb") as f:
            while True:
                data = f.read(4000)  # Чтение файла блоками по 4000 байт
                if len(data) == 0:
                    break
                if self.__REC__.AcceptWaveform(data):
                    result = json.loads(self.__REC__.Result())
                    with open(output_file, "a") as out:
                        out.write(result["text"] + "\n")
            # Обработка оставшихся данных
            final_result = json.loads(self.__REC__.FinalResult())
            with open(output_file, "a") as out:
                out.write(final_result["text"] + "\n")


class FileHandler(FileSystemEventHandler):
    def __init__(self, stt: STT, watch_folder: str):
        self.stt = stt
        self.watch_folder = watch_folder

    def on_created(self, event):
        """
        Обрабатывает событие создания файла.
        """
        if not event.is_directory and os.path.basename(event.src_path) == "test.wav":
            print(f"Найден файл 'test'. Начинаю обработку...")
            time.sleep(2)
            output_file = os.path.join(self.watch_folder, "transcript.txt")
            self.stt.transcribe_audio(event.src_path, output_file)
            print("Текст успешно записан в файл 'transcript.txt'.")

            # Переименовываем файл
            new_name = os.path.join(self.watch_folder, "test_recog.wav")
            os.rename(event.src_path, new_name)
            print(f"Файл 'test' переименован в 'test_recog'.")


def main():
    watch_folder = "observe"  # Папка, в которой программа ищет файл "test"
    model_path = "model"  # Путь к модели Vosk

    # Инициализация STT
    stt = STT(modelpath=model_path)

    # Инициализация наблюдателя за файловой системой
    event_handler = FileHandler(stt, watch_folder)
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()

    print(f"Ожидание появления файла 'test' в папке '{watch_folder}'...")

    try:
        while True:
            time.sleep(1)  # Ожидание
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()