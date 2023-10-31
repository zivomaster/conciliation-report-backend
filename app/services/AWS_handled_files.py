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
    return f'the file {key} was saved successfully'


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
