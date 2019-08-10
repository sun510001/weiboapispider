from weibopy3 import APIClient
import csv
from pathlib import Path
import re
import urllib.request
import webbrowser
import time


def access_token_fac():
    key_list = []
    CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'

    check_key_path = Path("/home/sun/Code/weibo-api-update/WeiboTestProgram/key.txt")
    if check_key_path.exists():
        with open('/home/sun/Code/weibo-api-update/WeiboTestProgram/key.txt', 'r') as f_key:
            # scan the file
            for line in f_key.readlines():
                if len(line.strip()) != 0:
                    key_list.append(line.strip())
            # deal with key_list
        len_key = len(key_list)
        print(key_list, len_key)
    else:
        len_key = 0

    if len_key == 4:
        APP_KEY = key_list[0]
        APP_SECRET = key_list[1]
        access_token = key_list[2]
        expires = key_list[3]

        client = APIClient(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            redirect_uri=CALLBACK_URL)
        client.set_access_token(access_token, expires)
    else:
        APP_KEY = input("Please input APP_KEY: ")
        APP_SECRET = input("Please input APP_SECRET: ")
        client = APIClient(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            redirect_uri=CALLBACK_URL)

        url = client.get_authorize_url()
        print(url)
        webbrowser.open_new(url)
        print("Please input the code of weibo from the browser URL bar")
        code = input("(eg:https://api.weibo.com/...?code=xxxxxxxxxxx): ")
        r = client.request_access_token(code)
        print("access_token --> ", r.access_token)
        print("expires --> ", r.expires_in)
        client.set_access_token(r.access_token, r.expires_in)
        with open('/home/sun/Code/weibo-api-update/WeiboTestProgram/key.txt', 'w') as w_key:
            w_key.write(APP_KEY + '\n')
        with open('/home/sun/Code/weibo-api-update/WeiboTestProgram/key.txt', 'a') as a_key:
            a_key.write(APP_SECRET + '\n')
            a_key.write(str(r.access_token) + '\n')
            a_key.write(str(r.expires_in) + '\n')

    statuses = client.get.statuses__home_timeline()['statuses']
    #  statuses = client.get.statuses__user_timeline()['statuses']
    length = len(statuses)
    print(length)
    return statuses, length


def split_tweet(retweets):
    # split urls from str and change short url to long url.
    split_tweets = re.split(r'( |;|\n|\s|view:)', retweets)
    for j in range(0, len(split_tweets)):
        #  print(j, " : ", split_tweets[j])
        if re.match('http', split_tweets[j]):
            # change short_url to long_url
            try:
                res = urllib.request.urlopen(split_tweets[j], timeout=600)
                print("---->", res.geturl())
                split_tweets[j] = res.geturl()
            except BaseException:
                pass

    retweets_url_changed = ''.join(split_tweets)
    print("Retweeter : ", retweets_url_changed)
    #  print all info
    add_info2 = (statuses[i]['id'], statuses[i]['created_at'][0:19],
                 statuses[i]['user']['screen_name'], retweets_url_changed)
    return add_info2


def split_pic(pic_urlstr):
    #  try:
    a = 0
    b = 0
    pic_url_small1 = []
    pic_url_small2 = []
    pic_url = re.split(r'(/|\.|}|\')', str(pic_urlstr))
    for i in range(0, len(pic_url)):
        # 'large'->large pic, 'thumbnail'->small pic
        if re.match('http', pic_url[i]):
            a = i
        elif re.match('thumbnail', pic_url[i]):
            pic_url[i] = 'large'
        elif re.match(r'(jpg|gif|png|jpeg)', pic_url[i]):
            b = i
        if a != 0:
            if i <= 15:
                # http://wx3.sinaimg.cn/
                pic_url_small1.append(pic_url[i])
            elif i > 16:
                # jump 'thumbnail'
                # /007nhdaVgy1fx24tebfu0j30dc09xjty.jpg
                pic_url_small2.append(pic_url[i])
        if b != 0:
            break
    return (''.join(pic_url_small1), ''.join(pic_url_small2))


def read_origin_csv():
    # check if weibo.csv exist
    my_path = Path("/home/sun/Code/weibo-api-update/sun510001.github.io/weibo.csv")
    if not my_path.exists():
        with open('/home/sun/Code/weibo-api-update/sun510001.github.io/weibo.csv', 'w') as csvf:
            fileHeader = [
                'id',
                'created_at',
                'screen_name',
                'tweet',
                'pic1a',
                'pic1b',
                'pic2a',
                'pic2b',
                'pic3a',
                'pic3b',
                'pic4a',
                'pic4b',
                'pic5a',
                'pic5b',
                'pic6a',
                'pic6b',
                'pic7a',
                'pic7b',
                'pic8a',
                'pic8b',
                'pic9a',
                'pic9b']
            writer = csv.writer(csvf)
            writer.writerow(fileHeader)
        colflag2 = 0
    else:   # find the last id number column
        with open('/home/sun/Code/weibo-api-update/sun510001.github.io/weibo.csv', 'r') as csvf:
            f = csv.DictReader(csvf)
            try:
                column = [row['id'] for row in f]
                colflag2 = int(column[len(column) - 1])
            except BaseException:
                colflag2 = 0
                pass
    return colflag2


def check_flag():
    # check the stop_flag:
    check_stop_flag_file = Path('/home/sun/Code/weibo-api-update/WeiboTestProgram/stop_flag.txt')
    if check_stop_flag_file.exists():
        with open('/home/sun/Code/weibo-api-update/WeiboTestProgram/stop_flag.txt', 'r') as f_stop:
            stop_flag = f_stop.read()
            print(stop_flag)
        if not stop_flag == 'False':
            pass
        elif stop_flag == 'True':
            time.sleep(300)
            pass
        else:
            with open('/home/sun/Code/weibo-api-update/WeiboTestProgram/stop_flag.txt', 'w') as w_stop:
                w_stop.write('False')
    else:
        with open('/home/sun/Code/weibo-api-update/WeiboTestProgram/stop_flag.txt', 'w') as w_stop:
            w_stop.write('False')


if __name__ == '__main__':
    stop_flag = False
    while True:
        if not stop_flag:
            colflag = read_origin_csv()
            statuses, length = access_token_fac()

            # deal with all tweets catched
            for i in range(length - 1, -1, -1):
                if statuses[i]['id'] > colflag:

                    #  print this tweeter's text
                    retweeter = statuses[i]['text']

                    # if this is a retweet
                    if statuses[i].get('retweeted_status'):
                        retweeter = ''.join(
                            r"\RT@{0}:{1}".format(
                                statuses[i]['retweeted_status']['user']['screen_name'],
                                statuses[i]['retweeted_status']['text']))

                    add_info = []
                    add_info = list(split_tweet(retweeter))

                    pic = statuses[i]['pic_urls']
                    for k in range(0, len(pic)):
                        pic_a, pic_b = split_pic(pic[k])
                        print(pic_a)
                        print(pic_b)
                        add_info.append(pic_a)
                        add_info.append(pic_b)
                    # add tweets contexts finally
                    with open('/home/sun/Code/weibo-api-update/sun510001.github.io/weibo.csv', 'a') as csvfw:
                        writer = csv.writer(csvfw)
                        writer.writerow(add_info)
                        dictf_if = csv.DictReader(csvfw)
            check_flag()
        else:
            check_flag()
            pass
        time.sleep(60)

        # print all tweets in the weibo.csv for test
        #  with open('weibo.csv', 'r') as csvr:
        #  fr = csv.DictReader(csvr)
        #  for each in fr:
        #  print(each)
