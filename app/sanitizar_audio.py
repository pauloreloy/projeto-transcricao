import os
import boto3
import uuid
from pydub import AudioSegment, effects
from pydub.silence import detect_leading_silence

# === CONFIG ===
local_input = "audios/audio1.mp3"
cleaned_output = "audios/sanitized_audio_1.wav"
s3_bucket = "your-bucket"
s3_key = f"transcribe/input_{uuid.uuid4()}.wav"

# === STEP 1: Load audio with pydub ===
audio = AudioSegment.from_file(local_input)

# === STEP 2: Trim leading silence ===
def trim_leading_silence(audio_segment, silence_thresh=-50.0, chunk_size=10):
    start_trim = detect_leading_silence(audio_segment, silence_thresh, chunk_size)
    return audio_segment[start_trim:]

audio = trim_leading_silence(audio)

# === STEP 3: Normalize volume ===
audio = effects.normalize(audio)

# === STEP 4: Resample to 8kHz mono ===
audio = audio.set_frame_rate(8000).set_channels(1).set_sample_width(2)

# === STEP 5: Export as WAV (PCM 16-bit) ===
audio.export(cleaned_output, format="wav")

s3 = boto3.client("s3")

#with open(cleaned_output, "rb") as f:
#    s3.upload_fileobj(f, s3_bucket, s3_key)
#
#print(f"Uploaded sanitized file to s3://{s3_bucket}/{s3_key}")
