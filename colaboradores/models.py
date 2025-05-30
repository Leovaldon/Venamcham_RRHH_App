from django.db import models

from django.db import models

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
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    departamento = models.CharField(max_length=100, verbose_name="Departamento")
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
