from django import forms
from .models import conds

class condsForm(forms.ModelForm):
    class Meta:
        model = conds
        fields = ['name', 'relatos']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do condomínio'
            }),
            'relatos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Relato'
            }),
        }
        labels = {
            'name': 'Condomínio',
            'relatos': 'Relatos'
        }