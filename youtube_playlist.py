import os
import urllib
import simplejson
from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import sys
import pprint
import time

def clean(test_str):
	ret = ''
	skip1c = 0
	skip2c = 0
	for i in test_str:
		if i == '[':
			skip1c += 1
		elif i == '(':
			skip2c += 1
		elif i == ']' and skip1c > 0:
			skip1c -= 1
		elif i == ')'and skip2c > 0:
			skip2c -= 1
		elif skip1c == 0 and skip2c == 0:
			ret += i
	return ret

def ftclean(test_str):
	result = test_str.find(' ft ')
	s=test_str
	if(result!=-1):
		s=test_str[:result]
	result = test_str.find(' ft. ')
	if(result!=-1):
		s=test_str[:result]
	result = test_str.find(' feat ')
	if(result!=-1):
		s=test_str[:result]
	result = test_str.find(' feat. ')
	if(result!=-1):
		s=test_str[:result]
	return s

api_key = "AIzaSyCHusgH9Vz0QV61OYUYzPFcffeiGMlJ-dc"
youtube = build('youtube', 'v3', developerKey=api_key)
yt_playlist_id = 'PLJN9d2tepI0VPLqzV9q04KuAV5GeSwnS6'

sp_playlist_id="34TIydgL7JbTMsTfS4jo6V"
clientid="a3d9594006d4407bb0b135260232cd43"
clientsecret="4c12cf04478a48038f3ee194ac18eed4"
redir="https://www.google.com/"
scope = 'playlist-modify-public, playlist-modify-private'

videos = []

nextPageToken = None
while True:
	pl_request = youtube.playlistItems().list(
		part='contentDetails',
		playlistId=yt_playlist_id,
		maxResults=10,
		pageToken=nextPageToken
	)

	pl_response = pl_request.execute()

	vid_ids = []
	for item in pl_response['items']:
		vid_ids.append(item['contentDetails']['videoId'])
	

	vid_request = youtube.videos().list(
		part="snippet",
		id=','.join(vid_ids)
	)

	vid_response = vid_request.execute()

	for item in vid_response['items']:
		vid_title = item['snippet']['title']

		# vid_id = item['id']
		# yt_link = f'https://youtu.be/{vid_id}'

		# videos.append(
		#     {
		#         'title': vid_title,
		#         'url': yt_link
		#     }
		# )

		videos.append(vid_title)

	nextPageToken = pl_response.get('nextPageToken')

	if not nextPageToken:
		break
# videos=list(reversed(videos))
print("videos- ",len(videos))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientid, client_secret=clientsecret, redirect_uri=redir,scope=scope))

track_ids=[]
i=0
for title in videos:
	# search_str = 'ARCHON (Prod. Noxygen)'
	print(i)
	i=i+1
	search_str=title
	result = sp.search(search_str, limit=1)
	if(result['tracks']['total']==0):
		search_str = ftclean(search_str)
		search_str = clean(search_str)
		result = sp.search(search_str, limit=1)
		if(result['tracks']['total']==0):
			search_str = search_str.replace('-','')
			search_str = search_str.replace(':','')
			result = sp.search(search_str, limit=1)
			if(result['tracks']['total']==0):
				continue
		# print(result)
		# print(result['tracks']['items'][0]['id'])
	track_ids.append(result['tracks']['items'][0]['id'])

print("track-ids ",len(track_ids))

n=len(track_ids)
print(track_ids[0])
# i=0
# gap=100
# while(True):
#     if(n<=0):
#         break
#     sp.playlist_add_items(sp_playlist_id, track_ids[i-gap:n])
#     i=i-gap
#     n=n-gap

i=0
while(i<n):
	track_id=[track_ids[i]]
	sp.playlist_add_items(sp_playlist_id, track_id)
	# time.sleep(2)
	i=i+1