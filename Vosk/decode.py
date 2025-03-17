#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json

SetLogLevel(0)

wf = wave.open("decoder-test2.wav", "rb")

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model(".")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)
#a=""
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break

    if rec.AcceptWaveform(data):
        a = json.loads(rec.Result())
    #else:
        #print(rec.PartialResult())
#a=rec.FinalResult()
a=json.loads(rec.FinalResult())
print(a["text"])
