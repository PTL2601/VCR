import id
import decode

audio_file = "57816563491305416.wav" #!
caller_number_catch = "cdr_description.html" #!

extractor = id.CallerNumberExtractor(caller_number_catch)

stt = decode.STT(audio_file, model_path=".") #!model_path!
extractor.load_and_clean_html()

caller_number = extractor.extract_caller_number()
recognized_text = stt.decode_audio()