import os
import json
import ffmpeg
import soundfile as sf
from vosk import Model, KaldiRecognizer

class STT:
    def __init__(self, audio_path: str, model_path: str = "."):
        self.audio_path = audio_path
        self.model_path = model_path
        self.model = Model(model_path)

    @classmethod
    def is_not_wav(cls, file_path: str) -> bool:
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                return header != b'RIFF'
        except Exception:
            return True

    @classmethod
    def convert_to_wav(cls, input_file: str, output_file: str = None, sample_rate: int = 8000,
                       channels: int = 1) -> str:
        if not output_file:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_converted.wav"

        (
            ffmpeg
            .input(input_file)
            .output(
                output_file,
                format='wav',
                acodec='pcm_s16le',
                ar=sample_rate,
                ac=channels
            )
            .overwrite_output()
            .run(quiet=True)
        )
        return output_file

    def decode_audio(self) -> str:
        audio_path = self.audio_path

        if self.is_not_wav(audio_path):
            audio_path = self.convert_to_wav(audio_path)

        data, samplerate = sf.read(audio_path, dtype='int16')

        if len(data.shape) > 1 and data.shape[1] > 1:
            data = data.mean(axis=1).astype('int16')

        rec = KaldiRecognizer(self.model, samplerate)
        rec.SetWords(True)

        results = []
        chunk_size = 4000

        for start in range(0, len(data), chunk_size):
            chunk = data[start:start + chunk_size]
            chunk_bytes = chunk.tobytes()
            if rec.AcceptWaveform(chunk_bytes):
                results.append(json.loads(rec.Result()))

        results.append(json.loads(rec.FinalResult()))
        text = " ".join([res.get('text', '') for res in results]).strip()

        return text




