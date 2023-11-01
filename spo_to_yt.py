from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
from googleapiclient.discovery import build

def spotifyPlaylistScan(pl_id, clientid, clientsecret):
	redir="https://www.google.com/"
	scope = 'playlist-modify-public, playlist-modify-private'
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientid, client_secret=clientsecret, redirect_uri=redir,scope=scope))
	# sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
	print('Reading tracks from spotify playlist...')
	offset = 0
	tracks=[]
	while True:
		response = sp.playlist_items(pl_id,
									 offset=offset,
									 additional_types=['track'])
		
		if len(response['items']) == 0:
			break
		
		for item in response['items']:
			leadArtist = item['track']['artists'][0]['name']
			trackName = item['track']['name']
			name = trackName+' by '+ leadArtist
			tracks.append(name)
			# print(trackName,' by ', leadArtist)
			# if leadArtist=='pomodorosa':
			# 	pprint(item)
		offset = offset + len(response['items'])
		print(offset, "/", response['total'])
	return tracks

def youtubePlaylistAdd(yt_playlist_id, tracks, api_key):
	youtube = build('youtube', 'v3', developerKey=api_key)
	videoIds=[]
	print("Finding tracks on youtube...")
	i=0
	for track in tracks:
		request = youtube.search().list(
			part="snippet",
			q=track
		)
		response = request.execute()
		print(i)
		i=i+1
		for j in range(len(response['items']))
			if 'videoId' in response['items'][j]['id']:
				videoIds.append(response['items'][j]['id']['videoId'])
				break

	print("Adding tracks to Youtube playlist...")
	nextPageToken = None
	i=0
	for videoId in videoIds:
		i=i+1
		pl_request = youtube.playlistItems().insert(
			part='snippet',
			playlistId=yt_playlist_id,
			resourceId={'kind': 'youtube#video', 'videoId':videoId}
		)
		print(i)
		pl_response = pl_request.execute()

	print("Youtube videos added to playlist: ",len(videoIds))

if __name__ == "__main__":
	sp_playlist_id=""
	clientid=""
	clientsecret=""
	tracks = spotifyPlaylistScan(sp_playlist_id, clientid, clientsecret)

	yt_playlist_id = ''
	api_key = ""
	videos=youtubePlaylistAdd(yt_playlist_id, tracks, api_key)
	
