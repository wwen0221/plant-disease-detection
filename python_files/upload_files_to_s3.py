import boto3
import argparse
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

print(config)
aws_access_key = config['aws']['AWSAccessKeyId']
aws_secret_key = config['aws']['AWSSecretKey']

def uploadDirectory(client, path, bucketname, key):
    print('uploading...')
    for folders in os.listdir(path):
        for cls in os.listdir(f'{path}/{folders}'):
            if not cls.endswith('.lst'):
                for img in os.listdir(f'{path}/{folders}/{cls}'):
                    client.upload_file(f'{path}/{folders}/{cls}/{img}', bucketname,
                                       f'{key}/{folders}/{cls}/{img}')
            else:
                client.upload_file(f'{path}/{folders}/{cls}', bucketname,
                                   f'{key}/{folders}/{cls}')


def main(dir, bucket, key):
    client = boto3.client('s3', region_name='ap-southeast-1',
                          aws_access_key_id=aws_access_key,
                          aws_secret_access_key=aws_secret_key)

    uploadDirectory(client, dir, bucket, key)

    #uploadDirectory(client, val_lst, bucket, key, 's3validation_lst')
    print('uploaded')

if __name__ == '__main__':

    dir = 'C:/Users/Wei Wen/Desktop/New Plant Diseases Dataset(' \
          'Augmented)/New Plant Diseases Dataset(Augmented)'
    bucket = "plant-disease-detection-tutorial"
    key = "medium-tutorial"

    main(dir,bucket,key)