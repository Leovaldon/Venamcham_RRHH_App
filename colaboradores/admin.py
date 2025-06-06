from django.contrib import admin

from django.contrib import admin
from .models import Colaborador, Departamento, Cargo, EvaluacionDesempeno, EvaluacionClima, ResultadoOperativo, TipoEvaluacion, Evaluacion360, EvaluacionObjetivos # Importa el modelo Colaborador

# Registra el modelo para que sea visible y gestionable en el panel de administración
admin.site.register(Colaborador)
admin.site.register(Departamento)
admin.site.register(Cargo)
# admin.site.register(EvaluacionDesempeno) #
# admin.site.register(EvaluacionClima)     #
# admin.site.register(ResultadoOperativo)  #
admin.site.register(TipoEvaluacion)
admin.site.register(Evaluacion360)
admin.site.register(EvaluacionObjetivos)

from django import forms
from django.contrib import messages
from django.db import models
from django.utils.html import format_html

#-----------------EVALUACION 360º-----------------
class Evaluacion360AdminForm(forms.ModelForm):
    # Pequeña descripción al inicio del formulario
    descripcion_360 = forms.CharField(
        label="", # Deja la etiqueta vacía
        widget=forms.Textarea(attrs={'readonly': 'readonly', 'rows': 4, 'cols': 80, 'style': 'border: none; background-color: transparent; resize: none; font-style: italic;'}),
        initial="La riqueza de la evaluación 360° radica en obtener feedback de múltiples fuentes, lo que permite al evaluado recibir una visión completa y equilibrada de su desempeño. Esto es crucial para identificar patrones de comportamiento, áreas de mejora y oportunidades de desarrollo que podrían no ser visibles desde una sola perspectiva.",
        required=False # No es un campo que se guarde, solo informativo
    )

    class Meta:
        model = Evaluacion360
        fields = '__all__' # Incluye todos los campos del modelo

    def clean(self):
        cleaned_data = super().clean()

        # Validar que las puntuaciones estén entre 1 y 5
        # Ahora 'models' estará definido gracias a la importación
        puntuaciones_fields = [f.name for f in self.Meta.model._meta.get_fields() if isinstance(f, models.IntegerField) and f.name.startswith('p')]

        for field_name in puntuaciones_fields:
            valor = cleaned_data.get(field_name)
            if valor is not None:
                if not (1 <= valor <= 5):
                    self.add_error(field_name, "La puntuación debe ser entre 1 y 5.")
                #else:
                    #self.add_error(field_name, "Este campo es obligatorio y la puntuación debe ser entre 1 y 5.")


        # Validaciones adicionales aquí si es necesario, por ejemplo:
        # Asegurarse de que el 'tipo_evaluacion' sea el correcto para Evaluacion360, etc.
        # Desarrollar en el futuro

        return cleaned_data

class Evaluacion360Admin(admin.ModelAdmin):
    form = Evaluacion360AdminForm # Usamos nuestro formulario personalizado

    list_display = (
        'colaborador',
        'fecha_evaluacion',
        'evaluador',
        'puntaje_total',
        'link_documento_adjunto',
    )
    list_filter = ('fecha_evaluacion', 'evaluador', 'tipo_evaluacion', 'colaborador')
    search_fields = ('colaborador__primer_nombre', 'colaborador__primer_apellido', 'evaluador')

    fieldsets = (
        (None, {
            'fields': ('descripcion_360',) # Solo para la descripción inicial
        }),
        ('Información Básica', {
            'fields': ('colaborador', 'tipo_evaluacion', 'fecha_evaluacion', 'evaluador'),
        }),
        ('Puntuaciones de Comportamiento y Habilidades', {
            'description': 'Puntúe cada aspecto del 1 al 5 (donde 1 es "Necesita mejorar" y 5 es "Excelente").',
            'fields': (
                'p1_resuelve_problemas', 'p2_resuelve_conflictos', 'p3_respetuoso',
                'p4_empatia', 'p5_sociable_comunicativo', 'p6_confiable',
                'p7_aporta_valor', 'p8_actitud_proactiva_ayudar', 'p9_proactivo_ideas',
                'p10_iniciativa_proyectos', 'p11_conoce_valores', 'p12_comportamiento_etico',
                'p13_implica_cumple_plazos', 'p14_manejo_estres', 'p15_recibe_criticas_aprende',
                'p16_valora_otras_opiniones', 'p17_ideas_innovadoras', 'p18_practica_formacion_continua',
            ),
        }),
        ('Otros Comentarios y Documentos', {
            'fields': ('comentarios', 'documento_adjunto'),
        }),
        ('Puntaje Total', {
            'fields': ('puntaje_total',),
            'description': 'Este campo se calcula automáticamente.',
            'classes': ('collapse',),
        })
    )
    readonly_fields = ('puntaje_total',)

