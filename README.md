# Playlist-Mixer
This project took less than 2 hours to program yet it solves a very real problem I've had. I wanted to make a playlist with mine and my friend's music once, so I combined a playlist from each of us. The only problem is my playlist was considerably larger so the resultant playlist ended up being mostly my songs. That's exactly what **Playlist Mixer** solves. Given some playlists, a new playlist is made combining equal percentages of each playlist (or custom percentages).<br>

## Running the script
There are 2 scripts that are exactly the same besides how they handle the percentages. `static_playlist.py` takes custom percentages for each playlist while `eq_static_playlist.py` takes an equal percentage of each playlist.

Once you run it, you will be asked which playlists (and percentage, depending on which script) you'd like songs from. You're also asked what you'd like the length and name of the resultant playlist to be. Once it finishes running, you'll have a new playlist in your library.<br><br>
**Below is an example run w/ custom percentages**<br>
For the custom percentages script, when you're taking percentages of a small number you will often end up with different percentages in the end. So for that script, the true percentages of the playlist will be printed at the end.<br>
<img align="left" src="https://github.com/GeorgeD88/Playlist-Mixer/blob/main/static_playlist_run.png" alt="Example program run" width="75%">
<br>
<img align="left" src="https://github.com/GeorgeD88/Playlist-Mixer/blob/main/static_playlist_result.png" alt="Resulting playlist" width="75%">