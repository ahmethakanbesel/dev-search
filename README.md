# GitHub Developer Search
It allows you to search for developers on GitHub and provides statistics about their GitHub profiles.

## Installing
### Install Required Packages
- Run `pip install -r requirements.txt`
### Configure Database
- It runs with PostgreSQL by default but you can change database options on `backend/settings.py`
- You may need to run `python manage.py makemigrations` and `python manage.py migrate`
### Configure GitHub Token
- It can run without GitHub access token but if you specify GitHub username and personal access token in `devsearch/settings.py` you will get higher rate limit.
You can create a personal access token here: https://github.com/settings/tokens

## Running
- Run `python manage.py runserver`
- Open http://localhost:8000/

## Preview
![Home Page](preview/homepage.png "Home Page")
*Home Page*

![Search Results](preview/search-results.png "Search Results")
*Search Results*

![Profile Detail](preview/profile-page.png "Profile Page")
*Profile Detail Page*

## Credits
- [Django](https://github.com/django/django)
- [Bootstrap](https://github.com/twbs/bootstrap)