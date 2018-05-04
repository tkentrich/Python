#!/bin/env python

import os
import sqlite3
from ID3 import *

dbfile = '/home/richkent/Workspace/Python/library.db'
conn = sqlite3.connect(dbfile)

def selectAlbum(artistID):
    print "Select an album:"

def selectArtist():
    showartists()
    print "- - - - -"
    print "Select an artist"    
    
def showartists():
    cursor = conn.execute('SELECT oid, name FROM artist ORDER BY name')
    results = cursor.fetchall()
    for row in results:
        print '{0}) {1}'.format(row[0], row[1])
    
def showalbums():
    artistID = selectArtist()

def showtracks():
    artistID = selectArtist()
    albumID = selectAlbum(artistID)

def inputlibrary():
    print "Input Library"

def populatelibrary():
    response = raw_input("Enter mp3 root folder: ")
    tree = os.walk(response)
    try:
        (a, arts, a) = tree.next()
        for artist in arts:
            print "New artist ", artist
            (a, albs, a) = tree.next()
            for album in albs:
                print "   New album ", album
                (a, a, trks) = tree.next()
                for track in trks:
                    print "      New track ", track
            
    except StopIteration:
        print "Iteration stopped"

def mainmenu():
    done = False
    while not done:
        print "1) Show artists"
        print "2) Show an artist's albums"
        print "3) Show an album's tracks"
        print "4) Input library info"
        print "5) Populate library based on mp3s"
        print ""
        print "0) Quit"
        print ""
        response = int(input ("Enter choice: "))
        if response == 1:
            showartists()
        elif response == 2:
            showalbums()
        elif response == 3:
            showtracks()
        elif response == 4:
            inputlibrary()
        elif response == 5:
            populatelibrary()
        elif response == 0:
            done = True
        else:
            print "Invalid response:", response

    print "Good-Bye!"

mainmenu()
