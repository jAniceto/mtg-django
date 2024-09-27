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
    card_sb = forms.CharField(max_length=100, required=False)
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), empty_label='Any', required=False)
    SORT_OPTIONS = [
        ('updated_at', 'Date updated'),
        ('created_at', 'Date created'),
        ('price', 'Deck price'),
        ('name', 'Deck name'),
    ]
    sort_attribute = forms.ChoiceField(choices=SORT_OPTIONS, initial='Date updated')
    sort_direction = forms.ChoiceField(
        choices=[('Desc', 'Desc'), ('Asc', 'Asc')], 
        initial='Desc',
        widget=forms.RadioSelect
    )


class DecksJSONUploadForm(forms.Form):
    file = forms.FileField(label='Select a JSON file')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.json'):
            raise forms.ValidationError('File must be a JSON file.')
        return file
