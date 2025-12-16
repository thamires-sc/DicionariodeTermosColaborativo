from django.urls import path

from .views import (
    ListaTermosView, 
    TermoCreateView, 
    TermoUpdateView, 
    TermoDeleteView, 
    detalhe_termo
)

urlpatterns = [
   
    path('', ListaTermosView.as_view(), name='lista_termos'), 
    
    path('adicionar/', TermoCreateView.as_view(), name='adicionar_termo'), 
    
    path('<int:pk>/', detalhe_termo, name='detalhe_termo'),
    

    path('<int:pk>/editar/', TermoUpdateView.as_view(), name='editar_termo'),
    

    path('<int:pk>/excluir/', TermoDeleteView.as_view(), name='excluir_termo'),
]