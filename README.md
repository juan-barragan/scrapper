# Technical test creating a scrapper for enn.com
# Create a python virtual enviroenemnt
python3 -m venv .venv
# activate venv
source .venv/bin/activate
# Update pip
pip install -U pip
# install requirements using the requirements file
pip install -r requirements.txt
# Apply migrations
python manage.py makemigrations
python manage.py migrate
# populate the database by scrapping the site. The integer is the number of articles to scrap on each subject. (climate, energy, etc) by going to this url. Scrapping 20 articles
http://localhost:8000/scrap/20/
# Getting one article, you need to know the article id (the first number on the url)
http://localhost:8000/article/69137
# Get all articles talking about NASA. All keywords at the end separated by comma
http://localhost:8000/article/NASA/
