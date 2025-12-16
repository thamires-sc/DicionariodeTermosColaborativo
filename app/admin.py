# app/admin.py

from django.contrib import admin
from .models import Termo

# Registra o modelo Termo no painel de administração
admin.site.register(Termo)
