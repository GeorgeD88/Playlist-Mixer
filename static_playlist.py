from spotipy_wrapper import SpotipyWrapper
from pprint import PrettyPrinter
from myutils import *
from sys import exit
from creds import *


""" Static playlist implementation of playlist mixing. """

spotify = SpotipyWrapper(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES)
pp = PrettyPrinter().pprint  # for dev purposes


print("For each playlist you'd like to combine, input a percentage (w/ no sign) and a playlist link/ID for each line (enter nothing when finished):")
input_line = input()
total_ratio = 0  # total ratio starts at 0 before input
playlists = {}


# INPUT HANDLING ===
while input_line != '':
    # split input into ratio and playlist and do input checking
    split_input = input_line.strip().split(' ')
    if len(split_input) != 2:
        print('\nInput needs to consist of a percentage and a playlist link/ID, separated by a space\n')
        input_line = input()
        continue

    # unpacks the and processes the inputs properly
    ratio, plist = float(split_input[0]), split_input[1] if split_input[1][:8] != 'https://' else split_input[1].split('/')[4].split('?')[0]

    # checks if playlist was already inputted
    if plist in playlists:
        print('\nThis playlist was already inputted\n')
        input_line = input()
        continue

    # adds ratio to total ratio and then exits if it exceeds 100%
    total_ratio += ratio
    if total_ratio > 100:
        exit(f'Total percentage cannot be more than 100%, you\'re at: {total_ratio}%')

    # puts the playlist and its respective ratio into the dict
    playlists[plist] = ratio * .01

    input_line = input()

# exits if total ratio isn't 100%
if total_ratio < 100:
    exit(f'Total percentage cannot be less than 100%, you ended up with: {total_ratio}%')

print('Resultant playlist')
plist_name = input('name: ')  # resultant playlist name
plist_length = int(input('length (may end up different): '))  # resultant playlist length
print("\nWorking on the playlist, this won't take long....\n")

# PLAYLIST CREATION ===
plist_tracks = set()
found_names = []
stats = '\nResultant Stats\n===============\n'
for p_id, percentage in playlists.items():
    # gets the number of tracks to be added from this playlist
    n_tracks = pround(plist_length * percentage)
    p_tracks = spotify.random_playlist_tracks(p_id, n_tracks)

    plist_tracks.update(p_tracks)
    p_name = spotify.sp.playlist(p_id)['name']
    calc_ratio = len(p_tracks)/plist_length
    stats += f'{p_name}: {calc_ratio}\n'
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
print(stats)
# 4. Enjoy 😎
