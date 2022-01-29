import pandas as pd
import tweepy
from pytz import timezone
import config
from output_log import Logging

# APIキーのセット
class TweetSearch:
    def __init__(self):
        self.consumer_key = config.CK
        self.consumer_secret = config.CS
        self.access_token = config.AT
        self.access_token_secret = config.AT
        self.bearer_token = config.BT

    def client(self):
        return tweepy.Client(
            self.bearer_token,
            self.consumer_key,
            self.consumer_secret,
            self.access_token,
            self.access_token_secret,
        )

    def get_recent_tweet(self, client, key, start, end, max_results):

        # def get_search_tweet(search_key, )

        return client.search_recent_tweets(
            query=key,
            start_time=start,
            end_time=end,
            expansions=["attachments.media_keys", "author_id"],
            tweet_fields=["created_at", "lang", "public_metrics"],
            media_fields=["preview_image_url"],
            max_results=max_results,
        )

    def out_tweet(self, users, tweets, max_cnt) -> None:
        """
        out put tweets,
        tweets = response.data,
        users = includes["users"]
        """
        # ツイートの出力の確認
        for user, tweet in zip(users, tweets):
            if (
                tweet.public_metrics["like_count"]
                + tweet.public_metrics["retweet_count"]
                > max_cnt
            ):
                print(
                    f'{user["name"]}\n'
                    "{0}\n"
                    "{1}\n"
                    "いいね数: {2}\n"
                    "引用数: {3}\n"
                    "リツイート数: {4}\n"
                    "{5}\n"
                    "{6}".format(
                        user,
                        tweet.text,
                        tweet.public_metrics["like_count"],
                        tweet.public_metrics["quote_count"],
                        tweet.public_metrics["retweet_count"],
                        tweet.created_at.astimezone(timezone("Asia/Tokyo")).replace(
                            tzinfo=None
                        ),
                        # tweet.created_at.replace(tzinfo=None),
                        "====================================",
                    )
                )


if __name__ == "__main__":
    logger = Logging(__file__, isTest=True)
    # log = logger._get_module_logger(__file__,True)
    logger.info_log("テストスタート")
    twitter = TweetSearch()
    client = twitter.client()
    logger.info_log("ツイート情報取得")
    response = twitter.get_recent_tweet(
        client, "デイトラ", "2022-01-23T00:00:00Z", "2022-01-25T00:00:00Z", 10
    )
    tweets = response.data
    includes = response.includes
    users = includes["users"]
    logger.info_log("ツイート出力")
    twitter.out_tweet(users, tweets, 10)
    logger.info_log("出力終了")
