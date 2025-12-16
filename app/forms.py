from django import forms
from .models import Termo
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CadastroColaboradorForm(UserCreationForm):
    """
    Formulário para cadastro de usuários que adiciona o campo 'email' 
    e o torna obrigatório para fins de recuperação de senha.
    """
    class Meta:
        model = User
        fields = ('username', 'email') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].required = True 
        
        self.fields['email'].label = 'E-mail para Recuperação de Senha'
        
        self.fields['email'].widget.attrs.update({'placeholder': 'seu.email@exemplo.com'})



class TermoForm(forms.ModelForm):
    class Meta:
        model = Termo
        fields = ['termo', 'definicao', 'categoria'] 

    def clean_definicao(self):
        definicao = self.cleaned_data.get('definicao')
        
        if len(definicao) < 20:
            raise ValidationError(f"A definição deve ter pelo menos 20 caracteres. (Atual: {len(definicao)})")
            
        return definicao