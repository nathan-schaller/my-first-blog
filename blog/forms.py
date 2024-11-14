from django import forms
 
from .models import Character
 
class MoveForm(forms.ModelForm):
 
    class Meta:
        model = Character
        fields = ('lieu',)

    def clean_lieu(self):
    # Logique de validation du champ 'lieu'
        nouveau_lieu = self.cleaned_data['lieu']
        # Validation si le lieu est occupé, etc.
        return nouveau_lieu   