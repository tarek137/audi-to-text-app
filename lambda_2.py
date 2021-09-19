import json
import boto3
import datetime
from datetime import datetime
import pymysql


def lambda_handler(event, context):

    print(json.dumps(event))

    record = event['Records'][0]
    shortDate = datetime.today().strftime('%Y-%m-%d')

    BUCKET_NAME = record['s3']['bucket']['name']
    KEY = record['s3']['object']['key']
    # extract user name
    Rep = KEY.split("/")[1]
    user = Rep.split("_")[0]

    # Establish connection with RDS Database (MySQL) (same informations you provide in the flask app code )
    conn = pymysql.connect(
        host='xxxxxxxxxxxxxxxxxx',
        port=3306,
        user='xxxxxxxxxxxx',
        password='xxxxxxx',
        db='xxxxxxxx',

    )

    s3 = boto3.client('s3', 'xxxxxx') #indicate the region
    #sending S3 sql query to extract only transcript text from the transcribe json file
    response = s3.select_object_content(
        Bucket=BUCKET_NAME,
        Key=KEY,
        ExpressionType='SQL',
        Expression="SELECT * FROM s3object[*].results.transcripts[*] r",
        InputSerialization={'JSON': {"Type": "Lines"}},
        OutputSerialization={'JSON': {}},
    )

    # writing the sql query reuslt to output json file
    for event in response['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            print(records)

    with open('/tmp/output.json', 'w') as data:
        data.write(records)

    # retrieve email address of the user from Mysql database

    cur = conn.cursor()
    row = cur.execute("SELECT user_email FROM Users WHERE username = %s",
                      (user,))
    rows = cur.fetchall()
    stored_email = rows[0][0]
    # creating email

    SENDER = "xxxxxxxxxxxxxxxxxxxxx"
    RECIPIENT = stored_email
    AWS_REGION = "xxxxxxxxxxxxx"
    SUBJECT = "xxxxxxxxxxx"
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                 )
    #adding the sql query output to the body of the email
    BODY_HTML = f"<html><head>Please find your message</head><body><p>" + records + "</p></body></html>"

    CHARSET = "UTF-8"
    client = boto3.client('ses', region_name=AWS_REGION)

    # Provide the contents of the email.
    response_2 = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line

    )

    #storing the output json file in S3 under s3://username/date/text
    path = f'{user}/{shortDate}/text/{Rep}'
    s3.upload_file('/tmp/output.json', Bucket=BUCKET_NAME, Key=path)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
