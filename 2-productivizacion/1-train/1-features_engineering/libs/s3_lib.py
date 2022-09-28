import os
import boto3
from io import StringIO

import config_lib as cl
import params_lib as pl


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

    s3 = s3Client(prm_aws_endpoint,
                  prm_aws_access_key_id,
                  prm_aws_secret_access_key)
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
):

    s3 = s3Client(prm_aws_endpoint,
                  prm_aws_access_key_id,
                  prm_aws_secret_access_key)
    s3.upload_file(
        Filename=localpath,
        Bucket=prm_aws_s3_bucket,
        Key=referencepath,
        ExtraArgs={'ACL': 'bucket-owner-full-control'}
    )


def writeS3(
    prm_aws_endpoint,
    prm_aws_access_key_id,
    prm_aws_secret_access_key,
    prm_aws_s3_bucket,
    referencepath, data
):

    s3 = s3Client(prm_aws_endpoint,
                  prm_aws_access_key_id,
                  prm_aws_secret_access_key)
    with StringIO() as buffer:
        data.to_csv(buffer, index=False)
        response = s3.put_object(
            Bucket=prm_aws_s3_bucket, Key=referencepath, Body=buffer.getvalue()
        )
    return response


def lee_s3(config, localpath, referencepath):
    prm_aws_endpoint = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_endpoint"),
        "El parametro endpoint es obligatorio."
    )
    prm_aws_s3_bucket = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_s3_bucket"),
        "El parametro bucket es obligatorio."
    )
    prm_aws_access_key_id = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_access_key_id"),
        "El parametro access_key_id es obligatorio."
    )
    prm_aws_secret_access_key = pl.validar_parametros(
        cl.valor_config(config, "s3access", "aws_secret_access_key"),
        "El parametro secret_access_key es obligatorio."
    )
    return readS3(prm_aws_endpoint,
                  prm_aws_access_key_id,
                  prm_aws_secret_access_key,
                  prm_aws_s3_bucket,
                  localpath,
                  referencepath)

