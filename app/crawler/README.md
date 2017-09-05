# twitter-crawler twitter爬虫

## Core Code
- ./app/basicinfo_crawler: 抓取用户基础信息
- ./app/relation_crawler: 抓取用户关系信息
- ./app/tweets_crawler: 抓取用户推文信息

./crawler.py 、portrayal.py、 ./relation.py （测试使用）

## twitter 开发者API官方文档地址
[https://dev.twitter.com/overview/api](https://dev.twitter.com/overview/api)

## python-twitter官方教程
[https://python-twitter.readthedocs.io/en/latest/twitter.html](https://python-twitter.readthedocs.io/en/latest/twitter.html)

## 数据库字段含义

### 用户基础信息
- id: unique identifier for this User (用户ID)
- screen_name: String | The screen name, handle, or alias that this user identifies themselves with. screen_names are unique but subject to change(账号名称（唯一）)
- name: String | The name of the user, as they’ve defined it.(用户名称)
- created_at: String | The UTC datetime that the user account was created on Twitter.(加入日期)("Mon Nov 29 21:18:15 +0000 2010")
- description: String(Nullable) | The user-defined string describing their account (个人简介)
- followers_count: int | The number of followers this account currently has. Under certain conditions of duress, this field will temporarily indicate “0.”（粉丝数）
- friends_count: int | The number of users this account is following (AKA their “followings”). Under certain conditions of duress, this field will temporarily indicate “0.”(关注的人数)
- statuses_count: int | The number of tweets (including retweets) issued by the user(推文数)
- favourites_count: int | the number of tweets this user has favorited in the account’s lifetime(喜欢的推文数)
- location: String(Nullable) | The user-defined location for this account’s profile. Not necessarily a location nor parseable(居住地)
- lang: String | The BCP 47 code for the user’s self-declared user interface language. May or may not have anything to do with the content of their Tweets. (语言)
- protected: tinyint(0 or 1 => Boolean) | When 1, indicates that this user has chosen to protect their Tweets.
- time_zone: String(Nullable ) | A string describing the Time Zone this user declares themselves within(时区)
- verified: tinyint(0 or 1 => Boolean) | When 1, indicates that the user has a verified account(是否认证)
- default_profile_image: tinyint(0 or 1 => Boolean) | When 1, indicates that the user has not uploaded their own avatar and a default egg avatar is used instead.
- utc_offset: int(Nullable ) | The offset from GMT/UTC in seconds(协调世界时偏差(The offset from GMT/UTC in seconds.))
- geo_enabled: tinyint(0 or 1 => Boolean) | When 1, indicates that the user has enabled the possibility of geotagging their Tweets.(是否允许标识用户的地理位置)
- listed_count: int | The number of public lists that this user is a member of
- profile_background_color: String | The hexadecimal color chosen by the user for their background.
- profile_text_color: String | The hexadecimal color the user has chosen to display text with in their Twitter UI
- profile_sidebar_fill_color: String | The hexadecimal color the user has chosen to display sidebar backgrounds with in their Twitter UI
- is_translator: tinyint(0 or 1 => Boolean) | When 1, indicates that the user is a participant in Twitter’s translator community
- profile_image_url: String | A HTTPS-based URL pointing to the user’s avatar image(头像)

### 推文信息
- coordinates：Nullable Represents the geographic location of this Tweet as reported by the user or client application. The inner coordinates array is formatted as geoJSON (longitude first, then latitude).  
```python 
"coordinates":
{
    "coordinates":
    [
        -75.14310264,
        40.05701649
    ],
    "type":"Point"
}
```
- created_at：UTC time when this Tweet was created
- entities： Entities which have been parsed out of the text of the Tweet
```python
"entities":
{
    "hashtags":[],
    "urls":[],
    "user_mentions":[]
}
```
- favorite_count： Nullable Indicates approximately how many times this Tweet has been liked by Twitter users
- id：The integer representation of the unique identifier for this Tweet
- in_reply_to_screen_name：If the represented Tweet is a reply, this field will contain the screen name of the original Tweet’s author
- in_reply_to_user_id: If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s author ID. This will not necessarily always be the user directly mentioned in the Tweet
- in_reply_to_status_id：If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s ID.
- lang：When present, indicates a BCP 47 language identifier corresponding to the machine-detected language of the Tweet text, or und if no language could be detected.
- place：When present, indicates that the tweet is associated (but not necessarily originating from) a Place
```python
"place":
{
    "attributes":{},
     "bounding_box":
    {
        "coordinates":
        [[
                [-77.119759,38.791645],
                [-76.909393,38.791645],
                [-76.909393,38.995548],
                [-77.119759,38.995548]
        ]],
        "type":"Polygon"
    },
     "country":"United States",
     "country_code":"US",
     "full_name":"Washington, DC",
     "id":"01fbe706f872cb32",
     "name":"Washington",
     "place_type":"city",
     "url": "http://api.twitter.com/1/geo/id/01fbe706f872cb32.json"
}
```
- retweet_count：Number of times this Tweet has been retweeted. 
- source：Utility used to post the Tweet, as an HTML-formatted string. Tweets from the Twitter website have a source value of web.
- text: The actual UTF-8 text of the status update.