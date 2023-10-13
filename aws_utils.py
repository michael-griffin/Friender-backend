import boto3
import os
from dotenv import load_dotenv
from botocore.client import Config
import boto3.session


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

load_dotenv()
# Current plan: save credentials in .env, load with os.
aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
bucket_name = 'r33-friender-mg-dz'


# Below is needed for pre-signed URLs: signature version must be updated,
# Region name should match that of bucket we're using.

session = boto3.session.Session(region_name='us-east-2')
s3 = session.client(
    's3', config=boto3.session.Config(signature_version='s3v4'))


# Generate pre-signed URL for image already in bucket
def get_image_url(img_name):
    signed_url = s3.generate_presigned_url("get_object",
                                           Params={
                                               "Bucket": bucket_name, "Key": img_name},
                                           ExpiresIn=3600)

    print(signed_url)
    return signed_url


def upload_image(filepath, img_filename):
    s3.upload_file(filepath, bucket_name, img_filename)
    return "upload complete"




















# Upload file to bucket
# def upload_image(img_filename):
#     s3.upload_file(f"./{img_filename}.png", bucket_name, img_filename)
#     return "upload complete"



# with open("./meme-gen.png", "rb") as file:
#     s3.upload_fileobj(file, bucket_name, "meme-gen.png",
#                       ExtraArgs={"ACL": "public-read"})


# Generate pre-signed URL for image already in bucket
# Getting an error
# The authorization mechanism you have provided is not supported.
# Please use AWS4-HMAC-SHA256.

# #Googling suggests that signature type is too old.
# signed_url = s3.generate_presigned_url("get_object",
#                                        Params={"Bucket": bucket_name,
#                                                 "Key": 'Dawid-Planeta-fox.jpg'},
#                                        ExpiresIn=1200)


# List all buckets
# buckets_resp = s3.list_buckets()
# for bucket in buckets_resp["Buckets"]:
#     print(bucket)


# # List all objects in bucket (gives metadata, not file itself)
# response = s3.list_objects_v2(Bucket=bucket_name)
# for obj in response["Contents"]:
#     print(obj)


# FIXME: THIS APPROACH DID NOT WORK.
# ClientError: An error occurred (AccessControlListNotSupported) when
# calling the PutObject operation: The bucket does not allow ACLs

# with open("./meme-gen.png", "rb") as file:
#     s3.upload_fileobj(file, bucket_name, "meme-gen.png",
#                       ExtraArgs={"ACL": "public-read"})

# This works, but jesus
# s3resource = boto3.resource('s3')
# s3resource.meta.client.upload_file('./meme-gen.png', bucket_name, 'meme-new.png')


# Misc Notes:
# Below error came about due to clock being not synced properly (running clockfix
# in terminal was enough to fix)

# ClientError: An error occurred (RequestTimeTooSkewed) when calling the
# ListBuckets operation: The difference between the request time and the
# current time is too large.


# Unneeded, from documentation:
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
