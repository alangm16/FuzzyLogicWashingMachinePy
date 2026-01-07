import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Crear sistema de control y simulador
sistema_ctrl = None
simulador = None

def calcular_resultados():
    global sistema_ctrl, simulador
    if sistema_ctrl is None or simulador is None:
        messagebox.showerror("Error", "El sistema de control no está definido.")
        return

    # Obtener valores de entrada
    tipo_tela = tipo_tela_var.get()
    suciedad_ropa = suciedad_ropa_var.get()
    peso_ropa = peso_ropa_var.get()

    # Establecer entradas en el simulador
    simulador.input['tipoTela'] = tipo_tela
    simulador.input['suciedadRopa'] = suciedad_ropa
    simulador.input['pesoRopa'] = peso_ropa

    # Computar el resultado
    simulador.compute()

    # Obtener resultados y redondear
    tiempo_lavado_result = round(simulador.output['tiempoLavado'], 1)
    temperatura_result = round(simulador.output['temperatura'], 2)
    tiempo_secado_result = round(simulador.output['tiempoSecado'], 1)
    rpm_result = round(simulador.output['RPM'], 1)
    calidad_lavado_result = round(simulador.output['calidadLavado'], 1)

    # Mostrar resultados
    resultados_text.delete(1.0, tk.END)
    resultados_text.insert(tk.END, f"Resultados:\n\n"
                                    f"Tiempo de Lavado: {tiempo_lavado_result}\n"
                                    f"Temperatura: {temperatura_result}\n"
                                    f"Tiempo de Secado: {tiempo_secado_result}\n"
                                    f"RPM: {rpm_result}\n"
                                    f"Calidad de Lavado: {calidad_lavado_result}")

def iniciar_sistema():
    global sistema_ctrl, simulador
    # Crear sistema de control
    tipo_tela = ctrl.Antecedent(np.arange(0, 101, 1), 'tipoTela')
    suciedad_ropa = ctrl.Antecedent(np.arange(0, 101, 1), 'suciedadRopa')
    peso_ropa = ctrl.Antecedent(np.arange(0, 101, 1), 'pesoRopa')
    tiempo_lavado = ctrl.Consequent(np.arange(0, 61, 1), 'tiempoLavado')
    temperatura = ctrl.Consequent(np.arange(15, 61, 1), 'temperatura')
    tiempo_secado = ctrl.Consequent(np.arange(0, 61, 1), 'tiempoSecado')
    rpm = ctrl.Consequent(np.arange(0, 1601, 1), 'RPM')
    calidad_lavado = ctrl.Consequent(np.arange(0, 101, 1), 'calidadLavado')

    # Definir funciones de membresía, reglas, y crear el sistema de control y simulador

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

    # Código de definición de funciones de membresía y reglas aquí...

    sistema_ctrl = ctrl.ControlSystem(rules)
    simulador = ctrl.ControlSystemSimulation(sistema_ctrl)

# Crear ventana
root = tk.Tk()
root.title("Sistema de Lavado")

# Crear y empaquetar contenedor para entradas
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

# Variables de entrada
tipo_tela_var = tk.DoubleVar()
suciedad_ropa_var = tk.DoubleVar()
peso_ropa_var = tk.DoubleVar()

# Etiquetas y controles de entrada
tipo_tela_label = ttk.Label(input_frame, text="Tipo de Tela (0-100):")
tipo_tela_label.grid(row=0, column=0, sticky=tk.W)
tipo_tela_scale = ttk.Scale(input_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=tipo_tela_var)
tipo_tela_scale.grid(row=0, column=1, sticky=tk.W)
tipo_tela_value_label = ttk.Label(input_frame, textvariable=tipo_tela_var)
tipo_tela_value_label.grid(row=0, column=2, sticky=tk.W)

suciedad_ropa_label = ttk.Label(input_frame, text="Suciedad de la Ropa (0-100):")
suciedad_ropa_label.grid(row=1, column=0, sticky=tk.W)
suciedad_ropa_scale = ttk.Scale(input_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=suciedad_ropa_var)
suciedad_ropa_scale.grid(row=1, column=1, sticky=tk.W)
suciedad_ropa_value_label = ttk.Label(input_frame, textvariable=suciedad_ropa_var)
suciedad_ropa_value_label.grid(row=1, column=2, sticky=tk.W)

peso_ropa_label = ttk.Label(input_frame, text="Peso de la Ropa (0-100):")
peso_ropa_label.grid(row=2, column=0, sticky=tk.W)
peso_ropa_scale = ttk.Scale(input_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=peso_ropa_var)
peso_ropa_scale.grid(row=2, column=1, sticky=tk.W)
peso_ropa_value_label = ttk.Label(input_frame, textvariable=peso_ropa_var)
peso_ropa_value_label.grid(row=2, column=2, sticky=tk.W)

# Botón de calcular
calcular_button = ttk.Button(input_frame, text="Calcular", command=calcular_resultados)
calcular_button.grid(row=3, column=0, columnspan=2, pady=10)

# Crear y empaquetar contenedor para resultados
resultados_frame = ttk.Frame(root, padding="10")
resultados_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))

# Texto de resultados
resultados_text = tk.Text(resultados_frame, height=10, width=30)
resultados_text.grid(row=0, column=0)

# Inicializar sistema de control
iniciar_sistema()

# Ejecutar ventana
root.mainloop()