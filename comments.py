from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime


def get_youtube_comments(video_id, API_KEY, published_after=None, published_before=None):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    try:
        comments = []
        nextPageToken = None

        while True:
            response = youtube.commentThreads().list(
                part='snippet, replies',
                videoId=video_id,
                maxResults=100,
                pageToken=nextPageToken
            ).execute()

            for item in response['items']:
                # Get the top-level comment
                top_level_comment = item['snippet']['topLevelComment']['snippet']
                comment_text = top_level_comment['textDisplay']
                comment_date = datetime.strptime(top_level_comment['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')

                # Check if the comment falls within the specified time range
                if (not published_after or comment_date >= published_after) and \
                   (not published_before or comment_date <= published_before):
                    comments.append({'text': comment_text, 'date': comment_date})

                # Check if there are replies to the top-level comment
                if 'replies' in item.keys():
                    next_page_token = None
                    while True:
                        reply_response = youtube.comments().list(
                            part='snippet',
                            parentId=item['id'],
                            maxResults=100,
                            pageToken=next_page_token
                        ).execute()

                        for reply_item in reply_response['items']:
                            reply_text = reply_item['snippet']['textDisplay']
                            reply_date = datetime.strptime(reply_item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                            if (not published_after or reply_date >= published_after) and \
                               (not published_before or reply_date <= published_before):
                                comments.append({'text': reply_text, 'date': reply_date})

                        next_page_token = reply_response.get('nextPageToken')
                        if not next_page_token:
                            break

            nextPageToken = response.get('nextPageToken')
            if not nextPageToken:
                break

        return comments

    except HttpError as e:
        print('An error occurred:', e)
        return None
