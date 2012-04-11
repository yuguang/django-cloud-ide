from django.forms import ModelForm, Textarea, TextInput
from models import *

class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = ('title', 'description', 'tags')
        widgets = {
            'title': TextInput(attrs={
                'class': 'required letterswithspace check-spelling',
                'minWords': '3',
                'data-bind': 'value: title, attr: { readonly: !newFiddle() }'
            }),
            'description': Textarea(attrs={
                'class': 'required',
                'minWords': '10',
                'data-bind': 'value: description'
            }),
            'tags': TextInput(attrs={
                'class': 'required letterswithbasicpunc',
                'data-bind': 'value: tags'
            })
        }
