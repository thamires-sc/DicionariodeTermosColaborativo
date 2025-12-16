from django.db import models
from django.contrib.auth.models import User

# RF02 e RF06: Define as categorias focadas em TI
CATEGORIA_CHOICES = (
    ('PROG', 'Programação e Desenvolvimento'),
    ('DBA', 'Banco de Dados (DBA)'),
    ('CLOUD', 'Cloud Computing'),
    ('REDES', 'Redes e Segurança'),
    ('UXUI', 'UX/UI Design'),
    ('GERAL', 'Geral de TI'),
)

class Termo(models.Model):
    # RRN01: Garante que o título é único. A mensagem de erro está corrigida aqui.
    termo = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name='Título do Termo',
        error_messages={
            'unique': "Já existe um termo cadastrado com este título. Por favor, escolha um título diferente."
        }
    )
    
    # RF02 e RRN02: Definição (validação de tamanho é feita no forms.py)
    definicao = models.TextField(
        verbose_name='Definição Completa'
    )
    
    # RF02 e RF06: Categoria (max_length ajustado para 10 para evitar erros MySQL)
    categoria = models.CharField(
        max_length=10, 
        choices=CATEGORIA_CHOICES, 
        default='GERAL',
        verbose_name='Categoria'
    )
    
    # RRN03: Autoria Automática (Usuário que cadastrou/colaborou)
    colaborador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='termos_cadastrados',
        verbose_name='Autor/Colaborador'
    )
    
    # Data de registro do termo
    data_criacao = models.DateTimeField(
        auto_now_add=True
    )
    
    # Data da última atualização
    data_atualizacao = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        # A classe Meta agora está correta, sem o atributo 'error_messages'
        verbose_name_plural = "Termos"
        ordering = ['termo']
        
    def __str__(self):
        return self.termo
    
    