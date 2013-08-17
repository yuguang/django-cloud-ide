from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from taggit.models import Tag
from django.db.models import Count
from cloud_ide.fiddle.models import Snippet, Language
from utils import *

def snippet_list(request, queryset=None, **kwargs):
    if queryset is None:
        queryset = Snippet.objects.all()
    
    return object_list(
        request,
        queryset=queryset,
        paginate_by=20,
        **kwargs
    )


@login_required
def dashboard(request):
    return author_snippets(request, request.user.username)
    

def author_snippets(request, username):
    user = get_object_or_404(User, username=username)
    snippet_qs = Snippet.objects.filter(author=user) 
    return snippet_list(
        request,
        snippet_qs,
        template_name='fiddle/user_detail.html',
        extra_context={'author': user},
    )
    

def top_authors(request):
    return object_list(
        request,
        queryset=Snippet.objects.top_authors(),
        template_name='fiddle/top_authors.html',
        paginate_by=20)


def top_tags(request):
    return object_list(
        request,
        queryset=Snippet.objects.top_tags(),
        template_name='fiddle/tag_list.html',
        paginate_by=20,
    )
    

def top_languages(request):
    return object_list(
        request,
        queryset=Language.objects.all().annotate(score=Count('snippet')).order_by('-score'),
        template_name='fiddle/language_list.html',
        paginate_by=20)


def matches_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    snippet_qs = Snippet.objects.matches_tag(tag)
    return snippet_list(
        request,
        queryset=snippet_qs,
        template_name='fiddle/tag_detail.html',
        extra_context={'tag': tag},
    )


def language_detail(request, slug):
    language = get_object_or_404(Language, name=slug)
    return month_object_list(
        request,
        queryset=language.snippet_set.all(),
        paginate_by=20,
        template_name='fiddle/language_detail.html',
        extra_context={'language': language},
    )
