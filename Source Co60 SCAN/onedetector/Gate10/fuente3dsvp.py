import opengate as gate
import opengate_core as g4
import os
import numpy as np
from math import cos, sin, radians
from scipy.spatial.transform import Rotation as R

# Unidades
mm = gate.g4_units.mm
cm = gate.g4_units.cm  
keV = gate.g4_units.keV
MeV = gate.g4_units.MeV
GeV = gate.g4_units.GeV
Bq = gate.g4_units.Bq
Ci = gate.g4_units.Ci
deg = gate.g4_units.deg
s = gate.g4_units.s

# Crear simulacion
sim = gate.Simulation()
sim.user_info.check_volumes_overlap = False  # Desactiva validacion de overlaps globalmente

# Directorio de salida
sim.output_dir = os.path.join(os.getcwd(), "output")


# Deshabilitar visualization
sim.user_info.visu = False  # Esto desactiva la visualizacion
#sim.user_info.visu = True  # Esto activa la visualizacion
#visu_type = "qt"

# Verbose para ver mensajes
sim.verbose_level = "INFO"  # Importante para que muestre tiempo en terminal
sim.g4_verbose_level = 0    # Esto puede mantenerse bajo para evitar ruido


# Cargar base de datos de materiales
sim.volume_manager.add_material_database("GateMaterials.db")

# World
world = sim.world  # Acceder al world por defecto
world.size = [200 * mm, 250 * mm, 200 * mm]
world.material = "G4_AIR"

# Funcion de rotacion. Rotacion de 90 grados alrededor del eje X
angle_deg = 90
rot = R.from_euler('x', angle_deg, degrees=True)
rotation_matrix = rot.as_matrix()

# PORTAMUESTRA optimizado (cuerpo + tapa incluidos)
portamuestra = sim.add_volume("Tubs", "portamuestra")
portamuestra.mother = "world"
portamuestra.material = "Aluminium"
portamuestra.rmin = 73.5 * mm
portamuestra.rmax = 74.0 * mm
portamuestra.dz = 100 * mm  # Altura total = 2 * dz
portamuestra.translation = [0 * mm, 0 * mm, 0 * mm]
portamuestra.rotation = rotation_matrix
portamuestra.user_info.vis = True
portamuestra.user_info.color = [1, 1, 1, 1]  # Blanco
portamuestra.user_info.style = "wireframe"
portamuestra.user_info.check_overlaps = True

# CONTENEDOR DE MUESTRA
contenedor = sim.add_volume("Tubs", "contenedormuestra")
contenedor.mother = "world"
contenedor.material = "PVC"
contenedor.rmin = 50.47 * mm
contenedor.rmax = 50.97 * mm
contenedor.dz = 129.5 / 2 * mm  # Gate define altura completa, GATE10 espera la mitad
contenedor.translation = [0 * mm, 0 * mm, 0 * mm]
contenedor.rotation = rotation_matrix
contenedor.user_info.vis = True
contenedor.user_info.color = [0, 1, 1, 1]  # Cyan (RGB: 0,1,1) + opaco (A:1)
contenedor.user_info.style = "wireframe"
contenedor.user_info.check_overlaps = True

# TAPA SUPERIOR DEL CONTENEDOR DE MUESTRA
tapa_sup_contenedor = sim.add_volume("Tubs", "tapa_sup_contenedor")
tapa_sup_contenedor.mother = "world"
tapa_sup_contenedor.material = "PVC"
tapa_sup_contenedor.rmin = 0.0 * mm
tapa_sup_contenedor.rmax = 50.97 * mm
tapa_sup_contenedor.dz = 2.0 / 2 * mm  # altura total / 2
tapa_sup_contenedor.translation = [0 * mm, 65.75 * mm, 0 * mm]
tapa_sup_contenedor.rotation = rotation_matrix
tapa_sup_contenedor.user_info.vis = True
tapa_sup_contenedor.user_info.color = [0, 1, 1, 1]  # Cyan (RGB: 0,1,1) + opaco (A:1)
tapa_sup_contenedor.user_info.style = "wireframe"
tapa_sup_contenedor.user_info.check_overlaps = True

