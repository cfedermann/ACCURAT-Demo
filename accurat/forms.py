"""
Project: ACCURAT Demo Translation Services
 Author: Christian Federmann <cfedermann@dfki.de>
"""
from django import forms

LANGUAGE_CODES = {
  'German': 'de',
  'English': 'en',
  'Romanian': 'ro',
  'Greek': 'el',
  'Estonian': 'et',
  'Croatian': 'hr',
  'Lithuanian': 'lt',
  'Latvian': 'lv',
  'Slovenian': 'sl',
}

LANGUAGE_PAIRS = (
  'German,English,Baseline',
  'German,English,Improved',
  'German,Romanian,Baseline',
  'German,Romanian,Improved',
  'Greek,Romanian,Baseline',
  'Greek,Romanian,Improved',
  'English,Greek,Baseline',
  'English,Greek,Improved',
  'English,Estonian,Baseline',
  'English,Estonian,Improved',
  'English,Croatian,Baseline',
  'English,Croatian,Improved',
  'English,Croatian,Narrow',
  'English,Lithuanian,Baseline',
  'English,Lithuanian,Improved',
  'English,Lithuanian,Narrow',
  'English,Latvian,Baseline',
  'English,Latvian,Improved',
  'English,Latvian,Narrow',
  'English,Romanian,Baseline',
  'English,Romanian,Improved',
  'English,Romanian,Narrow',
  'English,Slovenian,Baseline',
  'English,Slovenian,Improved',
  'Croatian,English,Baseline',
  'Croatian,English,Improved',
  'Lithunian,Romanian,Baseline',
  'Lithunian,Romanian,Improved',
  'Latvian,Lithunian,Baseline',
  'Latvian,Lithunian,Improved',
  'Romanian,German,Baseline',
  'Romanian,German,Improved',
  'Romanian,Greek,Baseline',
  'Romanian,Greek,Improved',
  'Romanian,English,Baseline',
  'Romanian,English,Improved',
  'Slovenian,English,Baseline',
  'Slovenian,English,Improved',
)

def _compute_choices(index):
    """Returns available source language choices."""
    choices = list(set([x.split(',')[index] for x in LANGUAGE_PAIRS]))
    choices.sort()
    return tuple((x, x) for x in choices)

class TranslateForm(forms.Form):
    source_language = forms.ChoiceField(choices=_compute_choices(0))
    target_language = forms.ChoiceField(choices=_compute_choices(1))
    system_type = forms.ChoiceField(choices=_compute_choices(2))
    source_text = forms.CharField(max_length=1000,
      help_text="You can enter up to 1,000 characters...",
      widget=forms.Textarea(attrs={'class': 'span8', 'maxlength': 1000}))