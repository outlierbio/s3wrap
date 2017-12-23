import os
import boto3
from moto import mock_s3

os.environ['SCRATCH_DIR'] = '/tmp'  # override any user-defined scratch dir

import s3wrap


@mock_s3
def test_key_exists():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='bucket')
    conn.Object('bucket', 'key').put(Body=b'test data', ServerSideEncryption='AES256')

    assert s3wrap.key_exists('bucket', 'key')


@mock_s3
def test_swap_args_download():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='bucket')
    conn.Object('bucket', 'key').put(Body=b'test data', ServerSideEncryption='AES256')

    args = ['cat', 's3://bucket/key', '-']
    local_args, s3_downloads, s3_uploads = s3wrap.swap_args(args)

    assert 's3://bucket/key' in s3_downloads
    assert s3_downloads['s3://bucket/key'].startswith('/tmp')  # {<s3_path>: <local_path>}

    assert local_args[0] == 'cat'
    assert local_args[1].startswith('/tmp')  # local temp file
    assert local_args[2] == '-'

    assert s3_uploads == {}


@mock_s3
def test_swap_args_upload():
    args = ['echo', '"this is a test"', '>', 's3://bucket/new_key']
    local_args, s3_downloads, s3_uploads = s3wrap.swap_args(args)

    assert 's3://bucket/new_key' in s3_uploads
    assert s3_uploads['s3://bucket/new_key'].startswith('/tmp')  # {<s3_path>: <local_path>}

    assert s3_downloads == {}
