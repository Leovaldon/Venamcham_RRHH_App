from django.test import TestCase

from .models import Colaborador, Departamento, Cargo, Evaluacion360, TipoEvaluacion
import datetime # Para trabajar con fechas

class ColaboradorModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Colaborador.
    """

    def setUp(self):
        """
        Configura los datos iniciales necesarios para las pruebas.
        Se ejecuta antes de cada método de prueba.
        """
        self.departamento = Departamento.objects.create(nombre="Ventas", descripcion="Departamento de Ventas")
        self.cargo = Cargo.objects.create(nombre="Ejecutivo de Ventas", descripcion="Rol de ventas directas")
        
        self.colaborador = Colaborador.objects.create(
            cedula="12345678",
            primer_nombre="Juan",
            primer_apellido="Perez",
            fecha_nacimiento=datetime.date(1990, 5, 15),
            cargo=self.cargo,
            departamento=self.departamento,
            fecha_ingreso=datetime.date(2020, 1, 1),
            salario_base=1500.00,
            activo=True
        )

    def test_colaborador_creation(self):
        """
        Verifica que un colaborador se pueda crear correctamente
        y que su representación __str__ sea la esperada.
        """
        self.assertEqual(Colaborador.objects.count(), 1)
        colaborador = Colaborador.objects.get(cedula="12345678")
        self.assertEqual(colaborador.primer_nombre, "Juan")
        self.assertEqual(str(colaborador), "Juan Perez (12345678)")
        self.assertEqual(colaborador.cargo.nombre, "Ejecutivo de Ventas")

    def test_unique_cedula(self):
        """
        Verifica que no se puedan crear dos colaboradores con la misma cédula.
        """
        with self.assertRaises(Exception): # Esperamos que se levante una excepción
            Colaborador.objects.create(
                cedula="12345678", # Cédula duplicada
                primer_nombre="Maria",
                primer_apellido="Gomez",
                fecha_nacimiento=datetime.date(1991, 1, 1),
                cargo=self.cargo,
                departamento=self.departamento,
                fecha_ingreso=datetime.date(2021, 1, 1),
                salario_base=1600.00,
            )

class Evaluacion360ModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Evaluacion360.
    """

    def setUp(self):
        self.departamento = Departamento.objects.create(nombre="Marketing")
        self.cargo = Cargo.objects.create(nombre="Diseñador")
        self.colaborador = Colaborador.objects.create(
            cedula="87654321",
            primer_nombre="Ana",
            primer_apellido="Ruiz",
            fecha_nacimiento=datetime.date(1992, 10, 20),
            cargo=self.cargo,
            departamento=self.departamento,
            fecha_ingreso=datetime.date(2019, 3, 1),
            salario_base=1800.00,
        )
        self.tipo_evaluacion_360 = TipoEvaluacion.objects.create(nombre="Evaluación 360º")

    def test_puntaje_total_calculation(self):
        """
        Verifica que el puntaje total de Evaluacion360 se calcule correctamente.
        """
        evaluacion = Evaluacion360.objects.create(
            colaborador=self.colaborador,
            tipo_evaluacion=self.tipo_evaluacion_360,
            fecha_evaluacion=datetime.date(2024, 6, 1),
            evaluador="Supervisor Inmediato",
            p1_resuelve_problemas=4,
            p2_resuelve_conflictos=5,
            p3_respetuoso=3,
            p4_empatia=4,
            p5_sociable_comunicativo=5,
            p6_confiable=4,
            p7_aporta_valor=3,
            p8_actitud_proactiva_ayudar=4,
            p9_proactivo_ideas=5,
            p10_iniciativa_proyectos=3,
            p11_conoce_valores=4,
            p12_comportamiento_etico=5,
            p13_implica_cumple_plazos=4,
            p14_manejo_estres=3,
            p15_recibe_criticas_aprende=4,
            p16_valora_otras_opiniones=5,
            p17_ideas_innovadoras=4,
            p18_practica_formacion_continua=3,
            comentarios="Buen desempeño general."
        )
        
        # El puntaje total esperado sería la suma de todos los pX_...
        expected_total = sum([4,5,3,4,5,4,3,4,5,3,4,5,4,3,4,5,4,3]) # Suma de los valores
        self.assertEqual(evaluacion.puntaje_total, expected_total)
        self.assertEqual(evaluacion.puntaje_total, 72) # Confirma que la suma es 69
        
    def test_evaluacion360_str_representation(self):
        """
        Verifica que la representación __str__ de Evaluacion360 sea la correcta.
        """
        evaluacion = Evaluacion360.objects.create(
            colaborador=self.colaborador,
            tipo_evaluacion=self.tipo_evaluacion_360,
            fecha_evaluacion=datetime.date(2024, 6, 1),
            evaluador="Supervisor Inmediato",
            # Se requieren al menos los campos obligatorios para crear el objeto
            p1_resuelve_problemas=1, p2_resuelve_conflictos=1, p3_respetuoso=1, p4_empatia=1,
            p5_sociable_comunicativo=1, p6_confiable=1, p7_aporta_valor=1, p8_actitud_proactiva_ayudar=1,
            p9_proactivo_ideas=1, p10_iniciativa_proyectos=1, p11_conoce_valores=1, p12_comportamiento_etico=1,
            p13_implica_cumple_plazos=1, p14_manejo_estres=1, p15_recibe_criticas_aprende=1, p16_valora_otras_opiniones=1,
            p17_ideas_innovadoras=1, p18_practica_formacion_continua=1,
        )
        self.assertEqual(str(evaluacion), "Eval. 360º de Ana Ruiz (2024-06-01 por Supervisor Inmediato)")

