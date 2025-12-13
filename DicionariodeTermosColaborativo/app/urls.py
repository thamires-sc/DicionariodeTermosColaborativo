# app/urls.py

from django.urls import path

# Importa as classes e a função que definimos em app/views.py
from .views import (
    ListaTermosView, 
    TermoCreateView, 
    TermoUpdateView, 
    TermoDeleteView, 
    detalhe_termo
)

urlpatterns = [
    # 1. LISTAGEM, BUSCA E HOME (RF05/RF03/RF06)
    # ListaTermosView é uma CLASSE, então usamos .as_view()
    path('', ListaTermosView.as_view(), name='lista_termos'), 
    
    # 2. CRIAÇÃO DE TERMO (RF02)
    # TermoCreateView é uma CLASSE
    path('adicionar/', TermoCreateView.as_view(), name='adicionar_termo'), 
    
    # 3. VISUALIZAÇÃO DE DETALHE (RF04)
    # detalhe_termo é uma FUNÇÃO, então é chamada diretamente
    path('<int:pk>/', detalhe_termo, name='detalhe_termo'),
    
    # 4. EDIÇÃO (RF07)
    # TermoUpdateView é uma CLASSE
    path('<int:pk>/editar/', TermoUpdateView.as_view(), name='editar_termo'),
    
    # 5. EXCLUSÃO (RF07)
    # TermoDeleteView é uma CLASSE
    path('<int:pk>/excluir/', TermoDeleteView.as_view(), name='excluir_termo'),
]