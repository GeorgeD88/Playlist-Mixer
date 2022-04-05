from spotipy_wrapper import SpotipyWrapper
from pprint import PrettyPrinter
from myutils import *
from sys import exit
from creds import *


""" Static playlist implementation of playlist mixing (but with equal ratios). """

spotify = SpotipyWrapper(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES)
pp = PrettyPrinter().pprint  # for dev purposes


print("For each playlist you'd like to combine, input a playlist link/ID for each line (enter nothing when finished):")
input_line = input()
playlists = []


# INPUT HANDLING ===
while input_line != '':
    # extracts ID if it's a link
    plist = input_line if input_line[:8] != 'https://' else input_line.split('/')[4].split('?')[0]

    # checks if playlist was already inputted
    if plist in playlists:
        print('\nThis playlist was already inputted\n')
        input_line = input()
        continue

    # puts the playlist and its respective ratio into the dict
    playlists.append(plist)

    input_line = input()

print('Resultant playlist')
plist_name = input('name: ')  # resultant playlist name
plist_length = int(input('length (may end up different): '))  # resultant playlist length
print("\nWorking on the playlist, this won't take long....\n")

# PLAYLIST CREATION ===
plist_tracks = set()
percentage = 1/len(playlists)
n_tracks = pround(plist_length * percentage)
found_names = []
for p_id in playlists:
    # gets a sample of tracks from the playlist
    p_tracks = spotify.random_playlist_tracks(p_id, n_tracks)

    plist_tracks.update(p_tracks)
    p_name = spotify.sp.playlist(p_id)['name']
    found_names.append(p_name)

plist_tracks = list(plist_tracks)
length = len(found_names)

# create playlist name if no playlist name was provided
if plist_name == '':
    plist_name = 'Songs from ' + (found_names[0] if len(found_names) == 1 else found_names[0] + ' and more')

# constructs playlist description
description = 'Songs pulled from playlist'
if length == 1:
    description += f' {found_names[0]}.'
elif length == 2:
    description += f's {found_names[0]} and {found_names[1]}.'
elif length > 5:
    description += 's ' + p_description(found_names[:5]) + 'and more.'
else:
    description += 's ' + p_description(found_names[:len(found_names)-1]) + f'and {found_names[-1]}.'

# creates playlist and returns new playlist ID
new_plist_id = spotify.new_playlist(plist_name, description=description)
spotify.add_playlist_tracks(new_plist_id, plist_tracks)
print('\nNew Playlist ID:\n' + new_plist_id)
print('\nResultant Percentage: {:.2f}%\n'.format(percentage*100))
# 4. Enjoy 😎
