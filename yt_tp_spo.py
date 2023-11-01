from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyOAuth
import spotipy

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

def youtubePlaylistScan(yt_playlist_id, api_keyi):
	youtube = build('youtube', 'v3', developerKey=api_key)
	videos = []
	print("Reading Youtube playlist...")
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
			videos.append(vid_title)

		nextPageToken = pl_response.get('nextPageToken')

		if not nextPageToken:
			break

	print("Youtube videos in playlist: ",len(videos))
	return videos

def spotifyPlaylistAdd(sp_playlist_id, videos, clientid, clientsecret):
	redir="https://www.google.com/"
	scope = 'playlist-modify-public, playlist-modify-private'

	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientid, client_secret=clientsecret, redirect_uri=redir,scope=scope))

	print("Finding tracks on spotify...")
	track_ids=[]
	i=0
	for title in videos:
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
			
		track_ids.append(result['tracks']['items'][0]['id'])

	print("Tracks found on spotify: ",len(track_ids))

	n=len(track_ids)

	print("Adding tracks to spotify playlist...")
	for i in range(n):
		track_id=[track_ids[i]]
		sp.playlist_add_items(sp_playlist_id, track_id)
		# time.sleep(2)
	print("Tracks added.")

if __name__ == "__main__":
	api_key = ""
	yt_playlist_id = ''
	videos=youtubePlaylistScan(yt_playlist_id, api_key)

	clientid=""
	clientsecret=""
	sp_playlist_id=""
	spotifyPlaylistAdd(sp_playlist_id, videos, clientid, clientsecret)

