from django.db import models

from django.db import models

#COLABORADORES
class Colaborador(models.Model):
    # Datos personales
    cedula = models.CharField(max_length=15, unique=True, verbose_name="Cédula de Identidad")
    primer_nombre = models.CharField(max_length=100, verbose_name="Primer Nombre")
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name="Segundo Nombre")
    primer_apellido = models.CharField(max_length=100, verbose_name="Primer Apellido")
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True, verbose_name="Segundo Apellido")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    correo_electronico = models.EmailField(max_length=254, unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")

    # Datos laborales
    # REFERENCIA A LOS MODELOS COMO CADENAS DE TEXTO
    cargo = models.ForeignKey('Cargo', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cargo")
    departamento = models.ForeignKey('Departamento', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Departamento")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso")
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salario Base")
    activo = models.BooleanField(default=True, verbose_name="Activo en la empresa")

    # Metadatos automáticos
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    ultima_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        ordering = ['primer_apellido', 'primer_nombre'] # Ordena por defecto al consultar

    def __str__(self):
        # Esto define cómo se muestra un objeto Colaborador en el panel de administración
        # y en otros lugares donde se necesita una representación en cadena.
        return f"{self.primer_nombre} {self.primer_apellido} ({self.cedula})"

#DEPARTAMENTOS DE VENAMCHAM
class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Departamento")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Departamento")

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

#CARGOS DEL PERSONAL
class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Cargo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Cargo")

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
#EVALUACION DE DESEMPEÑO (GENERAL)
class EvaluacionDesempeno(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='evaluaciones_desempeno', verbose_name="Colaborador Evaluado")
    fecha_evaluacion = models.DateField(verbose_name="Fecha de Evaluación")
    evaluador = models.CharField(max_length=100, verbose_name="Evaluador")
    puntaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Puntaje Obtenido") # Ej. 1-5, o 1-100
    comentarios = models.TextField(blank=True, null=True, verbose_name="Comentarios Generales")
    # Campo para adjuntar un archivo (ej. PDF de la evaluación detallada)
    documento_adjunto = models.FileField(upload_to='evaluaciones_desempeno/', blank=True, null=True, verbose_name="Documento Adjunto")

    class Meta:
        verbose_name = "Evaluación de Desempeño"
        verbose_name_plural = "Evaluaciones de Desempeño"
        ordering = ['-fecha_evaluacion', 'colaborador__primer_apellido'] # Ordena por fecha descendente

    def __str__(self):
        return f"Eval. Desempeño de {self.colaborador.primer_nombre} {self.colaborador.primer_apellido} ({self.fecha_evaluacion})"

#EVALUACION CLIMA LABORAL (GENERAL)
class EvaluacionClima(models.Model):
    # Para evaluaciones a nivel de departamento o general
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Departamento Evaluado")
    fecha_evaluacion = models.DateField(verbose_name="Fecha de Evaluación")
    titulo = models.CharField(max_length=200, verbose_name="Título de la Evaluación")
    # Aquí puedes agregar campos para métricas específicas del clima, ej. puntaje_liderazgo, puntaje_comunicacion
    puntaje_general = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Puntaje General del Clima")
    fortalezas = models.TextField(blank=True, null=True, verbose_name="Principales Fortalezas")
    areas_mejora = models.TextField(blank=True, null=True, verbose_name="Áreas de Oportunidad")
    documento_adjunto = models.FileField(upload_to='evaluaciones_clima/', blank=True, null=True, verbose_name="Informe Completo")

    class Meta:
        verbose_name = "Evaluación de Clima Organizacional"
        verbose_name_plural = "Evaluaciones de Clima Organizacional"
        ordering = ['-fecha_evaluacion', 'departamento__nombre']

    def __str__(self):
        if self.departamento:
            return f"Eval. Clima {self.titulo} - {self.departamento.nombre} ({self.fecha_evaluacion})"
        return f"Eval. Clima {self.titulo} (General) ({self.fecha_evaluacion})"

#RESULTADOS OPERATIVOS (GENERAL)
class ResultadoOperativo(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name='resultados_operativos', verbose_name="Colaborador Asociado")
    # Si un resultado operativo aplica a un departamento completo en lugar de un colaborador individual
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Departamento Asociado")
    fecha_registro = models.DateField(verbose_name="Fecha de Registro del Resultado")
    tipo_metrica = models.CharField(max_length=100, verbose_name="Tipo de Métrica (ej. Ventas, Producción, Proyectos Completados)")
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor del Resultado")
    comentarios = models.TextField(blank=True, null=True, verbose_name="Comentarios Adicionales")

    class Meta:
        verbose_name = "Resultado Operativo"
        verbose_name_plural = "Resultados Operativos"
        ordering = ['-fecha_registro', 'colaborador__primer_apellido', 'departamento__nombre']

    def __str__(self):
        if self.colaborador:
            return f"{self.tipo_metrica}: {self.valor} para {self.colaborador.primer_nombre} {self.colaborador.primer_apellido} ({self.fecha_registro})"
        elif self.departamento:
            return f"{self.tipo_metrica}: {self.valor} para {self.departamento.nombre} ({self.fecha_registro})"
        return f"{self.tipo_metrica}: {self.valor} (General) ({self.fecha_registro})"

#TIPO DE EVALUACION
class TipoEvaluacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Evaluación")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Tipo de Evaluación")

    class Meta:
        verbose_name = "Tipo de Evaluación"
        verbose_name_plural = "Tipos de Evaluaciones"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