# TAPA INFERIOR DEL CONTENEDOR DE MUESTRA
tapa_inf_contenedor = sim.add_volume("Tubs", "tapa_inf_contenedor")
tapa_inf_contenedor.mother = "world"
tapa_inf_contenedor.material = "PVC"
tapa_inf_contenedor.rmin = 0.0 * mm
tapa_inf_contenedor.rmax = 50.97 * mm
tapa_inf_contenedor.dz = 2.0 / 2 * mm  # altura total / 2
tapa_inf_contenedor.translation = [0 * mm, -65.75 * mm, 0 * mm]
tapa_inf_contenedor.rotation = rotation_matrix
tapa_inf_contenedor.user_info.vis = True
tapa_inf_contenedor.user_info.color = [0, 1, 1, 1]  # Cyan (RGB: 0,1,1) + opaco (A:1)
tapa_inf_contenedor.user_info.style = "wireframe"
tapa_inf_contenedor.user_info.check_overlaps = True

# SOPORTES DE MADERA (alternativa simple)
soportemadera1 = sim.add_volume("Tubs", "soportemadera1")
soportemadera1.mother = "world"
soportemadera1.material = "Wood"
soportemadera1.rmin = 0.0 * mm
soportemadera1.rmax = 59.97 * mm
soportemadera1.dz = 9.0 / 2 * mm

vector = np.array([0, -20.5 * mm, 0])
pos_inicial = np.array([0, -72.25 * mm, 0])
traslaciones = [list(pos_inicial + i * vector) for i in range(2)]
soportemadera1.translation = traslaciones
soportemadera1.rotation = [rotation_matrix] * 2
soportemadera1.user_info.vis = True
soportemadera1.user_info.color = [1, 1, 0, 1]
soportemadera1.user_info.style = "wireframe"
soportemadera1.user_info.check_overlaps = True

# Soporte central en forma de caja
soportemadera2 = sim.add_volume("Box", "soportemadera2")
soportemadera2.mother = "world"
soportemadera2.material = "Wood"
soportemadera2.size = [50 * mm, 50 * mm, 9.5 * mm]
soportemadera2.translation = [0 * mm, -82.5 * mm, 0 * mm]
soportemadera2.rotation = rotation_matrix
soportemadera2.user_info.vis = True
soportemadera2.user_info.color = [1, 1, 0, 1]  # Amarillo
soportemadera2.user_info.style = "wireframe"
soportemadera2.user_info.check_overlaps = True

# TAPA INFERIOR Y SUPERIOR DEL RACK
def crear_tapa(nombre, y_pos):
    tapa = sim.add_volume("Tubs", nombre)
    tapa.mother = "world"
    tapa.material = "StainlessSteel"
    tapa.rmin = 75.5 * mm
    tapa.rmax = 85.5 * mm
    tapa.dz = 0.5 * mm
    tapa.translation = [0, y_pos, 0]
    tapa.rotation = rotation_matrix
    tapa.user_info.vis = True
    tapa.user_info.color = [0.5, 0.5, 0.5, 1]
    tapa.user_info.style = "wireframe"
    tapa.user_info.check_overlaps = True

crear_tapa("tapa_inferior", -105 * mm)
crear_tapa("tapa_superior", 100.5 * mm)


# LAPIZ Co60
lapiz_co60 = sim.add_volume("Tubs", "lapiz_co60")
lapiz_co60.mother = "world"
lapiz_co60.material = "StainlessSteel"
lapiz_co60.rmin = 4.99 * mm
lapiz_co60.rmax = 5.0 * mm
lapiz_co60.dz = 100 * mm
lapiz_co60.rotation = [rotation_matrix] * 16
lapiz_co60.translation = [[80.5 * cos(radians(i * 360/16)), 0, 80.5 * sin(radians(i * 360/16))] for i in range(16)]
lapiz_co60.user_info.vis = True
lapiz_co60.user_info.color = [0.5, 0.5, 0.5, 1]
lapiz_co60.user_info.style = "solid"
lapiz_co60.user_info.check_overlaps = True


# TAPA DEL TUBO
tapa = sim.add_volume("Tubs", "tapa")
tapa.material = "Polypropilene"
tapa.rmin = 0.0 * mm
tapa.rmax = 9.5 * mm
tapa.dz = 15.5 / 2 * mm
tapa.translation = [0 * mm, 42.75 * mm, 0 * mm]
tapa.rotation = rotation_matrix
tapa.user_info.vis = True
tapa.user_info.color = [1, 1, 1, 1]  # Blanco
tapa.user_info.style = "wireframe"
tapa.user_info.check_overlaps = True

# TUBO
tubo = sim.add_volume("Tubs", "tubo")
tubo.mother = "world"
tubo.material = "Glass"
tubo.rmin = 6.52 * mm
tubo.rmax = 8.5 * mm
tubo.dz = 87. / 2 * mm
tubo.translation = [0 * mm, -9 * mm, 0 * mm]
tubo.rotation = rotation_matrix
tubo.user_info.vis = True
tubo.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo.user_info.style = "wireframe"
tubo.user_info.check_overlaps = True

