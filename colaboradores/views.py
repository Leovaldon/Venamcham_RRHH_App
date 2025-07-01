from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io # Importa io para manejar la salida del PDF
import os
from datetime import datetime
from django.conf import settings

from .models import Evaluacion360, EvaluacionObjetivos # IMportar los modelos necesarios


#---------- EVALUACION 360 ----------
# Función auxiliar para xhtml2pdf para encontrar archivos estáticos y media
def link_callback(uri, rel):
    # Determinar la ruta absoluta al archivo
    # Si es un archivo media (subido por el usuario)
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    # Si es un archivo estático (CSS, JS, imágenes de diseño, como tu logo)
    elif uri.startswith(settings.STATIC_URL):
        # Aquí está el cambio clave: Intentamos encontrarlo directamente en la carpeta 'static'
        # de tu BASE_DIR, que es donde los tienes en desarrollo.
        path = os.path.join(settings.BASE_DIR, uri.replace(settings.STATIC_URL, "static/"))
        # Ojo: si tu STATIC_URL fuera algo como '/assets/', entonces uri.replace('/assets/', "static/")
        # pero con STATIC_URL = 'static/', lo mejor es simplemente reemplazar 'static/'

        # Otra forma robusta de buscar en STATICFILES_DIRS (más complejo para un solo logo)
        # from django.contrib.staticfiles import finders
        # static_file_path = finders.find(uri.replace(settings.STATIC_URL, ''))
        # if static_file_path:
        #     path = static_file_path
        # else:
        #     path = None # No encontrado por finders

    else:
        return uri  # Puede ser una URL externa que xhtml2pdf no necesita resolver localmente

    # Asegúrate de que el archivo existe y es legible
    if not path or not os.path.isfile(path):
        print(f"DEBUG: PDF Link Callback - Archivo NO ENCONTRADO para URI: {uri} en la ruta intentada: {path}")
        # Puedes devolver una ruta a una imagen de "no encontrado" si quieres un placeholder
        # return 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==' # Pequeña imagen transparente
        return None # Si devuelve None o una cadena vacía, simplemente no se mostrará

    return path

#---------- GENERAR REPORTE EVALUACION 360º ----------
def generar_reporte_evaluacion360_pdf(request, evaluacion_id):

    """
    Genera un reporte en formato PDF para una Evaluación 360º específica.
    El PDF incluye los datos del colaborador, las puntuaciones de la evaluación
    y comentarios adicionales, con un formato de reporte corporativo.

    Parámetros:
    - request (HttpRequest): Objeto de la solicitud HTTP.
    - evaluacion_id (int): ID de la instancia de Evaluacion360 a reportar.

    Retorna:
    - HttpResponse: Un archivo PDF listo para descargar.
    """

    # Obtener la instancia de la evaluación 360 o un 404 si no existe
    evaluacion = get_object_or_404(Evaluacion360, pk=evaluacion_id)

    # Contexto para la plantilla HTML del PDF
    context = {
        'evaluacion': evaluacion,
        'now': datetime.now(), # Para mostrar la fecha de generación
    }

    # Cargar la plantilla HTML
    template_path = 'colaboradores/evaluacion360_pdf_template.html'
    template = get_template(template_path)
    html = template.render(context)

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    # 'attachment' fuerza la descarga, 'inline' intentaría mostrarlo en el navegador
    response['Content-Disposition'] = f'attachment; filename="reporte_evaluacion_360_{evaluacion.colaborador.cedula}_{evaluacion.fecha_evaluacion}.pdf"'

    # Buffer para escribir el PDF
    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        encoding='utf-8' # Muy importante para caracteres especiales (acentos, ñ)
    )

    # Si hay errores en la generación del PDF
    if pisa_status.err:
        # Renderizar una página de error más amigable
        return HttpResponse('Hubo un error al generar el PDF: <pre>' + html + '</pre>')
    return response

#---------- GENERAR REPORTE EVALUACION POR OBJETIVO ----------
def generar_reporte_evaluacion_objetivos_pdf(request, evaluacion_id):

    """
    Genera un reporte en formato PDF para una Evaluación por objetivos específica.
    El PDF incluye los datos del colaborador, las puntuaciones de la evaluación
    y comentarios adicionales, con un formato de reporte corporativo.

    Parámetros:
    - request (HttpRequest): Objeto de la solicitud HTTP.
    - evaluacion_id (int): ID de la instancia de Evaluacion360 a reportar.

    Retorna:
    - HttpResponse: Un archivo PDF listo para descargar.
    """

    evaluacion = get_object_or_404(EvaluacionObjetivos, pk=evaluacion_id)
    context = {
        'evaluacion': evaluacion,
        'now': datetime.now(),
    }
    # Asegúrate que el template_path apunte a tu nueva plantilla de objetivos
    template_path = 'colaboradores/evaluacion_objetivos_pdf_template.html' 
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    # Nombre del archivo para la descarga
    response['Content-Disposition'] = f'attachment; filename="reporte_evaluacion_objetivos_{evaluacion.colaborador.cedula}_{evaluacion.fecha_evaluacion}.pdf"'

    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        encoding='utf-8',
        link_callback=link_callback # ¡Asegúrate que link_callback esté aquí también!
    )
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF de Objetivos: <pre>' + html + '</pre>')
    return response