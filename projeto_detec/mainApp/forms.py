from django import forms
from .models import Conds, Itens_facial, Itens_dvr, Itens_outro

class condsForm(forms.ModelForm):
    class Meta:
        model = Conds
        fields = ['name', 'relatos', 'endereco']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do condomínio'
            }),
            'relatos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Relato'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço'
            })
        }
        labels = {
            'name': 'Condomínio',
            'relatos': 'Relatos',
            'endereco': 'Endereço'
        }
        
class FacialForm(forms.ModelForm):
    class Meta:
        model = Itens_facial
        fields = ['item', 'iplocal', 'link', 'mac', 'http', 'user', 'senha', 'desc']
        widgets = {
            'item': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item'
            }),
            'iplocal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IP local'
            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link WEB'
            }),
            'mac': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço MAC'
            }),
            'http': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Porta HTTP'
            }),
            'user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuário'
            }),
            'senha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Senha'
            }),
            'desc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição'
            }),
        }
        
class DVRForm(forms.ModelForm):
    class Meta:
        model = Itens_dvr
        fields = ['item', 'iplocal', 'link', 'mac', 'http', 'rtsp', 'user', 'senha', 'desc']
        widgets = {
            'item': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item'
            }),
            'iplocal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IP local'
            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link WEB'
            }),
            'mac': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço MAC'
            }),
            'http': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Porta HTTP'
            }),
            'user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuário'
            }),
            'senha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Senha'
            }),
            'desc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição'
            }),
        }
        
class OutroForm(forms.ModelForm):
    class Meta:
        model = Itens_outro
        fields = ['item', 'iplocal', 'link', 'mac', 'http', 'rtsp', 'user', 'senha', 'desc']
        widgets = {
            'item': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item'
            }),
            'iplocal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IP local'
            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link WEB'
            }),
            'mac': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço MAC'
            }),
            'http': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Porta HTTP'
            }),
            'user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuário'
            }),
            'senha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Senha'
            }),
            'desc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição'
            }),
        }