#-----------------EVALUACION 360º -----------------  
class Evaluacion360(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='evaluaciones_360', verbose_name="Colaborador Evaluado")
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.PROTECT, verbose_name="Tipo de Evaluación")
    fecha_evaluacion = models.DateField(verbose_name="Fecha de Evaluación")
    evaluador = models.CharField(
        max_length=50,
        choices=[
            ('Yo mismo', 'Yo mismo'),
            ('Supervisor Inmediato', 'Supervisor Inmediato'),
            ('Compañero de Trabajo', 'Compañero de Trabajo'),
            ('Subordinado', 'Subordinado'),
            ('Cliente', 'Cliente'),
            ('Proveedor', 'Proveedor'),
        ],
        verbose_name="¿Quién Evalúa?"
    )

    # Preguntas con puntuación del 1 al 5
    p1_resuelve_problemas = models.IntegerField(verbose_name="¿Resuelve problemas de forma efectiva?")
    p2_resuelve_conflictos = models.IntegerField(verbose_name="¿Sabe resolver conflictos adecuadamente?")
    p3_respetuoso = models.IntegerField(verbose_name="¿Es respetuoso con el resto de los empleados?")
    p4_empatia = models.IntegerField(verbose_name="¿Muestra empatía?")
    p5_sociable_comunicativo = models.IntegerField(verbose_name="¿Es sociable y se comunica de forma abierta y cercana con sus colegas?")
    p6_confiable = models.IntegerField(verbose_name="¿Es un compañero en quien se puede confiar?")
    p7_aporta_valor = models.IntegerField(verbose_name="¿Aporta valor y conocimiento al resto?")
    p8_actitud_proactiva_ayudar = models.IntegerField(verbose_name="¿Tiene una actitud proactiva a la hora de ayudar en el equipo?")
    p9_proactivo_ideas = models.IntegerField(verbose_name="¿Es proactivo para aportar ideas?")
    p10_iniciativa_proyectos = models.IntegerField(verbose_name="¿Toma la iniciativa en los proyectos?")
    p11_conoce_valores = models.IntegerField(verbose_name="¿Conoce y pone en práctica la misión y los valores de la empresa?")
    p12_comportamiento_etico = models.IntegerField(verbose_name="¿Demuestra un comportamiento ético y profesional?")
    p13_implica_cumple_plazos = models.IntegerField(verbose_name="¿Se implica en su trabajo y cumple los plazos?")
    p14_manejo_estres = models.IntegerField(verbose_name="¿Sabe manejarse en situaciones de estrés y de sobrecarga de trabajo?")
    p15_recibe_criticas_aprende = models.IntegerField(verbose_name="¿Recibe de forma positiva las críticas y los comentarios constructivos, ya sean positivos o negativos? ¿Aprende de sus errores?")
    p16_valora_otras_opiniones = models.IntegerField(verbose_name="¿Toma en cuenta y valora otras opiniones incluso si son distintas a las suyas?")
    p17_ideas_innovadoras = models.IntegerField(verbose_name="¿Aporta ideas innovadoras para alcanzar objetivos?")
    p18_practica_formacion_continua = models.IntegerField(verbose_name="¿Se muestra a favor y practica la formación continua como método de ayuda al crecimiento de la empresa?")

    comentarios = models.TextField(verbose_name="Comentarios Adicionales")
    documento_adjunto = models.FileField(upload_to='evaluaciones_360/', blank=True, null=True, verbose_name="Documento Adjunto")

    puntaje_total = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Puntaje Total")

    class Meta:
        verbose_name = "Evaluación 360º"
        verbose_name_plural = "Evaluaciones 360º"
        ordering = ['-fecha_evaluacion', 'colaborador__primer_apellido']
        unique_together = ('colaborador', 'fecha_evaluacion', 'evaluador') # Evita duplicados para la misma persona, fecha y evaluador

    def calcular_puntaje_total(self):
        # Suma de todas las puntuaciones (excluyendo 'id' y 'puntaje_total' y campos no IntegerField)
        # Obtenemos todos los campos que son IntegerField y empiezan con 'p'
        puntuaciones_fields = [f for f in self._meta.get_fields() if isinstance(f, models.IntegerField) and f.name.startswith('p')]

        total = 0
        for field in puntuaciones_fields:
            valor = getattr(self, field.name) # Obtiene el valor del campo
            if valor is not None:
                total += valor
        return total

    def save(self, *args, **kwargs):
        # Antes de guardar, calcula el puntaje total
        self.puntaje_total = self.calcular_puntaje_total()
        super().save(*args, **kwargs) # Llama al método save original

    def __str__(self):
        return f"Eval. 360º de {self.colaborador.primer_nombre} {self.colaborador.primer_apellido} ({self.fecha_evaluacion} por {self.evaluador})"

