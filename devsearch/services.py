import json
import os
from datetime import datetime, timedelta
import urllib.parse
from hashlib import sha256
from os import path

import requests

from devsearch.models import Developer, Repository, RepositoryTopic
import devsearch.settings as settings


def cache_valid(digest: str, days=1):
    cache_path = 'devsearch/cache/' + digest + '.json'
    if path.exists(cache_path):
        import datetime
        today = datetime.datetime.today()
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(cache_path))
        duration = today - modified_date
        if duration.days < days:
            return True
    return False


def search_on_github(keyword: str, page: int, per_page=15):
    params = {'q': keyword, 'page': page, 'per_page': per_page}
    # check cache.json exists
    digest = sha256(json.dumps(params, sort_keys=True).encode('utf8')).hexdigest()
    print(digest)
    if cache_valid(digest):
        with open('devsearch/cache/' + digest + '.json') as f:
            data = json.load(f)
            return data
    else:
        url = "https://api.github.com/search/users?" + urllib.parse.urlencode(params)
        if settings.GITHUB_USERNAME and settings.GITHUB_PERSONAL_ACCESS_TOKEN:
            response = requests.request("GET", url,
                                        auth=(settings.GITHUB_USERNAME, settings.GITHUB_PERSONAL_ACCESS_TOKEN))
        else:
            response = requests.request("GET", url)
        data = response.json()
        i = 0
        if 'items' in data:
            for user in data['items']:
                data['items'][i] = get_user(user['login'])
                if 'login' in user:
                    save_user(data['items'][i])
                i += 1
            with open('devsearch/cache/' + digest + '.json', 'w') as f:
                json.dump(data, f)
        return data


def get_user_data(username: str):
    url = "https://api.github.com/users/" + username
    if settings.GITHUB_USERNAME and settings.GITHUB_PERSONAL_ACCESS_TOKEN:
        response = requests.request("GET", url, auth=(settings.GITHUB_USERNAME, settings.GITHUB_PERSONAL_ACCESS_TOKEN))
    else:
        response = requests.request("GET", url)
    data = response.json()
    return data


def get_user_repositories(username: str, per_page=10, sort='pushed'):
    params = {'per_page': per_page, 'sort': sort}
    url = "https://api.github.com/users/" + username + "/repos?" + urllib.parse.urlencode(params)
    if settings.GITHUB_USERNAME and settings.GITHUB_PERSONAL_ACCESS_TOKEN:
        response = requests.request("GET", url, auth=(settings.GITHUB_USERNAME, settings.GITHUB_PERSONAL_ACCESS_TOKEN))
    else:
        response = requests.request("GET", url)
    data = response.json()
    return data


def get_user(username: str):
    user = get_user_data(username)
    user['repositories'] = get_user_repositories(username)
    return user


def save_user(developer):
    time_threshold = datetime.now() - timedelta(days=30)
    if not Developer.objects.filter(username=developer['login']).exists() or Developer.objects.filter(
            username=developer['login'], updated_at__lt=time_threshold).exists():
        # save to database
        dev = Developer.objects.create(
            name=developer['name'],
            username=developer['login'],
            bio=developer['bio'],
            email=developer['email'],
            company=developer['company'],
            location=developer['location'],
            website=developer['blog'],
            twitter=developer['twitter_username'],
            avatar=developer['avatar_url'],
            followers=developer['followers'],
            following=developer['following'],
            repositories=developer['public_repos']
        )
        for repo in developer['repositories']:
            if not Repository.objects.filter(name=repo['name'], owner=dev.id).exists():
                Repository.objects.create(
                    owner=dev,
                    name=repo['name'],
                    description=repo['description'],
                    stars=repo['stargazers_count'],
                    forks=repo['forks_count'],
                    language=repo['language'],
                    has_wiki=repo['has_wiki'],
                    has_issues=repo['has_issues'],
                    has_projects=repo['has_projects'],
                    license=repo['license']['name'] if repo['license'] else None,
                    last_push=repo['pushed_at']
                )


def save_to_database(developer_data):
    time_threshold = datetime.now() - timedelta(days=30)
    for developer in developer_data:
        if not Developer.objects.filter(username=developer['login']).exists() or Developer.objects.get(
                username=developer['login'], updated_at__lt=time_threshold):
            # save to database
            Developer.objects.create(
                name=developer['name'],
                username=developer['login'],
                bio=developer['bio'],
                email=developer['email'],
                company=developer['company'],
                location=developer['location'],
                website=developer['blog'],
                avatar=developer['avatar_url'],
                followers=developer['followers'],
                following=developer['following'],
                repositories=developer['public_repos']
            )
