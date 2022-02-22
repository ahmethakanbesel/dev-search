from django.contrib import admin

# Register your models here.
from devsearch import models

admin.site.register(models.Developer)
admin.site.register(models.Repository)
admin.site.register(models.RepositoryTopic)