#-----------------EVALUACION POR OBJETIVOS OKR-----------------
class EvaluacionObjetivos(models.Model):
    MEDICION_CHOICES = [
        ('% Cumplimiento', '% Cumplimiento'),
        ('Cantidad Cumplimiento', 'Cantidad Cumplimiento'),
        ('Logro', 'Logro (si aplica, ej. sí/no)'), # Se pueden añadir más opciones si es necesario
    ]

    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='evaluaciones_objetivos', verbose_name="Colaborador Evaluado")
    tipo_evaluacion = models.ForeignKey('TipoEvaluacion', on_delete=models.PROTECT, verbose_name="Tipo de Evaluación")
    fecha_evaluacion = models.DateField(verbose_name="Fecha de Evaluación")
    periodo_evaluado = models.CharField(max_length=100, verbose_name="Período Evaluado (ej. Q1 2025, Mensual Ene-25)")
    evaluador = models.CharField(max_length=100, verbose_name="Evaluador del Objetivo")

    # Detalles del Objetivo y su Medición
    objetivo_general = models.TextField(verbose_name="Objetivo General")
    tipo_medicion = models.CharField(max_length=50, choices=MEDICION_CHOICES, verbose_name="Tipo de Medición")
    meta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Meta (Valor Esperado)")
    resultado_obtenido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Resultado Obtenido")

    # Puntuación final y feedback
    puntuacion_final = models.IntegerField(null=True, blank=True, verbose_name="Puntuación del Colaborador (1-100)")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones / Feedback")
    documento_adjunto = models.FileField(upload_to='evaluaciones_objetivos/', blank=True, null=True, verbose_name="Documento Adjunto")

    class Meta:
        verbose_name = "Evaluación por Objetivos"
        verbose_name_plural = "Evaluaciones por Objetivos"
        ordering = ['-fecha_evaluacion', 'colaborador__primer_apellido']
        unique_together = ('colaborador', 'fecha_evaluacion', 'objetivo_general') # Evita duplicados para la misma persona, fecha y objetivo

    def __str__(self):
        return f"Eval. Objetivos de {self.colaborador.primer_nombre} {self.colaborador.primer_apellido} - {self.objetivo_general[:50]}... ({self.fecha_evaluacion})"