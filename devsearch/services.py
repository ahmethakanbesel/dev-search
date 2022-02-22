from datetime import datetime, timedelta
import urllib.parse

import requests

from devsearch.models import Developer, Repository, RepositoryTopic


def search_on_github(keyword: str, page: int, per_page=40):
    params = {'q': keyword, 'page': page, 'per_page': per_page}
    url = "https://api.github.com/search/users?" + urllib.parse.urlencode(params)
    response = requests.request("GET", url)
    data = response.json()
    return data


def get_user_data(username: str):
    url = "https://api.github.com/search/users/" + username
    response = requests.request("GET", url)
    data = response.json()
    return data


def get_user_repositories(username: str, per_page=10, sort='pushed'):
    params = {'per_page': per_page, 'sort': sort}
    url = "https://api.github.com/users/" + username + "/repos?" + urllib.parse.urlencode(params)
    response = requests.request("GET", url)
    data = response.json()
    return data


def get_user(username: str):
    user = get_user_data(username)
    user['repositories'] = get_user_repositories(username)
    return user


def save_user(developer):
    if not Developer.objects.filter(username=developer['login']).exists() or Developer.objects.get(
            username=developer['login']).updated_at < datetime.now() - datetime.timedelta(days=30):
        # save to database
        dev = Developer.objects.create(
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
        for repo in developer['repositories']:
            if not Repository.objects.filter(name=repo['name'], owner=dev.id).exists():
                Repository.objects.create(
                    owner=dev.id,
                    name=repo['name'],
                    description=repo['description'],
                    stars=repo['stargazers_count'],
                    forks=repo['forks_count'],
                    language=repo['language'],
                    has_wiki=repo['has_wiki'],
                    has_issues=repo['has_issues'],
                    has_projects=repo['has_projects'],
                    license=repo['license']['name'],
                    last_push=repo['pushed_at']
                )


def save_to_database(developer_data):
    for developer in developer_data:
        if not Developer.objects.filter(username=developer['login']).exists() or Developer.objects.get(
                username=developer['login']).updated_at < datetime.now() - datetime.timedelta(days=30):
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
