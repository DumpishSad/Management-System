from django import forms
from .models import Meeting
from users.models import User


class MeetingForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Участники"
    )

    datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label="Дата и время"
    )

    class Meta:
        model = Meeting
        fields = ['title', 'datetime', 'participants']