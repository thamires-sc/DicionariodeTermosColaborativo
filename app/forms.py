# app/forms.py

from django import forms
from .models import Termo
from django.core.exceptions import ValidationError

class TermoForm(forms.ModelForm):
    class Meta:
        model = Termo
        # Campos que o usuário poderá preencher (RF02: Termo, Definição, Categoria)
        fields = ['termo', 'definicao', 'categoria'] 

    # RRN02: Validação da Regra de Negócio para Definição
    def clean_definicao(self):
        definicao = self.cleaned_data.get('definicao')
        
        # A validação de mínimo de 20 caracteres é feita aqui, no forms.py
        if len(definicao) < 20:
            raise ValidationError(f"A definição deve ter pelo menos 20 caracteres. (Atual: {len(definicao)})")
            
        return definicao