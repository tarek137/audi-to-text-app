
# flask-audio-to-text-app 

This application allows the user to record an audio and recieve an email with the transcribed text 


Architecture diagram : 

![diagram](https://user-images.githubusercontent.com/70094057/133929432-1b06f495-b660-4e30-8a32-b2489c5c67b9.JPG)



Use case scenario : 

1) User registers with his email address (AWS cognito sends a code to the user email that he uses to validate his registration ) 
2) Once registred , the user can login using his credentials 
3) Once the user logged in , Amazon cognito generates an access token , the flask app checks the validity of the token and extracts user informations from it (sub id , username , email , login date ) : all these information are stored in a RDS database (MySQL ) 
4)  The user records his audio and hit the the submit button and the file is uploaded to S3 bucket (folder path s3://username/date/audio/filename) 
5)  Uploading the audio file will trigger a lambda function (lambda_1.py) that will create a transcribtion job and store the output in S3 (in the folder s3://transcripts/ ) 
6)  Once transcribed json file are available,  a second lambda will run a S3 sql qeury to extract only the text from the json file , add the text to the email body and sends it to the user via SES . In order to that , the lambda will query the RDS database to find the email address of the user who uploaded the file . Finally , the lambda will save the extracted text in a json file in a S3 folder ( s3://username/date/text/filename)
7)  User recieves the email with the text he recorded inside 


