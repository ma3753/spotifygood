"""
Created on Tue Mar  2 18:15:09 2021

@author: Ky
"""

# This is the coallessed form of everything here
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
from datetime import date
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

albumPraise = [
    "Great album!",
    "Solid album choice!",
    "Very nice album!",
    "Nice album!",
    "Sick album!",
    "Wow, now thats an album!",
    "This album is awesome!",
    "Solid album!"
]

generalPraise = [
    "Way To Go!",
    "Terrific!",
    "Marvelous!",
    "Bravo!",
    "Wonderful!",
    "Outstanding!",
    "Breathtaking!",
    "Well done!",
    "You go the extra mile!",
    "Wow!",
    "Spectacular!",
    "Sweet!",
    "Im impressed!",
    "You've earned my respect!",
    "Clever!",
    "Neat Work!",
    "I Like It!",
    "Lovely!",
    "Incredible!",
    "You Rock!",
    "Nice one!",
    "Very talented!",
    "Thats perfect!",
    "Great discovery!",
    "5 Stars to you!",
    "Remarkable!"
]


def getRandomPraise(typeOf):
    if typeOf == "A":
        return random.choice(albumPraise)
    else:
        return random.choice(generalPraise)


def years_between(years,
                  from_date=None):  # Function to determine years between date time - Credit: https://stackoverflow.com/questions/765797/python-timedelta-in-years, Modified by Austin Kottoor
    if from_date is None:
        from_date = datetime.datetime.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!

        return from_date.replace(month=2, day=28,
                                 year=from_date.year - years)


