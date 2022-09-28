import os
import pandas as pd
import boto3
from io import StringIO


def s3Client(
    prm_aws_endpoint,
    prm_aws_access_key_id,
    prm_aws_secret_access_key
):

    s3_client = boto3.client(
        "s3",
        endpoint_url=prm_aws_endpoint,
        aws_access_key_id=prm_aws_access_key_id,
        aws_secret_access_key=prm_aws_secret_access_key
    )
    return s3_client


def readS3(
    prm_aws_endpoint,
    prm_aws_access_key_id,
    prm_aws_secret_access_key,
    prm_aws_s3_bucket,
    localpath,
    referencepath
):

    s3 = s3Client(prm_aws_endpoint, prm_aws_access_key_id, prm_aws_secret_access_key)
    file = os.path.basename(localpath)
    with open(localpath, 'wb') as data:
        s3.download_fileobj(prm_aws_s3_bucket, referencepath, data)
    return file


def uploadS3(
    prm_aws_endpoint,
    prm_aws_access_key_id,
    prm_aws_secret_access_key,
    prm_aws_s3_bucket,
    localpath,
    referencepath
) -> str:

    s3 = s3Client(prm_aws_endpoint, prm_aws_access_key_id, prm_aws_secret_access_key)
    s3.upload_file(
        Filename=localpath,
        Bucket=prm_aws_s3_bucket,
        Key=referencepath,
        ExtraArgs={'ACL': 'bucket-owner-full-control'}
    )
    salida = os.path.join(prm_aws_endpoint, prm_aws_s3_bucket, referencepath)
    return salida


def writeS3(
    prm_aws_endpoint,
    prm_aws_access_key_id,
    prm_aws_secret_access_key,
    prm_aws_s3_bucket,
    referencepath, data
):

    s3 = s3Client(prm_aws_endpoint, prm_aws_access_key_id, prm_aws_secret_access_key)
    with StringIO() as buffer:
        data.to_csv(buffer, index=False)
        response = s3.put_object(
            Bucket=prm_aws_s3_bucket, Key=referencepath, Body=buffer.getvalue()
        )
    return response