from fuzzywuzzy import fuzz
from stt import STT

commandsList = []


def equ(text, needed):
    return fuzz.ratio(text, needed) >= 70


def execute(text: str):
    print(f"> {text}")


stt = STT(modelpath="model")

print("listen...")
stt.listen(execute)
