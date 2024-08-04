import boto3
import urllib.parse
from boto3.dynamodb.conditions import Attr, Key
import json

"""code adapted from amazonaws:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
"""

dynamodb = boto3.resource('dynamodb')
table_music = dynamodb.Table('music')
table_subscribe = dynamodb.Table('subscribe')


def lambda_handler(event, context):
    if event.get('subscribe'):
        email = str(event['email'])
        title = str(event['title'])

        sub_result = subscribe_music(email, title)
        subs = sub_list(email)

        return {
            'statusCode': 200,
            'body': json.dumps({'subscriptions': subs, 'message': sub_result})
        }

    elif event.get('remove'):
        email = str(event['email'])
        title = event['title']

        response = table_subscribe.get_item(Key={'email': email})
        item = response.get('Item')

        if item:
            user_titles = item.get('title', '').split(',')
            if title in user_titles:
                user_titles.remove(title)
                updated_title = ','.join(user_titles)
                table_subscribe.update_item(Key={'email': email}, UpdateExpression='SET title = :val',
                                            ExpressionAttributeValues={':val': updated_title})

        subs = sub_list(email)
        return {
            'statusCode': 200,
            'body': json.dumps({'subscriptions': subs})
        }


    else:
        title = event.get('title')
        artist = event.get('artist')
        year = event.get('year')

        filter_expression = None

        if title:
            filter_expression = Attr('title').eq(title)
        if artist:
            filter_expression = filter_expression & Attr('artist').eq(artist) if filter_expression else Attr(
                'artist').eq(artist)
        if year:
            filter_expression = filter_expression & Attr('year').eq(year) if filter_expression else Attr('year').eq(
                year)

        if filter_expression:
            response = table_music.scan(FilterExpression=filter_expression)
            search_results = response['Items']

            for search in search_results:
                search['img_url'] = f"https://song-artist-image.s3.amazonaws.com/{urllib.parse.quote(search['title'])}"
        else:
            search_results = None

        return {
            'statusCode': 200,
            'body': json.dumps({'search_results': search_results})
        }


def subscribe_music(email, title):
    response = table_subscribe.get_item(Key={'email': email})
    item = response.get('Item')

    if item:
        user_titles = item.get('title', '').split(',')
        if title in user_titles:
            return "already subscribed"

        else:
            updated_title = ','.join(user_titles + [title])
            table_subscribe.update_item(Key={'email': email}, UpdateExpression='SET title = :val',
                                        ExpressionAttributeValues={':val': updated_title})
            return "subscription successful"

    else:
        table_subscribe.put_item(Item={'email': email, 'title': title})
        return "subscription successful"


def sub_list(email):
    subs = []

    response = table_subscribe.get_item(Key={'email': email})
    item = response.get('Item')

    if item and item.get('title'):
        for tle in item.get('title', '').split(','):
            if tle:
                music_info = table_music.query(KeyConditionExpression=Key('title').eq(tle))

                if 'Items' in music_info and music_info['Items']:
                    music_item = music_info['Items'][0]
                    object_url = f"https://song-artist-image.s3.amazonaws.com/{urllib.parse.quote(music_item['title'])}"
                    subs.append({'title': tle, 'artist': music_item['artist'], 'year': music_item['year'],
                                 'img_url': object_url})
    return subs
