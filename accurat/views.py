"""
Project: ACCURAT Demo Translation Services
 Author: Christian Federmann <cfedermann@dfki.de>
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as _login, logout as _logout
from django.shortcuts import render_to_response
from django.template import RequestContext

from accurat.forms import TranslateForm
from accurat.settings import COMMIT_TAG

def home(request):
    dictionary = {
      'title': 'ACCURAT Translation Services',
      'commit_tag': COMMIT_TAG,
    }
    return render_to_response("home.html", dictionary,
      context_instance=RequestContext(request))

# @login_required
def translate(request):
    if request.method == "POST":
        form = TranslateForm(request.POST)
        result = None

        if form.is_valid():
            # Create translation, blocking until result is ready
            # Set result variable...
            language = form.cleaned_data['language_pair']
            result = "TRANSLATION_{}_WOULD_BE_AVAILABLE_HERE".format(language)

    else:
        form = TranslateForm()
        result = None

    dictionary = {
      'title': 'ACCURAT Translation Services',
      'commit_tag': COMMIT_TAG,
      'form': form,
      'result': result,
    }
    return render_to_response("translate.html", dictionary,
      context_instance=RequestContext(request))

def login(request, template_name):
    """
    Renders login view by connecting to django.contrib.auth.views.
    """
    if request.user.username:
        dictionary = {
          'commit_tag': COMMIT_TAG,
          'message': 'You are already logged in as "{0}".'.format(
            request.user.username),
          'title': 'Appraise evaluation system',
        }
        
        return render(request, 'frontpage.html', dictionary)
    
    extra_context = {'commit_tag': COMMIT_TAG}
    return _login(request, template_name, extra_context=extra_context)


def logout(request, next_page):
    """
    Renders logout view by connecting to django.contrib.auth.views.
    """
    return _logout(request, next_page)
