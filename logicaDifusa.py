import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Crear variables de entrada
tipo_tela = ctrl.Antecedent(np.arange(0, 101, 1), 'tipoTela')
suciedad_ropa = ctrl.Antecedent(np.arange(0, 101, 1), 'suciedadRopa')
peso_ropa = ctrl.Antecedent(np.arange(0, 101, 1), 'pesoRopa')

# Crear variables de salida
tiempo_lavado = ctrl.Consequent(np.arange(0, 61, 1), 'tiempoLavado')
temperatura = ctrl.Consequent(np.arange(15, 61, 1), 'temperatura')
tiempo_secado = ctrl.Consequent(np.arange(0, 61, 1), 'tiempoSecado')
rpm = ctrl.Consequent(np.arange(0, 1601, 1), 'RPM')
calidad_lavado = ctrl.Consequent(np.arange(0, 101, 1), 'calidadLavado')

# Definir funciones de membresía
tipo_tela['delicada'] = fuzz.trimf(tipo_tela.universe, [0, 0, 50])
tipo_tela['media'] = fuzz.trimf(tipo_tela.universe, [10, 50, 90])
tipo_tela['resistente'] = fuzz.trimf(tipo_tela.universe, [50, 100, 100])

suciedad_ropa['poca'] = fuzz.trimf(suciedad_ropa.universe, [0, 0, 50])
suciedad_ropa['media'] = fuzz.trimf(suciedad_ropa.universe, [10, 50, 90])
suciedad_ropa['mucha'] = fuzz.trimf(suciedad_ropa.universe, [50, 100, 100])

peso_ropa['ligero'] = fuzz.trimf(peso_ropa.universe, [0, 0, 50])
peso_ropa['mediana'] = fuzz.trimf(peso_ropa.universe, [10, 50, 90])
peso_ropa['pesada'] = fuzz.trimf(peso_ropa.universe, [50, 100, 100])

# Definir funciones de membresía para las variables de salida
tiempo_lavado['muyCorta'] = fuzz.trapmf(tiempo_lavado.universe, [0, 0, 5, 10])
tiempo_lavado['corta'] = fuzz.trimf(tiempo_lavado.universe, [5, 15, 25])
tiempo_lavado['media'] = fuzz.trimf(tiempo_lavado.universe, [20, 30, 40])
tiempo_lavado['larga'] = fuzz.trimf(tiempo_lavado.universe, [35, 45, 55])
tiempo_lavado['muyLarga'] = fuzz.trapmf(tiempo_lavado.universe, [50, 55, 60, 60])

temperatura['fria'] = fuzz.trimf(temperatura.universe, [15, 15, 30])
temperatura['tibia'] = fuzz.trimf(temperatura.universe, [25, 37.5, 50])
temperatura['caliente'] = fuzz.trimf(temperatura.universe, [45, 60, 60])

tiempo_secado['muyCorta'] = fuzz.trapmf(tiempo_secado.universe, [0, 0, 5, 10])
tiempo_secado['corta'] = fuzz.trimf(tiempo_secado.universe, [5, 15, 25])
tiempo_secado['media'] = fuzz.trimf(tiempo_secado.universe, [20, 30, 40])
tiempo_secado['larga'] = fuzz.trimf(tiempo_secado.universe, [35, 45, 55])
tiempo_secado['muyLarga'] = fuzz.trapmf(tiempo_secado.universe, [50, 55, 60, 60])

rpm['baja'] = fuzz.trimf(rpm.universe, [0, 300, 600])
rpm['media'] = fuzz.trimf(rpm.universe, [400, 800, 1200])
rpm['alta'] = fuzz.trimf(rpm.universe, [1000, 1300, 1600])

calidad_lavado['baja'] = fuzz.trimf(calidad_lavado.universe, [0, 0, 50])
calidad_lavado['media'] = fuzz.trimf(calidad_lavado.universe, [10, 50, 90])
calidad_lavado['alta'] = fuzz.trimf(calidad_lavado.universe, [50, 100, 100])

