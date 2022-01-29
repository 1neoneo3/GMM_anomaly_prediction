import sys
import pandas as pd
import tweepy
from pytz import timezone
import config

# APIキーのセット
consumer_key = config.CK
consumer_secret = config.CS
access_token = config.AT
access_token_secret = config.AT
bearer_token = config.BT

client = tweepy.Client(
    bearer_token, consumer_key, consumer_secret, access_token, access_token_secret
)

search_key = "デイトラ"
id_list = []

# def get_search_tweet(search_key, )
print('リクエストを送信')
response = client.search_recent_tweets(
    query=search_key, # query= で検索するキーワードをセット
    start_time = "2022-01-25T00:00:00Z", # start_time= で検索期間の開始日時を設定
    end_time="2022-01-27T00:00:00Z", # end_time= で検索期間の終了日時を設定
    expansions=["attachments.media_keys", "author_id"], # 
    tweet_fields=["created_at", "lang", "public_metrics"], # tweet_fieldsで追加のツイート情報を取得
    media_fields=["preview_image_url"], # media_fieldsでメディア情報を取得
    max_results=100, # ツイートの取得数。最大で100
)

# print(response)
tweets = response.data
includes = response.includes
users = includes["users"]

tweet_data = []

print('ループ処理開始')
# ツイートの出力の確認
for user, tweet in zip(users, tweets):
    if tweet.public_metrics["like_count"] + tweet.public_metrics["retweet_count"] > 3:
        print(user["name"])
        print(user)
        print(tweet.text)
        print("いいね数: ", tweet.public_metrics["like_count"])
        print("引用数: ", tweet.public_metrics["quote_count"])
        print("リツイート数: ", tweet.public_metrics["retweet_count"])
        print(tweet.created_at.astimezone(timezone('Asia/Tokyo')))
        print("======================================================")
        sys.exit(0)
        