def testMain(uri):
    cid = '90f812db7c0349c28c19c4e28c512512'
    secret = '465acc7e919a4b1dbe6a019f668329ca'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    user = 'kymc22'
    # kymc22
    # spotify:playlist:1egw8xpMnqXBsVPVBzdGMH
    playlist_uri = 'spotify:playlist:1egw8xpMnqXBsVPVBzdGMH'

    if uri["search"] != "" and uri["search"] != "None":  # GET SEARCH
        playlist_uri = uri["search"]

    result = sp.playlist(playlist_uri)
    tracks = result['tracks']
    items = tracks['items']
    playName = result["name"]

    final_list = []
    song_popularity_max = 60
    artist_popularity_max = None
    artist_followers_max = 150000

    file = open(BASE_DIR / "spotipyStuff/albums.txt", "r")
    acclaimList = file.read().split("\n")

    my_seed_tracks = []

    context = {
        "search": uri["search"],
    }

    data3Data = []
    data2Data = []
    data1Data = []

    recommendationsData = []

    for i in range(len(items)):
        track = items[i]
        song = track['track']
        uri = song['uri']
        song_popularity = song['popularity']  # 0-100
        song_name = song['name']
        album = song['album']
        album_name = album['name']

        artist = song['artists'][0]
        artist_name = artist['name']
        artist_uri = artist['uri']
        artist_data = sp.artist(artist_uri)
        artist_popularity = artist_data['popularity']
        artist_followers = artist_data['followers']['total']

        song_data_list = [song_name, album_name, artist_name]

        rDate = str(album["release_date"]).split("-")  # store release date
        today = str(date.today()).split("-")  # Get todays date
        yDif = int(today[0]) - int(rDate[0])

        my_seed_tracks.append(uri)
        if song_popularity < song_popularity_max and artist_followers < artist_followers_max:
            final_list.append(song_data_list)

        if album_name in acclaimList:
            data2Data.append(getRandomPraise('A') + " " + album_name + " won a Grammy! Great album!")

        if len(rDate) > 1 and yDif != 1:
            mDif = yDif * 12 + int(rDate[1]) - int(today[1])

        elif yDif == 1 and len(rDate) > 1:
            mDif = 12 - int(rDate[1])
        else:
            mDif = 12

        if mDif < 0:
            mDif = 1

        if yDif > 20:
            data3Data.append((getRandomPraise("B") + " {} was released over {} years ago!".format(song_name, yDif)))
        if mDif < 3:
            data3Data.append((getRandomPraise("B") + " {} was just released, only {} months ago!".format(song_name, mDif)))

    data2Data.append("Nice! " + str(len(final_list)) + " of your songs are by non-mainstream artists.")

    for i in range(int(len(final_list) / 3)):
        if len(final_list) > 0:
            song = final_list[random.randrange(0, len(final_list) - 1)]
            data1Data.append(getRandomPraise("B") + " This song is really obscure! You Found a diamond in the ruff! " + song[0] + " by " + song[2])

            recommendationsData.append('<tr><th scope="row">' + song[2] + '</th><td>' + song[0] + '</td><td><a href="#" class="btn btn-light"><svg class="svg-inline--fa fa-thumbs-up fa-w-16" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="thumbs-up" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" data-fa-i2svg=""><path fill="currentColor" d="M104 224H24c-13.255 0-24 10.745-24 24v240c0 13.255 10.745 24 24 24h80c13.255 0 24-10.745 24-24V248c0-13.255-10.745-24-24-24zM64 472c-13.255 0-24-10.745-24-24s10.745-24 24-24 24 10.745 24 24-10.745 24-24 24zM384 81.452c0 42.416-25.97 66.208-33.277 94.548h101.723c33.397 0 59.397 27.746 59.553 58.098.084 17.938-7.546 37.249-19.439 49.197l-.11.11c9.836 23.337 8.237 56.037-9.308 79.469 8.681 25.895-.069 57.704-16.382 74.757 4.298 17.598 2.244 32.575-6.148 44.632C440.202 511.587 389.616 512 346.839 512l-2.845-.001c-48.287-.017-87.806-17.598-119.56-31.725-15.957-7.099-36.821-15.887-52.651-16.178-6.54-.12-11.783-5.457-11.783-11.998v-213.77c0-3.2 1.282-6.271 3.558-8.521 39.614-39.144 56.648-80.587 89.117-113.111 14.804-14.832 20.188-37.236 25.393-58.902C282.515 39.293 291.817 0 312 0c24 0 72 8 72 81.452z"></path></svg></a> <a href="#" class="btn btn-danger"><svg class="svg-inline--fa fa-thumbs-up fa-w-16" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="thumbs-up" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" data-fa-i2svg=""><path fill="currentColor" d="M104 224H24c-13.255 0-24 10.745-24 24v240c0 13.255 10.745 24 24 24h80c13.255 0 24-10.745 24-24V248c0-13.255-10.745-24-24-24zM64 472c-13.255 0-24-10.745-24-24s10.745-24 24-24 24 10.745 24 24-10.745 24-24 24zM384 81.452c0 42.416-25.97 66.208-33.277 94.548h101.723c33.397 0 59.397 27.746 59.553 58.098.084 17.938-7.546 37.249-19.439 49.197l-.11.11c9.836 23.337 8.237 56.037-9.308 79.469 8.681 25.895-.069 57.704-16.382 74.757 4.298 17.598 2.244 32.575-6.148 44.632C440.202 511.587 389.616 512 346.839 512l-2.845-.001c-48.287-.017-87.806-17.598-119.56-31.725-15.957-7.099-36.821-15.887-52.651-16.178-6.54-.12-11.783-5.457-11.783-11.998v-213.77c0-3.2 1.282-6.271 3.558-8.521 39.614-39.144 56.648-80.587 89.117-113.111 14.804-14.832 20.188-37.236 25.393-58.902C282.515 39.293 291.817 0 312 0c24 0 72 8 72 81.452z"></path></svg></a></td></tr>')

    data3String = ""

    for x in data3Data:
        data3String = "{}{}{}".format(data3String, x, "<br><br>")

    data2String = ""

    for x in data2Data:
        data2String = "{}{}{}".format(data2String, x, "<br><br>")

    data1String = ""

    for x in data1Data:
        data1String = "{}{}{}".format(data1String, x, "<br><br>")

    recommendationsDataString = ""

    for x in recommendationsData:
        recommendationsDataString = "{}{}{}".format(recommendationsDataString, x, "")

    context["data4"] = recommendationsDataString
    context['data3'] = data3String
    context['data2'] = data2String
    context['data1'] = data1String
    context["unique"] = "Your playlist is " + str(round(100.0*len(final_list)/len(items), 1)) + "% obscure."
    context["uniquenum"] = round(100.0*len(final_list)/len(items), 1)
    context["playlistName"] = playName


    return context
