from django import forms
from submit.models import CodeSubmission

language_choices=[
    ("py","Python"),
    ("c","C"),
    ("cpp","C++"),
]

class CodeSubmissionForm(forms.ModelForm):
    language=forms.ChoiceField(choices=language_choices)

    class Meta:
        model=CodeSubmission
        fields=['language','code','input_data']
        widgets = {
            'code': forms.Textarea(attrs={'class': 'code-area'}),
            'input_data': forms.Textarea(attrs={'class': 'input-area'}),
        }