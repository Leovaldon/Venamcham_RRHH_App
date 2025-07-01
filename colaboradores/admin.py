from django.contrib import admin

from django.contrib import admin
from .models import Colaborador, Departamento, Cargo, EvaluacionDesempeno, EvaluacionClima, ResultadoOperativo, TipoEvaluacion, Evaluacion360, EvaluacionObjetivos, EvaluacionClimaOrganizacional

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
admin.site.register(EvaluacionClimaOrganizacional)

from django import forms
from django.contrib import messages
from django.db import models
from django.urls import reverse
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
        'generar_reporte_pdf_link',
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
            return format_html('<a class="button" href="{}" target="_blank">Ver/Descargar</a>', obj.documento_adjunto.url)
        return "N/A" # Si no hay archivo, muestra "N/A"

    link_documento_adjunto.short_description = "Documento Adjunto" # Nombre de la columna en el listado
# --------------------------------------------------------

# --- NUEVO MÉTODO PARA EL ENLACE DE GENERAR REPORTE PDF DE SISTEMA ---
    def generar_reporte_pdf_link(self, obj):
        # Crea un enlace a la URL que definimos en colaboradores/urls.py
        # 'colaboradores:reporte_evaluacion360_pdf' hace referencia a 'app_name:name_de_la_url'
        if obj.pk: # Asegura que el objeto ya esté guardado y tenga un ID
            url = reverse('colaboradores:reporte_evaluacion360_pdf', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}" target="_blank" style="background-color: #4CAF50; color: white; padding: 5px 10px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">Generar PDF</a>',
                url
            )
            return "Guardar para generar"

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
        'generar_reporte_pdf_link_objetivos',
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

# --- NUEVO MÉTODO PARA EL ENLACE DE GENERAR REPORTE PDF DE OBJETIVOS ---
    def generar_reporte_pdf_link_objetivos(self, obj):
        if obj.pk:
            # Asegúrate de que el nombre de la URL coincida con el de colaboradores/urls.py
            url = reverse('colaboradores:reporte_evaluacion_objetivos_pdf', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}" target="_blank" style="background-color: #4CAF50; color: white; padding: 5px 10px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">Generar PDF</a>',
                url
            )
        return "Guardar para generar"

    generar_reporte_pdf_link_objetivos.short_description = "Reporte Sistema"

# --- MÉTODO PERSONALIZADO PARA EL ENLACE DEL DOCUMENTO ---
    def link_documento_adjunto(self, obj):
        if obj.documento_adjunto: # Verifica si hay un archivo adjunto
            # Retorna un enlace HTML que abre el archivo en una nueva pestaña
            return format_html('<a class="button" href="{}" target="_blank">Ver/Descargar</a>', obj.documento_adjunto.url)
        return "N/A" # Si no hay archivo, muestra "N/A"

    link_documento_adjunto.short_description = "Documento Adjunto" # Nombre de la columna en el listado
# --------------------------------------------------------

# Ahora registraremos EvaluacionObjetivos con nuestra clase de personalización
admin.site.unregister(EvaluacionObjetivos)
admin.site.register(EvaluacionObjetivos, EvaluacionObjetivosAdmin)

#-----------------EVALUACION CLIMA ORGANIZACIONAL-----------------

class EvaluacionClimaOrganizacionalAdminForm(forms.ModelForm):
    descripcion_clima = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'readonly': 'readonly', 'rows': 4, 'cols': 80, 'style': 'border: none; background-color: transparent; resize: none; font-style: italic;'}),
        initial="Esta encuesta de clima organizacional busca recopilar feedback anónimo sobre diferentes aspectos del ambiente laboral, las relaciones y la percepción de la empresa. Su objetivo es identificar fortalezas y áreas de mejora para el bienestar y desarrollo de todos los colaboradores.",
        required=False
    )

    class Meta:
        model = EvaluacionClimaOrganizacional
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        # Validar que las puntuaciones de las preguntas cerradas estén entre 1 y 5
        # Filtramos campos que son IntegerField y no son ForeignKeys (para evitar el id del departamento o tipo_evaluacion)
        puntuaciones_fields = [
            f.name for f in self.Meta.model._meta.get_fields()
            if isinstance(f, models.IntegerField) and f.name not in ['id', 'departamento_id', 'tipo_evaluacion_id']
        ]

        for field_name in puntuaciones_fields:
            valor = cleaned_data.get(field_name)
            if valor is not None:
                if not (1 <= valor <= 5):
                    self.add_error(field_name, "La puntuación debe ser entre 1 y 5.")

        return cleaned_data

