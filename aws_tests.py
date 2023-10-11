import boto3
import os
from dotenv import load_dotenv
from botocore.client import Config
import boto3.session


#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

load_dotenv()
#Current plan: save credentials in .env, load with os.
aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
bucket_name = 'r33-friender-mg-dz'



# s3 = boto3.client('s3')
# s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

#Below is needed for pre-signed URLs: signature version must be updated,
#Region name is a hacky workaround to an error I was getting.

session = boto3.session.Session(region_name='us-east-2')
s3 = session.client('s3', config= boto3.session.Config(signature_version='s3v4'))


#Generate pre-signed URL for image already in bucket
#Getting an error
#The authorization mechanism you have provided is not supported.
#Please use AWS4-HMAC-SHA256.

#Googling suggests that signature type is too old.
signed_url = s3.generate_presigned_url("get_object",
                                       Params={"Bucket": bucket_name,
                                                "Key": 'Dawid-Planeta-fox.jpg'},
                                       ExpiresIn=1200)
# print(signed_url)
# Upload file to bucket
s3.upload_file('./memory-game.png', bucket_name, 'mem-game2.png')







# List all buckets
# buckets_resp = s3.list_buckets()
# for bucket in buckets_resp["Buckets"]:
#     print(bucket)


# # List all objects in bucket (gives metadata, not file itself)
# response = s3.list_objects_v2(Bucket=bucket_name)
# for obj in response["Contents"]:
#     print(obj)





## FIXME: THIS APPROACH DID NOT WORK.
# ClientError: An error occurred (AccessControlListNotSupported) when
# calling the PutObject operation: The bucket does not allow ACLs

# with open("./meme-gen.png", "rb") as file:
#     s3.upload_fileobj(file, bucket_name, "meme-gen.png",
#                       ExtraArgs={"ACL": "public-read"})

#This works, but jesus
# s3resource = boto3.resource('s3')
# s3resource.meta.client.upload_file('./meme-gen.png', bucket_name, 'meme-new.png')











##Misc Notes:
#Below error came about due to clock being not synced properly (running clockfix
# in terminal was enough to fix)

#ClientError: An error occurred (RequestTimeTooSkewed) when calling the
#ListBuckets operation: The difference between the request time and the
#current time is too large.





## Unneeded, from documentation:
# s3 = boto3.resource('s3')
# for bucket in s3.buckets.all():
#     print(bucket.name)

# client = boto3.client(
#     's3',
#     aws_access_key_id=aws_access_key,
#     aws_secret_access_key=aws_secret_key
# )

# session = boto3.Session(
#     aws_access_key_id=aws_access_key,
#     aws_secret_access_key=aws_secret_key,
# )
