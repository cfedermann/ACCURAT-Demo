"""
Project: ACCURAT Demo Translation Services
 Author: Christian Federmann <cfedermann@dfki.de>
"""
from json import dumps
from subprocess import Popen
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as _login, logout as _logout
from django.shortcuts import render_to_response
from django.template import RequestContext

from accurat.forms import TranslateForm, LANGUAGE_PAIRS, LANGUAGE_CODES
from accurat.settings import COMMIT_TAG

TRANSLATION_CACHE = {'baseline': {}, 'improved': {}, 'narrow': {}}

def _compile_json_data(language_pairs):
    """
    Converts a tuple of language pair data into a 2-dimensional JSON map.
    """
    json_data = {}
    for language_pair in language_pairs:
        items = language_pair.split(',')
        _source = items[0].strip()
        _target = items[1].strip()
        _type =  items[2].strip()
        if not _source in json_data.keys():
            json_data[_source] = {}
        
        if not _target in json_data[_source].keys():
            json_data[_source][_target] = []
        
        json_data[_source][_target].append(_type)
    
    return json_data

def _translate(_source, _target, _type, _text):
    from tempfile import mkstemp
    from os import unlink, close, write
    
    source_language = LANGUAGE_CODES[_source]
    target_language = LANGUAGE_CODES[_target]
    system_type = _type.lower()
    
    _sentences_to_translate = []
    _cache = TRANSLATION_CACHE[system_type]
    for _line in _text.split(u'\n'):
        _stripped = _line.strip()
        if _cache.has_key(_stripped):
            if _cache[_stripped].has_key(target_language):
                continue
        
        _sentences_to_translate.append(_stripped)
    
    if len(_sentences_to_translate):
        source_file = mkstemp(suffix=".source", dir="/tmp")
        write(source_file[0], u'\n'.join(_sentences_to_translate))
        write(source_file[0], u'\n')
        close(source_file[0])
    
        target_file = source_file[1].strip('.source') + '.target'
    
        # This is a special instance of the Moses worker, with pre-defined
        # knowledge about the ACCURAT Moses configurations.  We use this
        # approach to ensure that only one Moses process at a time can be
        # started; by doing so, we can avoid memory issues.
        MOSES_CMD = '/share/accurat/run/wmt10/bin/moses-irstlm/mosesdecoder' \
          '/mosesdecoder/moses-cmd/src/moses'
    
        MOSES_CONFIG = '/share/accurat/mtserver/accurat/{0}-{1}/' \
          '{2}.moses.ini.bin'.format(source_language, target_language,
          system_type)
    
        # Then, we invoke the Moses command reading from the source file
        # and writing to a target file, also inside /tmp.  This blocks until
        # the Moses process finishes.
        shell_cmd = "{0} -f {1} < {2} > {3}".format(
          MOSES_CMD, MOSES_CONFIG, source_file[1], target_file)

        process = Popen(shell_cmd, shell=True)
        process.wait()

        # We can now load the translation from the target file.
        with open(target_file, 'r') as target:
            target_text = target.read()
    
        target_text = target_text.decode('utf-8')
        
        unlink(source_file[1])
        unlink(target_file)
    
    else:
        from time import sleep
        sleep(2)
        target_text = u''
    
    _result = []
    _translated_sentences = target_text.split(u'\n')
    _pos = 0
    for _line in _text.split(u'\n'):
        _stripped = _line.strip()
        if _cache.has_key(_stripped):
            if _cache[_stripped].has_key(target_language):
                _result.append(_cache[_stripped][target_language])
                continue
        
        else:
            _cache[_stripped] = {}
        
        _translated_sentence = _translated_sentences[_pos]
        _result.append(_translated_sentence)
        _cache[_stripped][target_language] = _translated_sentence
        
        _pos += 1
    
    print TRANSLATION_CACHE

    return u'\n'.join(_result)
    

def home(request):
    dictionary = {
      'title': 'ACCURAT Translation Services',
      'commit_tag': COMMIT_TAG,
    }
    return render_to_response("home.html", dictionary,
      context_instance=RequestContext(request))

@login_required
def translate(request):
    selected = ',,'
    if request.method == "POST":
        form = TranslateForm(request.POST)
        result = None
        
        print request.POST
        
        print "form.is_valid() = ", form.is_valid()

        if form.is_valid():
            # Create translation, blocking until result is ready
            # Set result variable...
            _source = form.cleaned_data['source_language']
            _target = form.cleaned_data['target_language']
            _type = form.cleaned_data['system_type']
            _text = form.cleaned_data['source_text']
            
            selected = '{0},{1},{2}'.format(_source, _target, _type)
            result = _translate(_source, _target, _type, _text)

    else:
        form = TranslateForm()
        result = None
    
    dictionary = {
      'title': 'ACCURAT Translation Services',
      'commit_tag': COMMIT_TAG,
      'form': form,
      'result': result,
      'selected': selected,
      'json_data': dumps(_compile_json_data(LANGUAGE_PAIRS)),
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
