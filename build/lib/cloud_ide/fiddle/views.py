from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template import RequestContext
import django.utils.simplejson as json
from jsonresponse import JsonResponse

from forms import SnippetForm
from models import Language, Snippet, defaultFiddle, defaultMeta, languageMeta

    
def create(request, language=None):
    form = SnippetForm()
    view_model = json.dumps(dict(defaultFiddle, **{
            'authenticated': request.user.is_authenticated()
        }))
    if language:
        default_meta = languageMeta.get(language, None)
        if not default_meta:
            return HttpResponseForbidden()
    else:
        default_meta = defaultMeta
    return render_to_response('index.html', {
        'form': form,
        'view_model': view_model,
        'default_meta': default_meta
    }, context_instance=RequestContext(request))


@login_required
def save(request):
    if not request.method == 'POST' or not 'title' in request.POST:
        return HttpResponseForbidden()
    
    snippet_title = request.POST['title']
    
    if not snippet_title:
        return HttpResponseForbidden()
    
    try: # load the snippet
        snippet = Snippet.objects.get(title=snippet_title)
        if request.user.id != snippet.author.id:
            return HttpResponseForbidden()
    except Snippet.DoesNotExist: # create new snippet
        snippet = Snippet(author=request.user)
        if not title_available(snippet_title):
            return HttpResponseForbidden()
    
    response_dict = {}
    if request.is_ajax():
        form = SnippetForm(instance=snippet, data=request.POST)
        if form.is_valid():
            snippet.code = request.POST['code']
            snippet.language = Language.objects.get(name=request.POST['language'])
            snippet = form.save()
            response_dict.update({'success': True})
        else:
            response_dict.update({'errors': form.errors})
    return JsonResponse(response_dict)


def title_available(title):
    return Snippet.objects.filter(title=title).count() == 0


def check_title(request):
    available = False
    if request.is_ajax():
        title = request.GET.get('title', '')
        if title and title_available(title):
            available = True
    return JsonResponse({'available': available})


def open(request, snippet_slug=None, embedded=False, language=None):
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    form = SnippetForm(instance=snippet)
    view_model = json.dumps(dict(defaultFiddle, **{
            'newFiddle': False,
            'authenticated': request.user.is_authenticated(),
            'isOwner': request.user.id == snippet.author.id
        }))
    return render_to_response('index.html', {
        'snippet': snippet,
        'form': form,
        'view_model': view_model,
        'embedded': embedded,
        'ownerId': snippet.author.id
    }, context_instance=RequestContext(request))
   
