import boto3
import uuid
import json

def lambda_handler(event, context):
    print(json.dumps(event))

    record = event['Records'][0]
    #collecting bucket name and key
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']

    #extracting the file name from the key
    file = s3object.split("/")[3]
    s3Path = f's3://{s3bucket}/{s3object}'
    jobName = f'{file}-{str(uuid.uuid4())}'
    #setting the output path (transcripts will be stored under "s3://transcripts/" folder)
    outputKey = f'transcripts/{file}-transcript.json'

    client = boto3.client('transcribe')

    response = client.start_transcription_job(
        TranscriptionJobName=jobName,
        LanguageCode='fr-FR',
        Media={'MediaFileUri': s3Path},
        OutputBucketName=s3bucket,
        OutputKey=outputKey
    )

    print(json.dumps(response, default=str))

    return {
        'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName']
    }
