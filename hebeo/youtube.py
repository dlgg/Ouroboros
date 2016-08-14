#!/usr/bin/python3
import isodate
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
    stats['user']     = ytData['items'][0]['snippet']['channelTitle'] if 'channelTitle' in ytData['items'][0]['snippet'] else 'No username'
    stats['title']    = ytData['items'][0]['snippet']['title'] if 'title' in ytData['items'][0]['snippet'] else 'No title'
    stats['duration'] = isodate.parse_duration(ytData['items'][0]['contentDetails']['duration']).total_seconds() if 'duration' in ytData['items'][0]['contentDetails'] else 0
    stats['view']     = ytData['items'][0]['statistics']['viewCount'] if 'viewCount' in ytData['items'][0]['statistics'] else 0
    stats['like']     = ytData['items'][0]['statistics']['likeCount'] if 'likeCount' in ytData['items'][0]['statistics'] else 0
    stats['dislike']  = ytData['items'][0]['statistics']['dislikeCount'] if 'dislikeCount' in ytData['items'][0]['statistics'] else 0
    return stats

