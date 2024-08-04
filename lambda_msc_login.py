import json
import boto3
import urllib.parse

"""code adapted from amazonaws:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
"""

dynamodb = boto3.resource('dynamodb')
table_login = dynamodb.Table('login')
table_music = dynamodb.Table('music')
table_subscribe = dynamodb.Table('subscribe')


def lambda_handler(event, context):
    email = event['email']
    password = event['password']

    response = table_login.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email))

    items = response['Items']

    if items and items[0].get('password') == password:
        username = items[0].get('user_name')
        subscriptions = []

        #response = table_music.scan(ProjectionExpression='#ttl, #art, #yr',
                                    ExpressionAttributeNames={'#ttl': 'title', '#art': 'artist', '#yr': 'year'})

        response = table_subscribe.get_item(Key={'email': email})
        if response and 'Item' in response:
            for tle in response['Item'].get('title', '').split(','):
                try:
                    music_info = table_music.query(
                        KeyConditionExpression=boto3.dynamodb.conditions.Key('title').eq(tle))

                    if 'Items' in music_info and music_info['Items']:
                        music_item = music_info['Items'][0]
                        object_url = f"https://song-artist-image.s3.amazonaws.com/{urllib.parse.quote(music_item['title'])}"
                        subscriptions.append({
                            'title': tle,
                            'artist': music_item['artist'],
                            'year': music_item['year'],
                            'img_url': object_url
                        })

                except Exception as e:
                    pass

        return {
            'statusCode': 200,
            'body': json.dumps({'username': username, 'email': email, 'subscriptions': subscriptions})
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid email or password'})
        }