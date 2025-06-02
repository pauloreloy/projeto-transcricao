import boto3
import time
import uuid
import json

# AWS clients
transcribe  = boto3.client("transcribe")
s3          = boto3.client("s3")

# Settings
bucket_name     = "projeto-transcricao"
audio_key       = "audios/cleaned-mono.wav"
s3_uri          = f"s3://{bucket_name}/{audio_key}"
job_name        = f"transcription-{uuid.uuid4()}"  # Unique job name

# Start transcription job
response = transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={"MediaFileUri": s3_uri},
    MediaFormat="wav",
    MediaSampleRateHertz=8000,
    LanguageCode="pt-BR",
    Settings={
        "ChannelIdentification": False,  # True if you want to separate call sides
        "ShowSpeakerLabels": True,
        "MaxSpeakerLabels": 2
    }
)

# Wait until the job finishes
while True:
    status      = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    job_status  = status["TranscriptionJob"]["TranscriptionJobStatus"]
    if job_status in ["COMPLETED", "FAILED"]:
        break
    print(f"Waiting for job... Current status: {job_status}")
    time.sleep(5)

# Check result
if job_status == "COMPLETED":
    transcript_file_uri = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

    # Get transcription result from the URI (it's a public HTTPS link)
    import requests
    transcript_json = requests.get(transcript_file_uri).json()
    transcript_text = transcript_json["results"]["transcripts"][0]["transcript"]
    print("Transcript:", transcript_text)
else:
    print("Transcription failed.")
