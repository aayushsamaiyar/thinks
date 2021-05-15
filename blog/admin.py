from django.contrib import admin
from django.contrib.admin.decorators import register
from blog.models import Post,BlogComment
# Register your models here.

admin.site.register((Post, BlogComment))

