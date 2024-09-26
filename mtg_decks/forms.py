from django import forms
from mtg_decks.models import Tag
from mtg_utils.mtg import color_families


class DeckFilterForm(forms.Form):
    FAMILY_CHOICES = [
        (k.capitalize(), k.capitalize())
        for k, v in color_families().items()  # e.g., ('Boros', 'Boros'),
    ]
    name = forms.CharField(max_length=100, required=False)
    family = forms.ChoiceField(choices=[('', 'Any')] + FAMILY_CHOICES, required=False)
    card = forms.CharField(max_length=100, required=False)
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), empty_label='Any', required=False)


class DecksJSONUploadForm(forms.Form):
    file = forms.FileField(label='Select a JSON file')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.json'):
            raise forms.ValidationError('File must be a JSON file.')
        return file