# Definir reglas
rules = [
    ctrl.Rule(tipo_tela['delicada'] & suciedad_ropa['poca'] & peso_ropa['ligero'], 
              (tiempo_lavado['muyCorta'], temperatura['fria'], tiempo_secado['muyCorta'], rpm['baja'], calidad_lavado['alta'])),
    ctrl.Rule(tipo_tela['delicada'] & suciedad_ropa['poca'] & peso_ropa['mediana'], 
              (tiempo_lavado['corta'], temperatura['fria'], tiempo_secado['corta'], rpm['baja'], calidad_lavado['alta'])),
    ctrl.Rule(tipo_tela['delicada'] & suciedad_ropa['poca'] & peso_ropa['pesada'], 
              (tiempo_lavado['media'], temperatura['fria'], tiempo_secado['media'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['delicada'] & suciedad_ropa['media'] & peso_ropa['ligero'], 
              (tiempo_lavado['media'], temperatura['fria'], tiempo_secado['media'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['delicada'] & suciedad_ropa['media'] & peso_ropa['mediana'], 
              (tiempo_lavado['media'], temperatura['fria'], tiempo_secado['media'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['delicada'] & suciedad_ropa['media'] & peso_ropa['pesada'], 
              (tiempo_lavado['larga'], temperatura['fria'], tiempo_secado['larga'], rpm['media'], calidad_lavado['baja'])),
    ctrl.Rule(tipo_tela['delicada'] & suciedad_ropa['mucha'] & peso_ropa['ligero'], 
              (tiempo_lavado['media'], temperatura['tibia'], tiempo_secado['media'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['delicada'] & suciedad_ropa['mucha'] & peso_ropa['mediana'], 
              (tiempo_lavado['media'], temperatura['tibia'], tiempo_secado['media'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['delicada'] & suciedad_ropa['mucha'] & peso_ropa['pesada'], 
              (tiempo_lavado['larga'], temperatura['tibia'], tiempo_secado['larga'], rpm['media'], calidad_lavado['baja'])),
    ctrl.Rule(tipo_tela['media'] & suciedad_ropa['poca'] & peso_ropa['ligero'], 
              (tiempo_lavado['corta'], temperatura['fria'], tiempo_secado['corta'], rpm['baja'], calidad_lavado['alta'])),
    ctrl.Rule(tipo_tela['media'] & suciedad_ropa['poca'] & peso_ropa['mediana'], 
              (tiempo_lavado['media'], temperatura['fria'], tiempo_secado['media'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['media'] & suciedad_ropa['poca'] & peso_ropa['pesada'], 
              (tiempo_lavado['larga'], temperatura['fria'], tiempo_secado['larga'], rpm['media'], calidad_lavado['baja'])),
    ctrl.Rule(tipo_tela['media'] & suciedad_ropa['media'] & peso_ropa['ligero'], 
              (tiempo_lavado['media'], temperatura['tibia'], tiempo_secado['media'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['media'] & suciedad_ropa['media'] & peso_ropa['mediana'], 
              (tiempo_lavado['larga'], temperatura['tibia'], tiempo_secado['larga'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['media'] & suciedad_ropa['media'] & peso_ropa['pesada'], 
              (tiempo_lavado['larga'], temperatura['tibia'], tiempo_secado['larga'], rpm['alta'], calidad_lavado['alta'])),
    ctrl.Rule(tipo_tela['media'] & suciedad_ropa['media'] & peso_ropa['ligero'], 
              (tiempo_lavado['corta'], temperatura['tibia'], tiempo_secado['corta'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['media'] & suciedad_ropa['mucha'] & peso_ropa['mediana'], 
              (tiempo_lavado['larga'], temperatura['tibia'], tiempo_secado['larga'], rpm['alta'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['media'] & suciedad_ropa['mucha'] & peso_ropa['pesada'], 
              (tiempo_lavado['larga'], temperatura['tibia'], tiempo_secado['larga'], rpm['alta'], calidad_lavado['alta'])),
    ctrl.Rule(tipo_tela['resistente'] & suciedad_ropa['poca'] & peso_ropa['ligero'], 
              (tiempo_lavado['corta'], temperatura['fria'], tiempo_secado['corta'], rpm['baja'], calidad_lavado['alta'])),
    ctrl.Rule(tipo_tela['resistente'] & suciedad_ropa['poca'] & peso_ropa['mediana'], 
              (tiempo_lavado['media'], temperatura['fria'], tiempo_secado['media'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['resistente'] & suciedad_ropa['poca'] & peso_ropa['pesada'], 
              (tiempo_lavado['larga'], temperatura['fria'], tiempo_secado['larga'], rpm['media'], calidad_lavado['baja'])),
    ctrl.Rule(tipo_tela['resistente'] & suciedad_ropa['media'] & peso_ropa['ligero'], 
              (tiempo_lavado['media'], temperatura['tibia'], tiempo_secado['media'], rpm['media'], calidad_lavado['media'])),
    ctrl.Rule(tipo_tela['resistente'] & suciedad_ropa['media'] & peso_ropa['mediana'], 
              (tiempo_lavado['larga'], temperatura['tibia'], tiempo_secado['larga'], rpm['media'], calidad_lavado['baja'])),
    ctrl.Rule(tipo_tela['resistente'] & suciedad_ropa['media'] & peso_ropa['pesada'], 
              (tiempo_lavado['muyLarga'], temperatura['tibia'], tiempo_secado['muyLarga'], rpm['alta'], calidad_lavado['alta'])),
    ctrl.Rule(tipo_tela['resistente'] & suciedad_ropa['mucha'] & peso_ropa['ligero'], 
              (tiempo_lavado['media'], temperatura['caliente'], tiempo_secado['media'], rpm['media'], calidad_lavado['baja'])),
    ctrl.Rule(tipo_tela['resistente'] & suciedad_ropa['mucha'] & peso_ropa['mediana'], 
              (tiempo_lavado['larga'], temperatura['caliente'], tiempo_secado['larga'], rpm['alta'], calidad_lavado['alta'])),
    ctrl.Rule(tipo_tela['resistente'] & suciedad_ropa['mucha'] & peso_ropa['pesada'], 
              (tiempo_lavado['muyLarga'], temperatura['caliente'], tiempo_secado['muyLarga'], rpm['alta'], calidad_lavado['alta'])),
]

# Crear sistema de control
sistema_ctrl = ctrl.ControlSystem(rules)

# Crear simulador
simulador = ctrl.ControlSystemSimulation(sistema_ctrl)

# Establecer entradas
simulador.input['tipoTela'] = 50
simulador.input['suciedadRopa'] = 50
simulador.input['pesoRopa'] = 50

# Computar el resultado
simulador.compute()

# Obtener resultados y redondear
tiempo_lavado_result = round(simulador.output['tiempoLavado'],1)
temperatura_result = round(simulador.output['temperatura'], 2)
tiempo_secado_result = round(simulador.output['tiempoSecado'],1)
rpm_result = round(simulador.output['RPM'],1)
calidad_lavado_result = round(simulador.output['calidadLavado'],1)

# Mostrar resultados redondeados
print("Resultados redondeados:")
print("Tiempo de Lavado:", tiempo_lavado_result)
print("Temperatura:", temperatura_result)
print("Tiempo de Secado:", tiempo_secado_result)
print("RPM:", rpm_result)
print("Calidad de Lavado:", calidad_lavado_result)