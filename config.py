

# database parameters

db_host = "database-1.cmcycie0rurf.eu-west-3.rds.amazonaws.com"
db_user = "admin"
db_password = "ttllzz00"
db_name ="konvoo"


#Cognito parameters check the readme please where i explain how to generate pem and kid

kid1 = 'EShqpvaqacoc5yuGCFhb7Z8dUg61zz3CmdmfUtSnU9I='
pem1 = '-----BEGIN RSA PUBLIC KEY-----\n'+\
'MIIBCgKCAQEAxPX5DFRRJ2Ch0zHpqUR8q+A5dtMfnhjngiaZ7WzoD3pMXnR587u0\n'\
       +'iTNn75Jxv6Vl+F8VYEQnxBvS3dYIesDJGV2IreCd40frVUmnfMk2rtfZEThvMcEY\n'\
       +'yyn9eKgaJ0tFtR15u0Gsz8uSagina7cpV03vyeyBlPf5jtzvYmNm7oSBbDAas/jo\n' \
       +'dskLwZttPXudok0G8lrjbH8ILF9a//yxKiGHV6eDC55B54J5DQ1B+y4XGKc2yR+H\n'+'yR/FsSBu15Lx6NyC8Ddd8G3nzpBU2n1SQq+cfHZOsITqWEo0Yfi9W7pSj0/cM5g8\n'\
       +'c7Nml2kygXspy9apOhfLWs4YC0oEzeGbjwIDAQAB\n'+'-----END RSA PUBLIC KEY-----\n' ,

kid2 = 'Kvj84xI+g0jPn5yGNZA9bRLLBTaxhaSR1roxfRqvYV8='
pem2 = '-----BEGIN RSA PUBLIC KEY-----\n' +'MIIBCgKCAQEAxPX5DFRRJ2Ch0zHpqUR8q+A5dtMfnhjngiaZ7WzoD3pMXnR587u0\n'\
       +'iTNn75Jxv6Vl+F8VYEQnxBvS3dYIesDJGV2IreCd40frVUmnfMk2rtfZEThvMcEY\n'\
       +'yyn9eKgaJ0tFtR15u0Gsz8uSagina7cpV03vyeyBlPf5jtzvYmNm7oSBbDAas/jo\n'+'dskLwZttPXudok0G8lrjbH8ILF9a//yxKiGHV6eDC55B54J5DQ1B+y4XGKc2yR+H\n'\
       +'yR/FsSBu15Lx6NyC8Ddd8G3nzpBU2n1SQq+cfHZOsITqWEo0Yfi9W7pSj0/cM5g8\n'\
       +'c7Nml2kygXspy9apOhfLWs4YC0oEzeGbjwIDAQAB\n'\
       +'-----END RSA PUBLIC KEY-----\n'

iss = 'https://cognito-idp.eu-west-3.amazonaws.com/eu-west-3_5QRTo1d8x'

#configure programmatic access keys from IAM AWS console for S3 client

AWS_SERVER_PUBLIC_KEY= "xxxxxxxxxxxxxxxxxxxxxx"
AWS_SERVER_SECRET_KEY ="xxxxxxxxxxxxxxxxxxxxxx"
REGION_NAME = "xxxxxxx"
BUCKET_NAME = "xxxxxxx"
