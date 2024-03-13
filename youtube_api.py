# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json

import googleapiclient.discovery

#credentials for API connection
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyC5qLDyzBTptLyeIdg7yPnefnhbDycLAL4"


def get_current_video(Channel_ID,Channel_Name):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"



    #build API class using credentials
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    User_Id = Channel_ID

    #request latest video based upon channel ID
    request = youtube.search().list(
        part="snippet",
        channelId = User_Id.strip('"') ,
        maxResults=1,
        order="date"
    )
    try:
        response = request.execute()
    except googleapiclient.errors.HttpError:
        print("API Point Limit extended")
        exit()

    #Dumps the ID of the latest video into internal varable
    video_Id = json.dumps(response["items"][0]["id"]["videoId"]).strip('"')

    #print(video_Id)

    #create a dict for less confusing return and dumps everything into it.
    d = dict();
    d['Channel_Name'] = Channel_Name
    d['Channel_Id'] = User_Id
    d['latest_Video_Id'] = video_Id
    #print(d)
    return d


def get_video_metadata(Video_Id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


    #build API class using credentials
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)


    request = youtube.videos().list(
        part="snippet",
        id=Video_Id
    )
    try:
        response = request.execute()
    except googleapiclient.errors.HttpError:
        print("API Point Limit extended")
        exit()

    

    video_decription_title = json.dumps(response["items"][0]["snippet"]["title"]).strip('"')
        #create a dict for less confusing return and dumps everything into it.

    #print(d)
    return video_decription_title 



# this part is only needed for testing and bugfixing this shit
def main():
    #print(get_current_video("UCyHDQ5C6z1NDmJ4g6SerW8g","@maiLab"))
    print(get_video_metadata('GtBnj3Z3eO4'))
    

if __name__ == "__main__":
    main()