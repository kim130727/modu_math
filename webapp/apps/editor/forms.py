from __future__ import annotations

from django import forms


class SemanticJsonForm(forms.Form):
    semantic_json = forms.CharField(widget=forms.Textarea, required=True)

