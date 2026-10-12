# Train Your AI

## Description

An application that allows the user to train their own AI to play the game snake. This project is part of a research project at UTSA to help increase AI education an AI literacy among middle schoolers. 

__Authors: Cesar Hinojosa and Priyanka Kumar with small macOS compatibility edits from Olivia Buchanan__

## Running Instructions

Linux and macOS: 
* clone the repository
* create a python virtual environment inside the project directory: $ python -m venv venv
* $ pip install -r dependencies.txt
* run the app: $ python main.py      
* open http://localhost:5001 in a web browser

Windows:
* clone the repository
* create a python virtual environment inside the project directory: $ python -m venv venv
* $ pip install -r dependencies.txt
* add "allow_unsafe_werkzeug=True" to socketio.run() inside main.py, so it reads: socketio.run(app, port=5001, allow_unsafe_werkzeug=True)
* install aka.ms/vs/16/release/vc_redist.x64.exe (type url into web browser to install)
* run the app: $ python main.py
* open http://localhost:5001 in a web browser

## A Note on the Port

The app serves on port 5001, set by socketio.run(app, port=5001) in main.py. Flask's default port 5000 is unusable on macOS: Control Center's AirPlay Receiver already listens on it (on both IPv4 and IPv6) and answers with an empty 403, so the page looks like it failed to load while the app itself is running fine. Change the port argument in main.py if 5001 is taken on your machine.
