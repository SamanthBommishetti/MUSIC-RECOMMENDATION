#!/usr/bin/env python
# coding: utf-8

# In[11]:


import streamlit as st
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Load the preprocessed data and similarity matrix
df = pickle.load(open('songs_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(genre, song_name):
    search_query = f"track:{song_name} genre:{genre}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Function to get recommendations based on song name
def get_recommendations(song_name):
    # Get the index of the song
    song_index = df[df['song_name'] == song_name].index[0]

    # Get the pairwise similarity scores with other songs
    sim_scores = list(enumerate(similarity[song_index].toarray()[0]))

    # Sort the songs based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 similar songs (excluding the input song itself)
    sim_scores = sim_scores[1:6]

    # Get the indices of the similar songs
    song_indices = [score[0] for score in sim_scores]

    # Return the names of the similar songs
    return df['song_name'].iloc[song_indices]

# Streamlit app
def main():
    st.title("Song Recommendations App")

    # User input: Select genre
    selected_genre = st.selectbox("Select a genre:", df['genre'].unique())

    # Filter songs based on selected genre
    genre_songs = df[df['genre'] == selected_genre]

    # User input: Select song
    selected_song = st.selectbox("Select a song:", genre_songs['song_name'].unique())

    # Display selected song and album cover
    st.write(f"Selected Song: {selected_song}")
    album_cover_url = get_song_album_cover_url(selected_genre, selected_song)
    st.image(album_cover_url, caption=f"Album Cover for {selected_song}", use_column_width=True)

    # Display song recommendations
    st.header("Song Recommendations:")
    recommendations = get_recommendations(selected_song)
    st.write(recommendations)

if __name__ == "__main__":
    main()







