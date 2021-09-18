from flask import Flask, render_template, request , redirect
import jwt
import datetime
from jwt.algorithms import RSAAlgorithm
import boto3
import pymysql
from datetime import datetime
import config

app = Flask(__name__  , static_folder='static',static_url_path='' ,
            template_folder='templates')

from werkzeug.utils import secure_filename
jwt.unregister_algorithm('RS256')
jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
s3 = boto3.client('s3',
                         aws_access_key_id=config.AWS_SERVER_PUBLIC_KEY,
                         aws_secret_access_key=config.AWS_SERVER_SECRET_KEY,
                         region_name=config.REGION_NAME
                         )
BUCKET_NAME = config.BUCKET_NAME

#use cognito user_pool
client = boto3.client('cognito-idp', region_name="eu-west-3")

#connect to database
conn = pymysql.connect(
    host=config.db_host,
    port=3306,
    user=config.db_user,
    password=config.db_password,
    db=config.db_name,

)


#decoding access token with RSA secret key (pem format) and checking 'iss' key value to validate the cognito JWT
def is_token_valid(token):
    pems_dict = {
        config.kid1: config.pem1,
        config.kid2: config.pem2
    }

    kid = jwt.get_unverified_header(token)['kid']
    pem = pems_dict.get(kid, None)

    if pem is None:
        print ('kid false')
        return False

    try:
        decoded_token = jwt.decode(token, pem, algorithms=['RS256'])
        iss = config.iss
        if decoded_token['iss'] != iss:
            print ('iss false')
            return False
        elif decoded_token['token_use'] != 'access':
            print ('access false')
            return False
        return True
    except Exception:
        return False



@app.route("/")
def hello():

    return render_template('index_home.html')


@app.route("/code_registration")
def code_registration():

    return render_template('code_registration.html')


@app.route("/welcome")
def welcome():
    for key, value in request.headers:
        print(key, ' : ', value)
    return render_template('welcome.html')


@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        audio_data = request.files['audio_data']
        if audio_data:
            filename = secure_filename(audio_data.filename)
            audio_data.save(filename)
            shortDate = datetime.today().strftime('%Y-%m-%d')
            #setting the path where the file will be stored in S3 (s3://user_name/date/audio/file_name)
            path = filename.split("_")[0]+"/"+shortDate+"/"+"audio/"+filename
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=path
            )

    return "upload done"


@app.route("/api/protected_api", methods=["POST"])
def protected_api():
    #access token sent from js frontend
    access_token = request.form['access_token']

    #checking access token validity
    if (is_token_valid(access_token)):

        # Extract attributes form access token using boto3 cognito client and get_user method
        response = client.get_user(
            AccessToken=access_token
        )

        username = response['Username']
        for attr in response['UserAttributes']:
            if attr['Name'] == 'sub':
                user_id = attr['Value']
                break
        for attr in response['UserAttributes']:
            if attr['Name'] == 'email':
                user_email = attr['Value']
                break
        date= response['ResponseMetadata']['HTTPHeaders']['date']

        #send collected informations to AWS MySQL databse
        cur = conn.cursor()
        cur.execute("REPLACE INTO Users (user_id,username,user_email , Last_login_date) VALUES (%s,%s,%s,%s)",
                    (user_id , username , user_email,date))
        conn.commit()

        return "Welcome Please record your message"


    else :
        return 'bad token' , 401 , redirect("/")


if __name__ == '__main__':
    app.run(debug=True)