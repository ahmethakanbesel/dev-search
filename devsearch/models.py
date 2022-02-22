from django.db import models


# Create your models here.
class Developer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, null=False, blank=False)
    username = models.SlugField(default='', null=True, unique=True, editable=False)
    bio = models.TextField(default='', null=True, blank=True)
    email = models.EmailField(default='', null=True, blank=True)
    company = models.CharField(max_length=128, null=True, blank=True)
    location = models.CharField(max_length=128, null=True, blank=True)
    website = models.URLField(default='', null=True, blank=True)
    avatar = models.URLField(default='', null=True, blank=True)
    stars = models.IntegerField(default=0, null=True, blank=True)
    forks = models.IntegerField(default=0, null=True, blank=True)
    followers = models.IntegerField(default=0, null=True, blank=True)
    following = models.IntegerField(default=0, null=True, blank=True)
    repositories = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Repository(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(Developer, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(default='', null=True, blank=True)
    language = models.CharField(max_length=128, null=True, blank=True)
    stars = models.IntegerField(default=0, null=True, blank=True)
    forks = models.IntegerField(default=0, null=True, blank=True)
    has_issues = models.BooleanField(default=False)
    has_wiki = models.BooleanField(default=False)
    has_projects = models.BooleanField(default=False)
    has_pages = models.BooleanField(default=False)
    license = models.CharField(max_length=128, null=True, blank=True)
    last_push = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RepositoryTopic(models.Model):
    id = models.BigAutoField(primary_key=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    topic = models.CharField(max_length=128, null=False, blank=False)
