FALT
====

Fresno Audiovisual Lexicon Tool

FALT is a tool to help investigate the similarities between audio-alone communication and visual-alone communication. 


![FALT SCREENSHOT](https://raw.githubusercontent.com/cameronbriar/FALT/master/comp1/static/cheese.png)


### To install (Debian):

    # Install required Python modules

    pip install django==1.4.2
    pip install python-Levenshtein

	# Get the FALT project
	git clone https://github.com/cameronbriar/FALT.git
	cd FALT

	# Fix `UPDATE_ROOT_DIRECTORY` variable in `FALT/settings.py` based on project directory location (e.g. `/home/user/FALT`)

	# Run the server
	python manage.py runserver 0.0.0.0:8000

    # Visit http://localhost:8000 in a browser
    # Click "About" to learn more
