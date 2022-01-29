# 必要なモジュールのimport
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


def main():
    '''
    メインの実行部分
    ツイートデータの取得からデータの出力まで
    '''
    
    # ツイートデータの取得
    data = get_search_tweet('Python', 100, 1)
    
    # ツイートデータを番号順に出力
    out_put_tweets(tweet_data)
    
    # ツイートデータをDataFrameにする
    df = make_df(tweet_data)

    # DataFrameの出力
    print(f"データフレーム{df}")
    
    # ツイートデータのCSVへの出力
    df.to_csv('tweet_data.csv')


def get_search_tweet(search_key, items_cnt, refav_cnt):
    '''
    ツイート情報を期間指定で収集
    取得できるのデータは直近1週間以内
    RT数＋いいね数の合計を超えるツイートを取得
    '''
    # ツイートデータ取得部分 start_time, end_timeの期間で取得
    response = client.search_recent_tweets(
        query=search_key,
        start_time = "2022-01-23T00:00:00Z",
        end_time="2022-01-27T00:00:00Z",
        expansions=["attachments.media_keys", "author_id"],
        tweet_fields=["created_at", "lang", "public_metrics"],
        media_fields=["preview_image_url"],
        since_id=sid,
        max_results=items_cnt,
    )

    tweets = response.data
    includes = response.includes
    users = includes["users"]

    # ツイートのデータを取り出して、リストにまとめていく部分
    tweet_data = []  # ツイートデータを入れる空のリストを用意
    for user, tweet in zip(users, tweets):
        # いいねとリツイートの合計がrefav_cnt以上の条件
        if tweet.public_metrics["like_count"] + tweet.public_metrics["retweet_count"] > refav_cnt:
            # 空のリストtweet_dataにユーザーネーム、スクリーンネーム、RT数、いいね数、日付などを入れる
            tweetd_data.append(user["name"], user, tweet.public_metrics["retweet_count"], tweet.public_metrics["like_count"],
                            tweet.public_metrics["quote_count"], tweet.created_at.astimezone(timezone('Asia/Tokyo')))
    return tweet_data


def out_put_tweets(tweet_data):
    '''
    ツイートのリストを順番をつけて出力する関数の作成
    '''
    for i in range(len(tweet_data)):
        print(f"{i} 番目{tweet_data[i]}")
        # ツイートデータ取得部分

def make_df(tweet_data):
    '''
    ツイートデーターからDataframeを作成する
    '''    
    # データを入れる空のリストを用意
    list_user_name = []
    list_user_id = []
    list_re_cnt = []
    list_fav_cnt = []
    list_quote_cnt = []
    list_date = []
    list_text = []
    
    # ツイートデータからユーザー名、ユーザーid、RT数、いいね数、日付け、ツイート本文のそれぞれをデータごとにまとめたリストを作る
    for i in range(len(data)):
        list_user_name.append(data[i][0])
        list_user_id.append(data([i][1]))
        list_re_cnt.append(data[i][2])
        list_fav_cnt.append(data[i][3])
        list_quote_cnt.append(data[i][4])
        list_date.append(data[i][5])
        list_text.append(data[i][6])
    
    # 先ほど作ったデータごとにまとめたリストからDataframeの作成
    df = DataFrame({'ユーザー名': list_user_name,
                    'ユーザーid': list_user_id,
                    'RT数': list_re_cnt,
                    'いいね数': list_fav_cnt,
                    '日時': list_date,
                    '本文': list_text})
    return df

# 実行部分
if __name__ == '__main__':
    main()

