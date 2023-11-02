import boto3
from botocore.exceptions import ClientError
from loguru import logger
from typing import Optional

from app.core.config import settings


def s3_upload(contents: bytes, key: str, path: str = None) -> Optional[str]:
    # get bucket
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    # bucket = s3.Bucket(settings.AWS_BUCKET_NAME)
    logger.info(f'Uploading {key} to s3')
    s3.put_object(
        Bucket=settings.AWS_BUCKET_NAME,
        Key=path + key,
        Body=contents
    )
    return f'the file {key} was saved successfully on {path + key}'


def s3_download(key: str, path: str = None):
    # get bucket
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    try:
        logger.info(f'Downloading {key} from s3')
        return s3.get_object(
            Bucket=settings.AWS_BUCKET_NAME,
            Key=path + key
        )
    except ClientError as err:
        logger.error(str(err))


def s3_delete(key: str, path: str = None) -> Optional[str]:
    # get bucket
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    try:
        logger.error(str(
            f"File '{key}' deleted successfully from '{settings.AWS_BUCKET_NAME}' bucket."))
        response = s3.delete_object(
            Bucket=settings.AWS_BUCKET_NAME, Key=path + key)
        return f"File '{key}' deleted successfully from '{settings.AWS_BUCKET_NAME}' bucket."
    except ClientError as err:
        logger.error(str(err))
        return f"Error: {str(err)}"


def s3_search(key: str, path: str = None) -> Optional[bool]:
    # is_exist
    is_exist = False
    # get bucket
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    # Check if the object exists in the S3 bucket
    try:
        s3.head_object(Bucket=settings.AWS_BUCKET_NAME, Key=path + key)
        is_exist = True  # Object exists
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            is_exist = False  # Object does not exist
        else:
            # Handle other potential errors
            is_exist = False
    return is_exist
