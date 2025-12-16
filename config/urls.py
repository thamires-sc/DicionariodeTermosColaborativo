from django.contrib import admin
from django.urls import path, include
from app.views import CadastroView

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('contas/', include('django.contrib.auth.urls')),
    path('contas/cadastro/', CadastroView.as_view(), name='cadastro'),
    path('', include('app.urls')), 
]