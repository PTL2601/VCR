from STT import id
from STT import stt
from KWR import kws

audio = "57816563491305416.wav"
cdr = "cdr_description.html"

#ОТКРОЙ ПУТЬ ДО МОДЕЛИ
################################################################
model_path = "E:/VKR/VKR actual/STT/Vosk/model"
#model_path = "C:/Users/Denis Beryozkin/Desktop/local test"
################################################################

audio_file = audio
caller_number_catch = cdr

extractor = id.CallerNumberExtractor(caller_number_catch)

stt = stt.STT(audio_file, model_path)
extractor.load_and_clean_html()

caller_number = extractor.extract_caller_number()
recognized_text = stt.decode_audio()
keywords = kws.KWS(recognized_text)
keywords_tools = keywords.tools
keywords_problems = keywords.problems