from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['score']
        labels = {'score': 'Оценка (1–5)'}
