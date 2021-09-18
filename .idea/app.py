import json

from flask import Flask, render_template, request , redirect
import jwt

from jwt.algorithms import RSAAlgorithm
import boto3
import pymysql


app = Flask(__name__  , static_folder='static',static_url_path='' ,
            template_folder='templates')

from werkzeug.utils import secure_filename
jwt.unregister_algorithm('RS256')
jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
s3 = boto3.client('s3')
BUCKET_NAME = 'konvoo-project'

#use cognito user_pool
client = boto3.client('cognito-idp', region_name="eu-west-3")

#connect to database
conn = pymysql.connect(
    host='database-1.cmcycie0rurf.eu-west-3.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='ttllzz00',
    db='konvoo',

)



def is_token_valid(token):
    pems_dict = {
        'EShqpvaqacoc5yuGCFhb7Z8dUg61zz3CmdmfUtSnU9I=': '-----BEGIN RSA PUBLIC KEY-----\n' +
    'MIIBCgKCAQEAxPX5DFRRJ2Ch0zHpqUR8q+A5dtMfnhjngiaZ7WzoD3pMXnR587u0\n' +
    'iTNn75Jxv6Vl+F8VYEQnxBvS3dYIesDJGV2IreCd40frVUmnfMk2rtfZEThvMcEY\n' +
    'yyn9eKgaJ0tFtR15u0Gsz8uSagina7cpV03vyeyBlPf5jtzvYmNm7oSBbDAas/jo\n' +
    'dskLwZttPXudok0G8lrjbH8ILF9a//yxKiGHV6eDC55B54J5DQ1B+y4XGKc2yR+H\n' +
    'yR/FsSBu15Lx6NyC8Ddd8G3nzpBU2n1SQq+cfHZOsITqWEo0Yfi9W7pSj0/cM5g8\n' +
    'c7Nml2kygXspy9apOhfLWs4YC0oEzeGbjwIDAQAB\n' +
    '-----END RSA PUBLIC KEY-----\n' ,
        'Kvj84xI+g0jPn5yGNZA9bRLLBTaxhaSR1roxfRqvYV8=': '-----BEGIN RSA PUBLIC KEY-----\n' +
    'MIIBCgKCAQEAxPX5DFRRJ2Ch0zHpqUR8q+A5dtMfnhjngiaZ7WzoD3pMXnR587u0\n' +
    'iTNn75Jxv6Vl+F8VYEQnxBvS3dYIesDJGV2IreCd40frVUmnfMk2rtfZEThvMcEY\n' +
    'yyn9eKgaJ0tFtR15u0Gsz8uSagina7cpV03vyeyBlPf5jtzvYmNm7oSBbDAas/jo\n' +
    'dskLwZttPXudok0G8lrjbH8ILF9a//yxKiGHV6eDC55B54J5DQ1B+y4XGKc2yR+H\n' +
    'yR/FsSBu15Lx6NyC8Ddd8G3nzpBU2n1SQq+cfHZOsITqWEo0Yfi9W7pSj0/cM5g8\n' +
    'c7Nml2kygXspy9apOhfLWs4YC0oEzeGbjwIDAQAB\n' +
    '-----END RSA PUBLIC KEY-----\n'

    }

    kid = jwt.get_unverified_header(token)['kid']
    pem = pems_dict.get(kid, None)

    if pem is None:
        print ('kid false')
        return False

    try:
        decoded_token = jwt.decode(token, pem, algorithms=['RS256'])
        iss = 'https://cognito-idp.eu-west-3.amazonaws.com/eu-west-3_5QRTo1d8x'
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

    return render_template('index_3.html')

@app.route("/" , methods=['POST'])
def test():
        username = request.form['username']

        password = request.form['password']
        response = client.initiate_auth(
            ClientId='6j18jgjcmnlb5s0qnph8vr9q4r',
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
        }
        )
        access_token = response['AuthenticationResult']['AccessToken']

        response_2 = client.get_user(
            AccessToken=access_token
        )
        for attr in response_2['UserAttributes']:
            if attr['Name'] == 'sub':
                user_id = attr['Value']
            break
        for attr in response_2['UserAttributes']:
            if attr['Name'] == 'email':
                user_email = attr['Value']
            break
        date = response_2['ResponseMetadata']['HTTPHeaders']['date']

    # send information to AWS MySQL databse
        cur = conn.cursor()
        cur.execute("REPLACE INTO Users (user_id,username,user_email , Last_login_date) VALUES (%s,%s,%s,%s)",
                (user_id, username, user_email, date))
        conn.commit()
        conn.close()






@app.route("/code_registration")
def code_registration():
    return render_template('code_registration.html')


@app.route("/welcome")
def welcome():
    for key, value in request.headers:
        print(key, ' : ', value)
    return render_template('welcome2video1.html')


@app.route("/video_2")
def video_2():
    return render_template("welcome2video2.html")

@app.route("/video_3")
def video_3():
    return render_template("welcome2video3.html")

@app.route("/video_4")
def video_4():
    return render_template("welcome2video4.html")

@app.route("/video_5")
def video_5():
    return render_template("welcome2video5.html")

@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        audio_data = request.files['audio_data']
        if audio_data:
            filename = secure_filename(audio_data.filename)
            audio_data.save(filename)
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            )
            msg = "Upload Done ! "

    return render_template("index_2.html", msg=msg)





@app.route("/api/protected_api", methods=["POST"])
def protected_api():
    access_token = request.form['access_token']
    if (is_token_valid(access_token)):
        '''response = client.get_user(
            AccessToken=access_token
        )
        #Extract attributes form access token
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

        #send information to AWS MySQL databse
        cur = conn.cursor()
        cur.execute("REPLACE INTO Users (user_id,username,user_email , Last_login_date) VALUES (%s,%s,%s,%s)",
                    (user_id , username , user_email,date))
        conn.commit()
        conn.close()'''

        return  'Welcome to Konvoo , Please watch the first video and record your message , ' \
               'once done hit the "Next" button to watch the following video ' \


    else :
        return 'bad token' , 401 , redirect("/")


if __name__ == '__main__':
    app.run(debug=True)