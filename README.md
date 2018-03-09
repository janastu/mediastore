# Mediastore

Uses Python Flask framework, Github auth to store a stream of bytes and provide a simple URI to the stored stream. Currently only handles audio, but video support can be added as well.

# Run

Install in a virtual environment

  $ pip install -r requirements.txt


Copy mediastore/config_example.yaml to mediastore/config.yaml. Place corresponding keys to Github app in config file.

Run

  $ python main.py

# To-do

Dockerize the app so it can run on the server
