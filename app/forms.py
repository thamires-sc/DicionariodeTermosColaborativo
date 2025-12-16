from django import forms
from .models import Termo
from django.core.exceptions import ValidationError

class TermoForm(forms.ModelForm):
    class Meta:
        model = Termo
        fields = ['termo', 'definicao', 'categoria'] 

    def clean_definicao(self):
        definicao = self.cleaned_data.get('definicao')
        
        if len(definicao) < 20:
            raise ValidationError(f"A definição deve ter pelo menos 20 caracteres. (Atual: {len(definicao)})")
            
        return definicao