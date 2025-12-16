from django.contrib import admin
from django.urls import path, include
from app.views import CadastroView

# A lista DEVE ser chamada 'urlpatterns' e DEVE conter as rotas!
urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('contas/', include('django.contrib.auth.urls')),
    path('contas/cadastro/', CadastroView.as_view(), name='cadastro'),
    path('', include('app.urls')), 
]