# AGUA FRICKE (solucion Fricke)
aguafricke = sim.add_volume("Tubs", "aguafricke")
aguafricke.mother = "world"
aguafricke.material = "FrickeSolution"
aguafricke.rmin = 0. * mm
aguafricke.rmax = 6.52 * mm
aguafricke.dz = (75 / 2) * mm  # 37.5 mm
aguafricke.translation = [0 * mm, -15 * mm, 0 * mm]
aguafricke.rotation = rotation_matrix
aguafricke.user_info.vis = True
aguafricke.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke.user_info.style = "wireframe"
aguafricke.user_info.check_overlaps = True

sim.user_info.verbose_level = 4  # Maximo detalle

# PROCESOS DE FISICA
sim.physics_manager.physics_list_name = "QGSP_BERT_EMZ"
sim.physics_manager.energy_range_min = (1 * keV)
sim.physics_manager.energy_range_max = (3 * GeV)


# FUENTES DE Co-60 (16 lapices radiales)
#Actividad total de fuente 07/03/2023=119.20 Ci, como son 16 lapices la actividad por cada lapiz = 7.45 Ci

# Parametros generales
#actividad_total = 1000000 * Bq
#actividad_por_lapiz = actividad_total / 16
radio_fuente = 4.8 * mm
altura_fuente = 101 * mm
radio_distribucion = 80.5 * mm

# Energias discretas del Co-60
energias = [1.173228 * MeV, 1.332492 * MeV]
pesos = [1.0, 1.0]

# Crear las 16 fuentes radialmente distribuidas
for i in range(16):
    angulo_deg = i * 22.5
    theta_rad = radians(angulo_deg)
    x = radio_distribucion * cos(theta_rad)
    z = radio_distribucion * sin(theta_rad)
    
    fuente = sim.add_source("GenericSource", f"co60_lapiz_{i}")
    fuente.particle = "gamma"
    #fuente.activity = actividad_por_lapiz
    fuente.position.type = "cylinder"
    fuente.position.radius = radio_fuente
    fuente.position.dz = altura_fuente
    fuente.position.translation = [x, 0 * mm, z]
    fuente.energy.type = "spectrum_discrete"
    fuente.energy.spectrum_energies = energias
    fuente.energy.spectrum_weights = pesos
    fuente.direction.type = "iso"
    
    # Visualizacion (opcional)
    fuente.user_info.vis = True
    fuente.user_info.color = [0.0, 1.0, 0.0, 1.0]  # Verde

# Confirmacion
#print("Se han creado las 16 fuentes radiales de Co60")

# DOSE ACTOR
dose_fricke = sim.add_actor("DoseActor", "dose_fricke")
dose_fricke.attached_to = "aguafricke"
dose_fricke.dose.active = True
dose_fricke.edep.active = False
dose_fricke.hit_type = "post"
dose_fricke.dose.algorithm = "VolumeWeighting"
dose_fricke.output_filename = "dose_fricke.mhd"
dose_fricke.write_to_disk = True


# CONFIGURACION DE TIEMPO Y SEMILLA

# Tiempo de ejecucion de la simulacion 
#sim.run_timing_intervals = [(0 * s, 10 * s)]

# Motor de numeros aleatorios y semilla
sim.random_engine = "MersenneTwister"
sim.random_seed = "auto"  # Semilla automatica (diferente en cada ejecucion)
sim.user_info.verbose_level = 4 
sim.g4_verbose_level = 1        

# MODO EVENTOS DIRECTOS
sim.number_of_events = int(1e7)  # luego 1e8 y 1e9


# INICIAR LA SIMULACION EN GATE 10

# 1. Configuracion final antes de iniciar
sim.number_of_threads = 4  # Opcional: Usar multiples hilos si esta disponible
sim.force_multithread_mode = True  # <-- esto asegura que GATE/Geant4 lo aplique

# 2. Verificacion final antes de ejecutar
print("Verificacion final de la simulacion:")
print(f"- Volumenes definidos: {len(sim.volume_manager.volumes)}")
print(f"- Fuentes activas: {len(sim.source_manager.sources)}")
print(f"- Actores registrados: {len(sim.actor_manager.actors)}")

# 3. Iniciar la simulacion
print("\nIniciando simulacion...")
sim.run()
print("Simulacion finalizada.")

# 4. Post-procesamiento / resumen
print("\nResumen de la simulacion:")
#print("- Tiempo simulado: 10 s")  # Se toma del run_timing_intervals
print("- Eventos simulados: 1e7")  # Se toma del modo de eventos directos