class EvaluacionClimaOrganizacionalAdmin(admin.ModelAdmin):
    form = EvaluacionClimaOrganizacionalAdminForm

    list_display = (
        'departamento',
        'fecha_evaluacion',
        'puntaje_total_cerradas', # Mostramos el puntaje total
        'link_documento_adjunto_clima', # Para futuros documentos adjuntos
    )
    list_filter = ('fecha_evaluacion', 'departamento')
    search_fields = ('departamento__nombre',)

    fieldsets = (
        (None, {
            'fields': ('descripcion_clima',)
        }),
        ('Información Básica', {
            'fields': ('departamento', 'fecha_evaluacion', 'tipo_evaluacion'),
            'description': 'Seleccione el departamento y la fecha de esta evaluación de clima. (Esta encuesta es anónima).'
        }),
        ('Relación con La Compañía (Puntúe del 1 al 5)', {
            'fields': (
                'rc1_directiva_coherente', 'rc2_conoce_plan_estrategico',
                'rc3_comparte_objetivos', 'rc4_identifica_valores',
                'rc5_comprometido_empresa', 'rc6_desarrollar_carrera',
                'rc7_mejorar_empresa_abierta', # Pregunta abierta aquí
            ),
        }),
        ('Relación con Los Líderes (Puntúe del 1 al 5)', {
            'fields': (
                'rl1_genera_ilusion', 'rl2_mantiene_ambiente', 'rl3_dedica_tiempo',
                'rl4_lider_coherente', 'rl5_comunica_prioridades', 'rl6_efectividad_feedback',
                'rl7_opinion_liderazgo_abierta', # Pregunta abierta
            ),
        }),
        ('Relación con El Puesto de Trabajo (Puntúe del 1 al 5)', {
            'fields': (
                'rpt1_recibio_herramientas', 'rpt2_impacto_objetivos_global',
                'rpt3_autonomia_trabajo', 'rpt4_feedback_ayuda_mejorar',
                'rpt5_conoce_crecimiento_profesional', 'rpt6_formacion_ayuda',
                'rpt7_siente_valorado', 'rpt8_concluye_trabajo_jornada',
                'rpt9_mejorar_puesto_abierta', # Pregunta abierta
            ),
        }),
        ('Relación con Los Compañeros (Puntúe del 1 al 5)', {
            'fields': (
                'rco1_ambiente_positivo', 'rco2_trabajo_equipo',
                'rco3_conoce_otros_departamentos', 'rco4_fomenta_agilidad',
                'rco5_comunicaciones_claras', 'rco6_comentarios_companeros_abierta', # Pregunta abierta
            ),
        }),
        ('Relación con Los Clientes (Puntúe del 1 al 5)', {
            'fields': (
                'rcl1_conoce_necesidades', 'rcl2_clientes_satisfechos',
                'rcl3_recomendaciones_tenidas_cuenta', 'rcl4_compagina_objetivos_calidad',
            ),
        }),
        ('Puntaje Total (Oculto)', { # Campo oculto, solo para referencia interna
            'fields': ('puntaje_total_cerradas',),
            'description': 'Este campo se calcula automáticamente y no se muestra en el formulario de la encuesta.',
            'classes': ('collapse',), # Oculta esta sección por defecto
        })
    )
    readonly_fields = ('puntaje_total_cerradas',) # No permitimos editar el total

    # --- MÉTODO PERSONALIZADO PARA EL ENLACE DEL DOCUMENTO ---
    def link_documento_adjunto_clima(self, obj):
        # Asumiendo que el modelo EvaluacionClimaOrganizacional tiene un campo 'documento_adjunto'
        if hasattr(obj, 'documento_adjunto') and obj.documento_adjunto:
            return format_html('<a href="{}" target="_blank">Ver/Descargar</a>', obj.documento_adjunto.url)
        return "N/A"
    link_documento_adjunto_clima.short_description = "Informe Adjunto"

    # --------------------------------------------------------

# Ahora registraremos EvaluacionClimaOrganizacional con nuestra clase de personalización
admin.site.unregister(EvaluacionClimaOrganizacional)
admin.site.register(EvaluacionClimaOrganizacional, EvaluacionClimaOrganizacionalAdmin)