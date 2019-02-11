from django import forms
from .models import Incoming, Outcoming


class NewForm(forms.ModelForm):
    class Meta():
        model = Incoming
        fields = [
            "incoming_date",
            "track_i",
            "trailer_i",
            "container_i",
            "upload",
            "sender",
            "cargo",
            "pack",
            "quantity_i",
            "cell_position",
            "cmr",
            "akt_i",
            "lot"
        ]
        widgets = {
        'quantity_i': forms.NumberInput(attrs={'placeholder': 'колличество'}),
        'track_i': forms.TextInput(attrs={'placeholder': '???'}),
        'incoming_date': forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }


class PlusForm(forms.ModelForm):
    class Meta():
        model = Outcoming
        fields = [
            "akt_incoming",
            "outcoming_date",
            "track_o",
            "trailer_o",
            "recepient",
            "akt_o",
            "quantity_o",
            "ttn",
            "comments"
        ]
        widgets = {
            'comments': forms.Textarea(attrs={'placeholder': 'Коментарии'}),
            'quantity_o': forms.NumberInput(attrs={'placeholder': 'колличество'}),
            'outcoming_date': forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

class summary(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
