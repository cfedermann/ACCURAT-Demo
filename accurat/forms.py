# -*- coding: utf-8 -*-
"""
Project: ACCURAT Demo Translation Services
 Author: Christian Federmann <cfedermann@dfki.de>
"""
from django import forms

LANGUAGE_PAIRS = (
  ('1', u'English → German'),
)

class TranslateForm(forms.Form):
    source_language = forms.ChoiceField()
    target_language = forms.ChoiceField()
    system_type = forms.ChoiceField()
    source_text = forms.CharField(max_length=1000,
      help_text="You can enter up to 1,000 characters...",
      widget=forms.Textarea(attrs={'class': 'span8', 'maxlength': 1000}))