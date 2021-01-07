#!/bin/bash

if [ ! -f /src/db/notes.db ]; then
	cp notes-empty.db /src/db/notes.db
fi

export CARDS_SETTINGS=/src/config.txt
gunicorn --bind  0.0.0.0:$PORT mainApp:app
