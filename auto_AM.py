import tweepy
import time
import datetime

API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


my_screen_name = ""

word_list = [""]
word_num = 0

result_mode = ["popular", "recent", "mixed"]
result_num = 1

set_count = 40

sleep_time = 60

favorite_flag = True
rt_flag = False
follow_flag = False

results = api.search(q = word_list[word_num], count = set_count, result_type = result_mode[result_num], exclude_replies = True, include_rts = False)

def main():
    for result in results:

        username = result.user._json['screen_name']

        tweet_id = result.id
        text = result.text


        if(text[0]=="R" and text[1]=="T"):

            tmp = text.split("@")[1]
            username = tmp.split(":")[0]
            tweet_id = result.retweeted_status.id
            if(username == my_screen_name):
                continue

        try:
            if(favorite_flag == True):
                api.create_favorite(tweet_id)
                print("いいね ", end="")
        except Exception as e:
            error_code = int(str(e).split(",")[0].split(":")[1])
            if(error_code == 139):
                print("いいね済み ", end="")
            else:
                print(e)

        try:

            if(rt_flag == True):
                api.retweet(tweet_id)
                print("RT ", end="")
        except Exception as e:
            error_code = int(str(e).split(",")[0].split(":")[1])
            if(error_code == 327):
                print("RT済み ", end="")
            else:
                print(e)

        try:

            if(follow_flag == True):
                following = api.show_friendship(source_screen_name = my_screen_name, target_screen_name = username)[0]._json['following']
                if(following == False):
                    api.create_friendship(username)
                    print("フォロー")
                else:
                    print("フォロー済み")
        except Exception as e:
            print(e)

        time.sleep(sleep_time)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
