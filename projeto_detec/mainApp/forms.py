from django import forms
from .models import Conds, Itens_facial, Itens_dvr, Itens_outro, Relatos

class condsForm(forms.ModelForm):
    class Meta:
        model = Conds
        fields = ['name', 'endereco']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }
        
        labels = {
            'name': 'Nome do condomínio',
            'endereco': 'Endereço'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if hasattr(field, 'label') and field.label:
                # Remove os dois pontos e espaços extras
                field.label = field.label.rstrip(': ')
        
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
        
class RelatoForm(forms.ModelForm):
    class Meta:
        model = Relatos
        fields = ['relato', 'tipo_relato', 'cat_rel_ayel', 'cat_rel_cam']
        widgets = {
            'relato': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva o relato',
                'rows': 4
            }),
            'tipo_relato': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cat_rel_ayel': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'cat_rel_cam': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }