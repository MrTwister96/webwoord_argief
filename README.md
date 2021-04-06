# Backend REST API for Covid Tracking App

# Readme from another repo - NEED TO UPDATE


## Requirements
- Python 3.7.5
- PIP 19.2.3

## Setup

Clone the repo
	
	git clone https://github.com/MrTwister96/webwoord_argief.git
	
Change to the directory
	
	cd webwoord_argief

Create the virtual environment
	
	python3 -m venv env
	
Activate the virtual environment (Windows)
	
	.\env\Scripts\activate
	
Install Requirements

	pip install -r requirements.txt

Run Migrations
	
	python3 manage.py makemigrations
	python3 manage.py migrate
	
Create a super user

	python3 manage.py createsuperuser
	
Start development server
	
	python3 manage.py runserver 0.0.0.0:8000
	
	Watching for file changes with StatReloader
	Performing system checks...

	System check identified no issues (0 silenced).
	March 16, 2021 - 22:28:42
	Django version 3.1.7, using settings 'webwoord.settings'
	Starting development server at http://0.0.0.0:8000/
	Quit the server with CTRL-BREAK.