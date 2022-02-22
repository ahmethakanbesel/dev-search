import datetime
import json

from django.contrib.humanize.templatetags import humanize
from django.db.models import Sum
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Developer, Repository
from .forms import SearchForm
import urllib.parse

from .services import search_on_github, save_user, get_user


def index(request):
    form = SearchForm()
    return render(request, 'devsearch/index.html', {'form': form})


def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/result/' + urllib.parse.quote(form['keyword'].value()))
    else:
        form = SearchForm()
    return render(request, 'devsearch/index.html', {'form': form})


def result(request, keyword, page=1):
    if request.GET.get('page'):
        page_param = int(request.GET.get('page'))
        if page_param and page_param > 1:
            page = page_param
    # get data from github
    developer_data = search_on_github(keyword, page)
    # read json file
    # with open('./devsearch/result.json') as json_file:
    #    developer_data = json.load(json_file)
    context = {
        "keyword": keyword,
        "total_count": developer_data['total_count'],
        "data": developer_data['items'],
        "range": range(1,  21),
        "current_page": page
    }
    return render(request, 'devsearch/result.html', context)


def detail(request, username):
    try:
        developer = Developer.objects.get(username=username)
    except Developer.DoesNotExist:
        user = get_user(username)
        if 'login' in user:
            save_user(user)
            developer = Developer.objects.get(username=username)
        else:
            raise Http404("GitHub account does not exist")
    repositories = Repository.objects.filter(owner=developer)
    developer.stars = repositories.aggregate(Sum('stars'))['stars__sum']
    developer.forks = repositories.aggregate(Sum('forks'))['forks__sum']
    developer.last_push = repositories.order_by('-last_push').first()
    if developer.last_push:
        developer.last_push = developer.last_push.last_push
    developer.save()
    if developer.last_push:
        developer.last_push = humanize.naturaltime(repositories.order_by('-last_push').first().last_push)
    languages = repositories.raw('SELECT 1 as id, language, count(1) count FROM devsearch_repository WHERE owner_id = %s and language IS NOT NULL GROUP BY language ORDER BY count DESC', [developer.id])
    repositories = repositories.order_by('-stars')
    return render(request, 'devsearch/profile.html',
                  {'developer': developer, 'repositories': repositories, 'languages': languages})


def not_found(request, exception):
    return render(request, 'devsearch/404.html')
