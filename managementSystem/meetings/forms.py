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

    class Meta:
        model = Meeting
        fields = ['title', 'date', 'time', 'participants']
