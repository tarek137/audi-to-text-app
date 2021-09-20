
# flask-audio-to-text-app 

This application allows the user to record an audio and recieve an email with the transcribed text (hosted on AWS)


Architecture diagram : 

![diagram](https://user-images.githubusercontent.com/70094057/133929432-1b06f495-b660-4e30-8a32-b2489c5c67b9.JPG)



Use case scenario : 

1) User registers with his email address (AWS cognito sends a code to the user email that he uses to validate his registration ) 
2) Once registred , the user can login using his credentials 
3) Once the user logged in , Amazon cognito generates an access token , the flask app checks the validity of the token and extracts user informations from it (sub id , username , email , login date ) : all these information are stored in a RDS database (MySQL ) 
4)  The user records his audio and hit the the submit button and the file is uploaded to S3 bucket (folder path s3://username/date/audio/filename) 
5)  Uploading the audio file will trigger a lambda function (lambda_1.py) that will create a transcribtion job and store the output in S3 (in the folder s3://transcripts/ ) 
6)  Once transcribed json file is available,  a second lambda will run a S3 sql qeury to extract only the text from the json file , add the text to the email body and sends it to the user via SES . In order to that , the lambda will query the RDS database to find the email address of the user who uploaded the file . Finally , the lambda will save the extracted text in a json file in a S3 folder ( s3://username/date/text/filename)
7)  User recieves the email with the text he recorded inside 

Important to know : 
- Please do not forget to update the config.py file with the parameters of you infrastructure , and update user pool id and client id in app.js 
- in order to generate the RSA key (kid + pem) you need to run these NodeJs commands locally : 
  1) npm install request jwk-top-pem
  2) node index.js (file available in /pem , update the cognito url inside)
 
 - you need to set up a MySQL database , you can keep the same column names (user_id /username /user_email/date) or change , in this case do not forget to update the sql queries in the code , this link can be helpful to configure the database : https://medium.com/aws-pocket/aws-rds-with-mysql-using-flask-f1c6d8cc7eff
- For audio recording I used the matt diamond javascript recorder : https://github.com/mattdiamond/Recorderjs
- Do not forget to give your lambdas the right permissions (first lmabda : S3 read + Transcribe , second lambda : S3 read and write + SES ) , adding cloudwatch permissions can be very useful for debugging and monitoring of lambda transactions
- you can run this code locally or in an EC2 instance , in this case it would be better to add a ngnix and uwsgi layer to handle several requests , this link explains how to configure it very well : https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
