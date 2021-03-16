from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import ClearableFileInput, ModelForm, ValidationError, HiddenInput, IntegerField

from backend.models import Preek, Reeks, Prediker

class PreekForm(ModelForm):
    
    class Meta:
        model = Preek
        fields = ['datum', 'prediker', 'tema', 'skriflesing', 'audio_file']
        widgets = {
            'datum': DateTimePickerInput(options={'sideBySide': True}),
            'audio_file': ClearableFileInput(attrs={'accept': '.mp3'}),
        }

class ReeksForm(ModelForm):

    class Meta:
        model = Reeks
        fields = ['naam']

class PredikerForm(ModelForm):

    class Meta:
        model = Prediker
        fields = '__all__'