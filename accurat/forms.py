"""
Project: ACCURAT Demo Translation Services
 Author: Christian Federmann <cfedermann@dfki.de>
"""
from django import forms

LANGUAGE_PAIRS = (
  'English,German,TypeA',
  'English,German,TypeB',
  'English,German,TypeC',
  'French,German,TypeA',
  'French,German,TypeB',
  'English,French,TypeA',
)

def _compute_source_choices():
    """Returns available source language choices."""
    choices = list(set([x.split(',')[0] for x in LANGUAGE_PAIRS]))
    choices.sort()
    return tuple((x, x) for x in choices)

def _compute_target_choices():
    """Returns available target language choices."""
    choices = list(set([x.split(',')[1] for x in LANGUAGE_PAIRS]))
    choices.sort()
    return tuple((x, x) for x in choices)

def _compute_type_choices():
    """Returns available system type choices."""
    choices = list(set([x.split(',')[2] for x in LANGUAGE_PAIRS]))
    choices.sort()
    return tuple((x, x) for x in choices)

class TranslateForm(forms.Form):
    source_language = forms.ChoiceField(choices=_compute_source_choices())
    target_language = forms.ChoiceField(choices=_compute_target_choices())
    system_type = forms.ChoiceField(choices=_compute_type_choices())
    source_text = forms.CharField(max_length=1000,
      help_text="You can enter up to 1,000 characters...",
      widget=forms.Textarea(attrs={'class': 'span8', 'maxlength': 1000}))