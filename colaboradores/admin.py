from django.contrib import admin

from django.contrib import admin
from .models import Colaborador # Importa el modelo Colaborador

# Registra el modelo para que sea visible y gestionable en el panel de administración
admin.site.register(Colaborador)
