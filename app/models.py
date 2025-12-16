from django.db import models
from django.contrib.auth.models import User

CATEGORIA_CHOICES = (
    ('PROG', 'Programação e Desenvolvimento'),
    ('DBA', 'Banco de Dados (DBA)'),
    ('CLOUD', 'Cloud Computing'),
    ('REDES', 'Redes e Segurança'),
    ('UXUI', 'UX/UI Design'),
    ('GERAL', 'Geral de TI'),
)

class Termo(models.Model):

    termo = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name='Título do Termo',
        error_messages={
            'unique': "Já existe um termo cadastrado com este título. Por favor, escolha um título diferente."
        }
    )
    
    definicao = models.TextField(
        verbose_name='Definição Completa'
    )
    
    categoria = models.CharField(
        max_length=10, 
        choices=CATEGORIA_CHOICES, 
        default='GERAL',
        verbose_name='Categoria'
    )
    
    colaborador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='termos_cadastrados',
        verbose_name='Autor/Colaborador'
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name_plural = "Termos"
        ordering = ['termo']
        
    def __str__(self):
        return self.termo
    
    