# --- MÉTODO PERSONALIZADO PARA EL ENLACE DEL DOCUMENTO ---
    def link_documento_adjunto(self, obj):
        if obj.documento_adjunto: # Verifica si hay un archivo adjunto
            # Retorna un enlace HTML que abre el archivo en una nueva pestaña
            return format_html('<a href="{}" target="_blank">Ver/Descargar</a>', obj.documento_adjunto.url)
        return "N/A" # Si no hay archivo, muestra "N/A"

    link_documento_adjunto.short_description = "Documento Adjunto" # Nombre de la columna en el listado
# --------------------------------------------------------

# Ahora registraremos Evaluacion360 con nuestra clase de personalización
admin.site.unregister(Evaluacion360)
admin.site.register(Evaluacion360, Evaluacion360Admin)

#-----------------EVALUACION POR OBJETIVOS-----------------
class EvaluacionObjetivosAdminForm(forms.ModelForm):
    descripcion_objetivos = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'readonly': 'readonly', 'rows': 3, 'cols': 80, 'style': 'border: none; background-color: transparent; resize: none; font-style: italic;'}),
        initial="La evaluación por objetivos permite medir el desempeño de un colaborador basándose en el logro de metas específicas y cuantificables establecidas para un período determinado. Esto se alinea con el marco de OKRs (Objetivos y Resultados Clave).",
        required=False
    )

    class Meta:
        model = EvaluacionObjetivos
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        puntuacion = cleaned_data.get('puntuacion_final')

        # Validar que la puntuación final esté entre 1 y 100
        if puntuacion is not None:
            if not (1 <= puntuacion <= 100): # Asumiendo que la puntuación final es de 1 a 100
                self.add_error('puntuacion_final', "La puntuación final debe ser entre 1 y 100.")
            #else:
                #self.add_error('puntuacion_final', "Este campo es obligatorio y la puntuación debe ser entre 1 y 100.")

        # Validaciones adicionales, por ejemplo:
        # - Si tipo_medicion es %, meta debe ser un porcentaje válido
        # - Si tipo_medicion es Cantidad, meta debe ser un número entero o decimal.
        # - Validar que resultado_obtenido tenga sentido con meta y tipo_medicion.
        # Estas validaciones pueden volverse complejas, se agregaran a futuro.

        return cleaned_data

class EvaluacionObjetivosAdmin(admin.ModelAdmin):
    form = EvaluacionObjetivosAdminForm

    list_display = (
        'colaborador',
        'fecha_evaluacion',
        'objetivo_general',
        'meta',
        'resultado_obtenido',
        'puntuacion_final',
        'evaluador',
        'link_documento_adjunto',
    )
    list_filter = ('fecha_evaluacion', 'evaluador', 'tipo_medicion', 'colaborador')
    search_fields = ('colaborador__primer_nombre', 'colaborador__primer_apellido', 'objetivo_general', 'evaluador')

    fieldsets = (
        (None, {
            'fields': ('descripcion_objetivos',)
        }),
        ('Información General del Objetivo', {
            'fields': ('colaborador', 'tipo_evaluacion', 'fecha_evaluacion', 'periodo_evaluado', 'evaluador'),
        }),
        ('Detalle del Objetivo', {
            'fields': ('objetivo_general', 'tipo_medicion', 'meta', 'resultado_obtenido'),
        }),
        ('Resultado y Feedback', {
            'fields': ('puntuacion_final', 'observaciones', 'documento_adjunto'),
        })
    )

# --- MÉTODO PERSONALIZADO PARA EL ENLACE DEL DOCUMENTO ---
    def link_documento_adjunto(self, obj):
        if obj.documento_adjunto: # Verifica si hay un archivo adjunto
            # Retorna un enlace HTML que abre el archivo en una nueva pestaña
            return format_html('<a href="{}" target="_blank">Ver/Descargar</a>', obj.documento_adjunto.url)
        return "N/A" # Si no hay archivo, muestra "N/A"

    link_documento_adjunto.short_description = "Documento Adjunto" # Nombre de la columna en el listado
# --------------------------------------------------------

# Ahora registraremos EvaluacionObjetivos con nuestra clase de personalización
admin.site.unregister(EvaluacionObjetivos)
admin.site.register(EvaluacionObjetivos, EvaluacionObjetivosAdmin)