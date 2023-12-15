from dotenv import load_dotenv
from datetime import datetime
import boto3
import json
import os


load_dotenv()

current_time = datetime.now()

# 시간을 이용하여 파일 이름 생성
formatted_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")

# S3 저장을 위한 정보
aws_access_key_id = os.getenv("CREDENTIALS_ACCESS_KEY")
aws_secret_access_key = os.getenv("CREDENTIALS_SECRET_KEY")
aws_region = 'ap-northeast-2'

# Create an S3 client
s3 = boto3.client('s3', 
                  aws_access_key_id=aws_access_key_id, 
                  aws_secret_access_key=aws_secret_access_key, 
                  region_name=aws_region)

bucket_name = "hellogptv-weather"
file_name = formatted_time

def upload_dict_to_s3(bucket, file_name, file):
    encode_file = json.dumps(file, indent=4, ensure_ascii=False)
    try:
        s3.put_object(Bucket=bucket, Key=file_name, Body=encode_file)
        return True
    except:
        return False
    