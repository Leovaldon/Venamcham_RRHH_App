from django.urls import path
from . import views

app_name = 'colaboradores' # Define el namespace de la app para evitar conflictos con otras URLs

urlpatterns = [
    path('evaluacion360/<int:evaluacion_id>/pdf/', views.generar_reporte_evaluacion360_pdf, name='reporte_evaluacion360_pdf'),
    path('evaluacionobjetivos/<int:evaluacion_id>/pdf/', views.generar_reporte_evaluacion_objetivos_pdf, name='reporte_evaluacion_objetivos_pdf'),
    # Aquí irán otras URLs futuras de la app colaboradores
]