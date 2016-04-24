#!/usr/bin/python3
import json
import sys
import os.path
import urllib.request

if os.path.exists('gdata.api'):
    f=open('gdata.api','r')
    API=f.read().strip()
    f.close()
else:
    print("File gdata doesn't exist. Please create it and insert your google API key in it.")
    sys.exit(1)

def ytVideoStats(videoid):
    ytUrl="https://www.googleapis.com/youtube/v3/videos?id="+videoid+"&key="+API+"&part=snippet,contentDetails,statistics"
    try:
        ytResp=urllib.request.urlopen(ytUrl).read()
    except urllib.error.HTTPError as e:
        print(e)
        sys.exit(1)
    except:
        print("Unexpected error: "+sys.exc_info()[0])
        sys.exit(2)
    ytData=json.loads(ytResp.decode("UTF-8"))
    stats = {}
    stats['link']     = "https://youtu.be/{}" + videoid
    stats['title']    = ytData['items'][0]['snippet']['title']
    stats['duration'] = ytData['items'][0]['contentDetails']['duration']
    stats['view']     = ytData['items'][0]['statistics']['viewCount']
    stats['like']     = ytData['items'][0]['statistics']['likeCount']
    stats['dislike']  = ytData['items'][0]['statistics']['dislikeCount']
    return stats

