# Python Youtube Playlist CLI

A simple CLI with two useful functionalities not provided by youtube.

Allows for querying the **aggregate playtime** of all videos as well as **sorting playlist** according to **view count**.

## Technologies

### Stack
Project is created with: 
* python

### Packages
Project uses the following packages: 
* google-api-python-client
* python-dotenv
* typer

## Launch
All commands should be in the project directory

### Setup
Follow these steps to setup the script for first time use: 

    - run `python ytlist.py init`
    - provide your youtube api key at the prompt
    - success message means you're ready to go! (really wish i had used golang instead now)

### Commands
Commands take the list id of a playlist as an argument.
The list id can be found in the _list_ query string of all playlist urls
There are two commands available:  
  1. Playtime: 
     - Sums the play time of all videos in the playlist
     - run `python ytlist playtime --help` for details
  2. Popular: 
     - Displays a sorted list of all the videos in the playlist
     - run `python ytlist popular --help` for details
