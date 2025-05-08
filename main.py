from STT import id
from STT import STT

audio_file = "57816563491305416.wav" #!
caller_number_catch = "cdr_description.html" #!

extractor = id.CallerNumberExtractor(caller_number_catch)

stt = STT.STT(audio_file, model_path="C:/Users/Denis Beryozkin/Desktop/local test") #!model_path!
extractor.load_and_clean_html()

caller_number = extractor.extract_caller_number()
recognized_text = stt.decode_audio()