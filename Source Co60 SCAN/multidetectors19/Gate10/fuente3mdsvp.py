import opengate as gate
import opengate_core as g4
import os
import numpy as np
from math import cos, sin, radians
from scipy.spatial.transform import Rotation as R

# Unidades
mm = gate.g4_units.mm
cm = gate.g4_units.cm  # Faltaba esta unidad!
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

# RACK PARA FUENTES Co60 (OPTIMIZADO)
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


#TUBOS EN ANILLO EXTERNO (12 tubos, aguafricke1 a aguafricke12)
#Tubo externo 1 (angulo = 15°)
tapa_externo_1 = sim.add_volume("Tubs", "tapa_externo_1")
tapa_externo_1.mother = "world"
tapa_externo_1.material = "Polypropilene"
tapa_externo_1.rmin = 0.0 * mm
tapa_externo_1.rmax = 9.5 * mm
tapa_externo_1.dz = 15.5 / 2 * mm
tapa_externo_1.translation = [10.077 * mm, 42.75 * mm, 37.586 * mm]  # X=39sin(15°) Y=42.75, Z=39cos(15°)
tapa_externo_1.rotation = rotation_matrix
tapa_externo_1.user_info.vis = True
tapa_externo_1.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_1.user_info.style = "wireframe"

tubo_externo_1 = sim.add_volume("Tubs", "tubo_externo_1")
tubo_externo_1.mother = "world"
tubo_externo_1.material = "Glass"
tubo_externo_1.rmin = 6.52 * mm
tubo_externo_1.rmax = 8.5 * mm
tubo_externo_1.dz = 87. / 2 * mm
tubo_externo_1.translation = [10.077 * mm, -9 * mm, 37.586 * mm]   # X=39sin(15°) Y=-9, Z=39cos(15°)
tubo_externo_1.rotation = rotation_matrix
tubo_externo_1.user_info.vis = True
tubo_externo_1.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_1.user_info.style = "wireframe"

aguafricke1 = sim.add_volume("Tubs", "aguafricke1")
aguafricke1.mother = "world"
aguafricke1.material = "FrickeSolution"
aguafricke1.rmin = 0. * mm
aguafricke1.rmax = 6.52 * mm
aguafricke1.dz = (75 / 2) * mm  # 37.5 mm
aguafricke1.translation = [10.077 * mm, -15 * mm, 37.586 * mm]  # X=39sin(15°) Y=-15, Z=39cos(15°)
aguafricke1.rotation = rotation_matrix
aguafricke1.user_info.vis = True
aguafricke1.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke1.user_info.style = "wireframe"

#Tubo externo 2 (angulo = 45°)
tapa_externo_2 = sim.add_volume("Tubs", "tapa_externo_2")
tapa_externo_2.mother = "world"
tapa_externo_2.material = "Polypropilene"
tapa_externo_2.rmin = 0.0 * mm
tapa_externo_2.rmax = 9.5 * mm
tapa_externo_2.dz = 15.5 / 2 * mm
tapa_externo_2.translation = [27.577 * mm, 42.75 * mm, 27.577 * mm]  # X=39sin(45°) Y=42.75, Z=39cos(45°)
tapa_externo_2.rotation = rotation_matrix
tapa_externo_2.user_info.vis = True
tapa_externo_2.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_2.user_info.style = "wireframe"

tubo_externo_2 = sim.add_volume("Tubs", "tubo_externo_2")
tubo_externo_2.mother = "world"
tubo_externo_2.material = "Glass"
tubo_externo_2.rmin = 6.52 * mm
tubo_externo_2.rmax = 8.5 * mm
tubo_externo_2.dz = 87. / 2 * mm
tubo_externo_2.translation = [27.577 * mm, -9 * mm, 27.577 * mm]   # X=39sin(45°) Y=-9, Z=39cos(45°)
tubo_externo_2.rotation = rotation_matrix
tubo_externo_2.user_info.vis = True
tubo_externo_2.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_2.user_info.style = "wireframe"

aguafricke2 = sim.add_volume("Tubs", "aguafricke2")
aguafricke2.mother = "world"
aguafricke2.material = "FrickeSolution"
aguafricke2.rmin = 0. * mm
aguafricke2.rmax = 6.52 * mm
aguafricke2.dz = (75 / 2) * mm  # 37.5 mm
aguafricke2.translation = [27.577 * mm, -15 * mm, 27.577 * mm]  # X=39sin(45°) Y=-15, Z=39cos(45°)
aguafricke2.rotation = rotation_matrix
aguafricke2.user_info.vis = True
aguafricke2.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke2.user_info.style = "wireframe"

#Tubo externo 3 (angulo = 75°)
tapa_externo_3 = sim.add_volume("Tubs", "tapa_externo_3")
tapa_externo_3.mother = "world"
tapa_externo_3.material = "Polypropilene"
tapa_externo_3.rmin = 0.0 * mm
tapa_externo_3.rmax = 9.5 * mm
tapa_externo_3.dz = 15.5 / 2 * mm
tapa_externo_3.translation = [37.586 * mm, 42.75 * mm, 10.077 * mm]  # X=39sin(75°) Y=42.75, Z=39cos(75°)
tapa_externo_3.rotation = rotation_matrix
tapa_externo_3.user_info.vis = True
tapa_externo_3.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_3.user_info.style = "wireframe"

tubo_externo_3 = sim.add_volume("Tubs", "tubo_externo_3")
tubo_externo_3.mother = "world"
tubo_externo_3.material = "Glass"
tubo_externo_3.rmin = 6.52 * mm
tubo_externo_3.rmax = 8.5 * mm
tubo_externo_3.dz = 87. / 2 * mm
tubo_externo_3.translation = [37.586 * mm, -9 * mm, 10.077 * mm]   # X=39sin(75°) Y=-9, Z=39cos(75°)
tubo_externo_3.rotation = rotation_matrix
tubo_externo_3.user_info.vis = True
tubo_externo_3.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_3.user_info.style = "wireframe"

aguafricke3 = sim.add_volume("Tubs", "aguafricke3")
aguafricke3.mother = "world"
aguafricke3.material = "FrickeSolution"
aguafricke3.rmin = 0. * mm
aguafricke3.rmax = 6.52 * mm
aguafricke3.dz = (75 / 2) * mm  # 37.5 mm
aguafricke3.translation = [37.586 * mm, -15 * mm, 10.077 * mm]  # X=39sin(75°) Y=-15, Z=39cos(75°)
aguafricke3.rotation = rotation_matrix
aguafricke3.user_info.vis = True
aguafricke3.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke3.user_info.style = "wireframe"

#Tubo externo 4 (angulo = 105°)
tapa_externo_4 = sim.add_volume("Tubs", "tapa_externo_4")
tapa_externo_4.mother = "world"
tapa_externo_4.material = "Polypropilene"
tapa_externo_4.rmin = 0.0 * mm
tapa_externo_4.rmax = 9.5 * mm
tapa_externo_4.dz = 15.5 / 2 * mm
tapa_externo_4.translation = [37.586 * mm, 42.75 * mm, -10.077 * mm]  # X=39sin(105°) Y=42.75, Z=39cos(105°)
rotation_matrix = rot.as_matrix()
tapa_externo_4.rotation = rotation_matrix
tapa_externo_4.user_info.vis = True
tapa_externo_4.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_4.user_info.style = "wireframe"

tubo_externo_4 = sim.add_volume("Tubs", "tubo_externo_4")
tubo_externo_4.mother = "world"
tubo_externo_4.material = "Glass"
tubo_externo_4.rmin = 6.52 * mm
tubo_externo_4.rmax = 8.5 * mm
tubo_externo_4.dz = 87. / 2 * mm
tubo_externo_4.translation = [37.586 * mm, -9 * mm, -10.077 * mm]   # X=39sin(105°) Y=-9, Z=39cos(105°)
tubo_externo_4.rotation = rotation_matrix
tubo_externo_4.user_info.vis = True
tubo_externo_4.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_4.user_info.style = "wireframe"

aguafricke4 = sim.add_volume("Tubs", "aguafricke4")
aguafricke4.mother = "world"
aguafricke4.material = "FrickeSolution"
aguafricke4.rmin = 0. * mm
aguafricke4.rmax = 6.52 * mm
aguafricke4.dz = (75 / 2) * mm  # 37.5 mm
aguafricke4.translation = [37.586 * mm, -15 * mm, -10.077 * mm]  # X=39sin(105°) Y=-15, Z=39cos(105°)
rotation_matrix = rot.as_matrix()
aguafricke4.rotation = rotation_matrix
aguafricke4.user_info.vis = True
aguafricke4.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke4.user_info.style = "wireframe"

#Tubo externo 5 (angulo = 135°)
tapa_externo_5 = sim.add_volume("Tubs", "tapa_externo_5")
tapa_externo_5.mother = "world"
tapa_externo_5.material = "Polypropilene"
tapa_externo_5.rmin = 0.0 * mm
tapa_externo_5.rmax = 9.5 * mm
tapa_externo_5.dz = 15.5 / 2 * mm
tapa_externo_5.translation = [27.577 * mm, 42.75 * mm, -27.577 * mm]  # X=39sin(135°) Y=42.75, Z=39cos(135°)
tapa_externo_5.rotation = rotation_matrix
tapa_externo_5.user_info.vis = True
tapa_externo_5.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_5.user_info.style = "wireframe"

tubo_externo_5 = sim.add_volume("Tubs", "tubo_externo_5")
tubo_externo_5.mother = "world"
tubo_externo_5.material = "Glass"
tubo_externo_5.rmin = 6.52 * mm
tubo_externo_5.rmax = 8.5 * mm
tubo_externo_5.dz = 87. / 2 * mm
tubo_externo_5.translation = [27.577 * mm, -9 * mm, -27.577 * mm]   # X=39sin(135°) Y=-9, Z=39cos(135°)
tubo_externo_5.rotation = rotation_matrix
tubo_externo_5.user_info.vis = True
tubo_externo_5.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_5.user_info.style = "wireframe"

aguafricke5 = sim.add_volume("Tubs", "aguafricke5")
aguafricke5.mother = "world"
aguafricke5.material = "FrickeSolution"
aguafricke5.rmin = 0. * mm
aguafricke5.rmax = 6.52 * mm
aguafricke5.dz = (75 / 2) * mm  # 37.5 mm
aguafricke5.translation = [27.577 * mm, -15 * mm, -27.577 * mm]  # X=39sin(135°) Y=-15, Z=39cos(135°)
aguafricke5.rotation = rotation_matrix
aguafricke5.user_info.vis = True
aguafricke5.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke5.user_info.style = "wireframe"

#Tubo externo 6 (angulo = 165°)
tapa_externo_6 = sim.add_volume("Tubs", "tapa_externo_6")
tapa_externo_6.mother = "world"
tapa_externo_6.material = "Polypropilene"
tapa_externo_6.rmin = 0.0 * mm
tapa_externo_6.rmax = 9.5 * mm
tapa_externo_6.dz = 15.5 / 2 * mm
tapa_externo_6.translation = [10.077 * mm, 42.75 * mm, -37.586 * mm]  # X=39sin(165°) Y=42.75, Z=39cos(165°)
tapa_externo_6.rotation = rotation_matrix
tapa_externo_6.user_info.vis = True
tapa_externo_6.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_6.user_info.style = "wireframe"

tubo_externo_6 = sim.add_volume("Tubs", "tubo_externo_6")
tubo_externo_6.mother = "world"
tubo_externo_6.material = "Glass"
tubo_externo_6.rmin = 6.52 * mm
tubo_externo_6.rmax = 8.5 * mm
tubo_externo_6.dz = 87. / 2 * mm
tubo_externo_6.translation = [10.077 * mm, -9 * mm, -37.586 * mm]   # X=39sin(165°) Y=-9, Z=39cos(165°)
tubo_externo_6.rotation = rotation_matrix
tubo_externo_6.user_info.vis = True
tubo_externo_6.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_6.user_info.style = "wireframe"

aguafricke6 = sim.add_volume("Tubs", "aguafricke6")
aguafricke6.mother = "world"
aguafricke6.material = "FrickeSolution"
aguafricke6.rmin = 0. * mm
aguafricke6.rmax = 6.52 * mm
aguafricke6.dz = (75 / 2) * mm  # 37.5 mm
aguafricke6.translation = [10.077 * mm, -15 * mm, -37.586 * mm]  # X=39sin(165°) Y=-15, Z=39cos(165°)
aguafricke6.rotation = rotation_matrix
aguafricke6.user_info.vis = True
aguafricke6.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke6.user_info.style = "wireframe"

#Tubo externo 7 (angulo = 195°)
tapa_externo_7 = sim.add_volume("Tubs", "tapa_externo_7")
tapa_externo_7.mother = "world"
tapa_externo_7.material = "Polypropilene"
tapa_externo_7.rmin = 0.0 * mm
tapa_externo_7.rmax = 9.5 * mm
tapa_externo_7.dz = 15.5 / 2 * mm
tapa_externo_7.translation = [-10.077 * mm, 42.75 * mm, -37.586 * mm]  # X=39sin(195°) Y=42.75, Z=39cos(195°)
tapa_externo_7.rotation = rotation_matrix
tapa_externo_7.user_info.vis = True
tapa_externo_7.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_7.user_info.style = "wireframe"

tubo_externo_7 = sim.add_volume("Tubs", "tubo_externo_7")
tubo_externo_7.mother = "world"
tubo_externo_7.material = "Glass"
tubo_externo_7.rmin = 6.52 * mm
tubo_externo_7.rmax = 8.5 * mm
tubo_externo_7.dz = 87. / 2 * mm
tubo_externo_7.translation = [-10.077 * mm, -9 * mm, -37.586 * mm]   # X=39sin(195°) Y=-9, Z=39cos(195°)
tubo_externo_7.rotation = rotation_matrix
tubo_externo_7.user_info.vis = True
tubo_externo_7.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_7.user_info.style = "wireframe"

aguafricke7 = sim.add_volume("Tubs", "aguafricke7")
aguafricke7.mother = "world"
aguafricke7.material = "FrickeSolution"
aguafricke7.rmin = 0. * mm
aguafricke7.rmax = 6.52 * mm
aguafricke7.dz = (75 / 2) * mm  # 37.5 mm
aguafricke7.translation = [-10.077 * mm, -15 * mm, -37.586 * mm]  # X=39sin(195°) Y=-15, Z=39cos(195°)
aguafricke7.rotation = rotation_matrix
aguafricke7.user_info.vis = True
aguafricke7.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke7.user_info.style = "wireframe"

#Tubo externo 8 (angulo = 225°)
tapa_externo_8 = sim.add_volume("Tubs", "tapa_externo_8")
tapa_externo_8.mother = "world"
tapa_externo_8.material = "Polypropilene"
tapa_externo_8.rmin = 0.0 * mm
tapa_externo_8.rmax = 9.5 * mm
tapa_externo_8.dz = 15.5 / 2 * mm
tapa_externo_8.translation = [-27.577 * mm, 42.75 * mm, -27.577 * mm]  # X=39sin(225°) Y=42.75, Z=39cos(225°)
tapa_externo_8.rotation = rotation_matrix
tapa_externo_8.user_info.vis = True
tapa_externo_8.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_8.user_info.style = "wireframe"

tubo_externo_8 = sim.add_volume("Tubs", "tubo_externo_8")
tubo_externo_8.mother = "world"
tubo_externo_8.material = "Glass"
tubo_externo_8.rmin = 6.52 * mm
tubo_externo_8.rmax = 8.5 * mm
tubo_externo_8.dz = 87. / 2 * mm
tubo_externo_8.translation = [-27.577 * mm, -9 * mm, -27.577 * mm]   # X=39sin(225°) Y=-9, Z=39cos(225°)
tubo_externo_8.rotation = rotation_matrix
tubo_externo_8.user_info.vis = True
tubo_externo_8.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_8.user_info.style = "wireframe"

aguafricke8 = sim.add_volume("Tubs", "aguafricke8")
aguafricke8.mother = "world"
aguafricke8.material = "FrickeSolution"
aguafricke8.rmin = 0. * mm
aguafricke8.rmax = 6.52 * mm
aguafricke8.dz = (75 / 2) * mm  # 37.5 mm
aguafricke8.translation = [-27.577 * mm, -15 * mm, -27.577 * mm]  # X=39sin(225Â°) Y=-15, Z=39cos(225Â°)
aguafricke8.rotation = rotation_matrix
aguafricke8.user_info.vis = True
aguafricke8.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke8.user_info.style = "wireframe"

#Tubo externo 9 (angulo = 255°)
tapa_externo_9 = sim.add_volume("Tubs", "tapa_externo_9")
tapa_externo_9.mother = "world"
tapa_externo_9.material = "Polypropilene"
tapa_externo_9.rmin = 0.0 * mm
tapa_externo_9.rmax = 9.5 * mm
tapa_externo_9.dz = 15.5 / 2 * mm
tapa_externo_9.translation = [-37.586 * mm, 42.75 * mm, -10.077 * mm]  # X=39sin(255°) Y=42.75, Z=39cos(255°)
tapa_externo_9.rotation = rotation_matrix
tapa_externo_9.user_info.vis = True
tapa_externo_9.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_9.user_info.style = "wireframe"

tubo_externo_9 = sim.add_volume("Tubs", "tubo_externo_9")
tubo_externo_9.mother = "world"
tubo_externo_9.material = "Glass"
tubo_externo_9.rmin = 6.52 * mm
tubo_externo_9.rmax = 8.5 * mm
tubo_externo_9.dz = 87. / 2 * mm
tubo_externo_9.translation = [-37.586 * mm, -9 * mm, -10.077 * mm]   # X=39sin(255°) Y=-9, Z=39cos(255°)
tubo_externo_9.rotation = rotation_matrix
tubo_externo_9.user_info.vis = True
tubo_externo_9.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_9.user_info.style = "wireframe"

aguafricke9 = sim.add_volume("Tubs", "aguafricke9")
aguafricke9.mother = "world"
aguafricke9.material = "FrickeSolution"
aguafricke9.rmin = 0. * mm
aguafricke9.rmax = 6.52 * mm
aguafricke9.dz = (75 / 2) * mm  # 37.5 mm
aguafricke9.translation = [-37.586 * mm, -15 * mm, -10.077 * mm]  # X=39sin(255°) Y=-15, Z=39cos(255°)
aguafricke9.rotation = rotation_matrix
aguafricke9.user_info.vis = True
aguafricke9.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke9.user_info.style = "wireframe"

#Tubo externo 10 (angulo = 285°)
tapa_externo_10 = sim.add_volume("Tubs", "tapa_externo_10")
tapa_externo_10.mother = "world"
tapa_externo_10.material = "Polypropilene"
tapa_externo_10.rmin = 0.0 * mm
tapa_externo_10.rmax = 9.5 * mm
tapa_externo_10.dz = 15.5 / 2 * mm
tapa_externo_10.translation = [-37.586 * mm, 42.75 * mm, 10.077 * mm]  # X=39sin(285°) Y=42.75, Z=39cos(285°)
tapa_externo_10.rotation = rotation_matrix
tapa_externo_10.user_info.vis = True
tapa_externo_10.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_10.user_info.style = "wireframe"

tubo_externo_10 = sim.add_volume("Tubs", "tubo_externo_10")
tubo_externo_10.mother = "world"
tubo_externo_10.material = "Glass"
tubo_externo_10.rmin = 6.52 * mm
tubo_externo_10.rmax = 8.5 * mm
tubo_externo_10.dz = 87. / 2 * mm
tubo_externo_10.translation = [-37.586 * mm, -9 * mm, 10.077 * mm]   # X=39sin(285°) Y=-9, Z=39cos(285°)
tubo_externo_10.rotation = rotation_matrix
tubo_externo_10.user_info.vis = True
tubo_externo_10.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_10.user_info.style = "wireframe"

aguafricke10 = sim.add_volume("Tubs", "aguafricke10")
aguafricke10.mother = "world"
aguafricke10.material = "FrickeSolution"
aguafricke10.rmin = 0. * mm
aguafricke10.rmax = 6.52 * mm
aguafricke10.dz = (75 / 2) * mm  # 37.5 mm
aguafricke10.translation = [-37.586 * mm, -15 * mm, 10.077 * mm]  # X=39sin(285°) Y=-15, Z=39cos(285°)
aguafricke10.rotation = rotation_matrix
aguafricke10.user_info.vis = True
aguafricke10.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke10.user_info.style = "wireframe"

#Tubo externo 11 (angulo = 315°)
tapa_externo_11 = sim.add_volume("Tubs", "tapa_externo_11")
tapa_externo_11.mother = "world"
tapa_externo_11.material = "Polypropilene"
tapa_externo_11.rmin = 0.0 * mm
tapa_externo_11.rmax = 9.5 * mm
tapa_externo_11.dz = 15.5 / 2 * mm
tapa_externo_11.translation = [-27.577 * mm, 42.75 * mm, 27.577 * mm]  # X=39sin(315°) Y=42.75, Z=39cos(315°)
tapa_externo_11.rotation = rotation_matrix
tapa_externo_11.user_info.vis = True
tapa_externo_11.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_11.user_info.style = "wireframe"

tubo_externo_11 = sim.add_volume("Tubs", "tubo_externo_11")
tubo_externo_11.mother = "world"
tubo_externo_11.material = "Glass"
tubo_externo_11.rmin = 6.52 * mm
tubo_externo_11.rmax = 8.5 * mm
tubo_externo_11.dz = 87. / 2 * mm
tubo_externo_11.translation = [-27.577 * mm, -9 * mm, 27.577 * mm]   # X=39sin(315°) Y=-9, Z=39cos(315°)
tubo_externo_11.rotation = rotation_matrix
tubo_externo_11.user_info.vis = True
tubo_externo_11.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_11.user_info.style = "wireframe"

aguafricke11 = sim.add_volume("Tubs", "aguafricke11")
aguafricke11.mother = "world"
aguafricke11.material = "FrickeSolution"
aguafricke11.rmin = 0. * mm
aguafricke11.rmax = 6.52 * mm
aguafricke11.dz = (75 / 2) * mm  # 37.5 mm
aguafricke11.translation = [-27.577 * mm, -15 * mm, 27.577 * mm]  # X=39sin(315°) Y=-15, Z=39cos(315°)
aguafricke11.rotation = rotation_matrix
aguafricke11.user_info.vis = True
aguafricke11.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke11.user_info.style = "wireframe"

#Tubo externo 12 (angulo = 345°)
tapa_externo_12 = sim.add_volume("Tubs", "tapa_externo_12")
tapa_externo_12.mother = "world"
tapa_externo_12.material = "Polypropilene"
tapa_externo_12.rmin = 0.0 * mm
tapa_externo_12.rmax = 9.5 * mm
tapa_externo_12.dz = 15.5 / 2 * mm
tapa_externo_12.translation = [-10.077 * mm, 42.75 * mm, 37.586 * mm]  # X=39sin(345°) Y=42.75, Z=39cos(345°)
tapa_externo_12.rotation = rotation_matrix
tapa_externo_12.user_info.vis = True
tapa_externo_12.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_externo_12.user_info.style = "wireframe"

tubo_externo_12 = sim.add_volume("Tubs", "tubo_externo_12")
tubo_externo_12.mother = "world"
tubo_externo_12.material = "Glass"
tubo_externo_12.rmin = 6.52 * mm
tubo_externo_12.rmax = 8.5 * mm
tubo_externo_12.dz = 87. / 2 * mm
tubo_externo_12.translation = [-10.077 * mm, -9 * mm, 37.586 * mm]   # X=39sin(345°) Y=-9, Z=39cos(345°)
tubo_externo_12.rotation = rotation_matrix
tubo_externo_12.user_info.vis = True
tubo_externo_12.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_externo_12.user_info.style = "wireframe"

aguafricke12 = sim.add_volume("Tubs", "aguafricke12")
aguafricke12.mother = "world"
aguafricke12.material = "FrickeSolution"
aguafricke12.rmin = 0. * mm
aguafricke12.rmax = 6.52 * mm
aguafricke12.dz = (75 / 2) * mm  # 37.5 mm
aguafricke12.translation = [-10.077 * mm, -15 * mm, 37.586 * mm]  # X=39sin(345°) Y=-15, Z=39cos(345°)
aguafricke12.rotation = rotation_matrix
aguafricke12.user_info.vis = True
aguafricke12.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke12.user_info.style = "wireframe"

#TUBOS EN ANILLO INTERNO (6 tubos, aguafricke13 a aguafricke18)
#Tubo interno 1 (angulo = 0°)
tapa_interno_1 = sim.add_volume("Tubs", "tapa_interno_1")
tapa_interno_1.mother = "world"
tapa_interno_1.material = "Polypropilene"
tapa_interno_1.rmin = 0.0 * mm
tapa_interno_1.rmax = 9.5 * mm
tapa_interno_1.dz = 15.5 / 2 * mm
tapa_interno_1.translation = [0 * mm, 42.75 * mm, 20.5 * mm]  # X=20.5sin(0°), Y=42.75, Z=20.5cos(0°)
tapa_interno_1.rotation = rotation_matrix
tapa_interno_1.user_info.vis = True
tapa_interno_1.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_interno_1.user_info.style = "wireframe"

tubo_interno_1 = sim.add_volume("Tubs", "tubo_interno_1")
tubo_interno_1.mother = "world"
tubo_interno_1.material = "Glass"
tubo_interno_1.rmin = 6.52 * mm
tubo_interno_1.rmax = 8.5 * mm
tubo_interno_1.dz = 87. / 2 * mm
tubo_interno_1.translation = [0 * mm, -9 * mm, 20.5 * mm]   # X=20.5sin(0°), Y=-9, Z=20.5cos(0°)
tubo_interno_1.rotation = rotation_matrix
tubo_interno_1.user_info.vis = True
tubo_interno_1.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_interno_1.user_info.style = "wireframe"

aguafricke13 = sim.add_volume("Tubs", "aguafricke13")
aguafricke13.mother = "world"
aguafricke13.material = "FrickeSolution"
aguafricke13.rmin = 0. * mm
aguafricke13.rmax = 6.52 * mm
aguafricke13.dz = (75 / 2) * mm  # 37.5 mm
aguafricke13.translation = [0 * mm, -15 * mm, 20.5 * mm]  # X=20.5sin(0°), Y=-15, Z=20.5cos(0°)
aguafricke13.rotation = rotation_matrix
aguafricke13.user_info.vis = True
aguafricke13.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke13.user_info.style = "wireframe"

#Tubo interno 2 (angulo = 60°)
tapa_interno_2 = sim.add_volume("Tubs", "tapa_interno_2")
tapa_interno_2.mother = "world"
tapa_interno_2.material = "Polypropilene"
tapa_interno_2.rmin = 0.0 * mm
tapa_interno_2.rmax = 9.5 * mm
tapa_interno_2.dz = 15.5 / 2 * mm
tapa_interno_2.translation = [17.753 * mm, 42.75 * mm, 10.25 * mm]  # X=20.5sin(60°), Y=42.75, Z=20.5cos(60°)
tapa_interno_2.rotation = rotation_matrix
tapa_interno_2.user_info.vis = True
tapa_interno_2.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_interno_2.user_info.style = "wireframe"

tubo_interno_2 = sim.add_volume("Tubs", "tubo_interno_2")
tubo_interno_2.mother = "world"
tubo_interno_2.material = "Glass"
tubo_interno_2.rmin = 6.52 * mm
tubo_interno_2.rmax = 8.5 * mm
tubo_interno_2.dz = 87. / 2 * mm
tubo_interno_2.translation = [17.753 * mm, -9 * mm, 10.25 * mm]   # X=20.5sin(60Â°), Y=-9, Z=20.5cos(60Â°)
tubo_interno_2.rotation = rotation_matrix
tubo_interno_2.user_info.vis = True
tubo_interno_2.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_interno_2.user_info.style = "wireframe"

aguafricke14 = sim.add_volume("Tubs", "aguafricke14")
aguafricke14.mother = "world"
aguafricke14.material = "FrickeSolution"
aguafricke14.rmin = 0. * mm
aguafricke14.rmax = 6.52 * mm
aguafricke14.dz = (75 / 2) * mm  # 37.5 mm
aguafricke14.translation = [17.753 * mm, -15 * mm, 10.25 * mm]  # X=20.5sin(60°), Y=-15, Z=20.5cos(60°)
aguafricke14.rotation = rotation_matrix
aguafricke14.user_info.vis = True
aguafricke14.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke14.user_info.style = "wireframe"

#Tubo interno 3 (angulo = 120°)
tapa_interno_3 = sim.add_volume("Tubs", "tapa_interno_3")
tapa_interno_3.mother = "world"
tapa_interno_3.material = "Polypropilene"
tapa_interno_3.rmin = 0.0 * mm
tapa_interno_3.rmax = 9.5 * mm
tapa_interno_3.dz = 15.5 / 2 * mm
tapa_interno_3.translation = [17.753 * mm, 42.75 * mm, -10.25 * mm]  # X=20.5sin(120°), Y=42.75, Z=20.5cos(120°)
tapa_interno_3.rotation = rotation_matrix
tapa_interno_3.user_info.vis = True
tapa_interno_3.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_interno_3.user_info.style = "wireframe"

tubo_interno_3 = sim.add_volume("Tubs", "tubo_interno_3")
tubo_interno_3.mother = "world"
tubo_interno_3.material = "Glass"
tubo_interno_3.rmin = 6.52 * mm
tubo_interno_3.rmax = 8.5 * mm
tubo_interno_3.dz = 87. / 2 * mm
tubo_interno_3.translation = [17.753 * mm, -9 * mm, -10.25 * mm]   # X=20.5sin(120°), Y=-9, Z=20.5cos(120°)
tubo_interno_3.rotation = rotation_matrix
tubo_interno_3.user_info.vis = True
tubo_interno_3.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_interno_3.user_info.style = "wireframe"

aguafricke15 = sim.add_volume("Tubs", "aguafricke15")
aguafricke15.mother = "world"
aguafricke15.material = "FrickeSolution"
aguafricke15.rmin = 0. * mm
aguafricke15.rmax = 6.52 * mm
aguafricke15.dz = (75 / 2) * mm  # 37.5 mm
aguafricke15.translation = [17.753 * mm, -15 * mm, -10.25 * mm]  # X=20.5sin(120°), Y=-15, Z=20.5cos(120°)
aguafricke15.rotation = rotation_matrix
aguafricke15.user_info.vis = True
aguafricke15.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke15.user_info.style = "wireframe"

#Tubo interno 4 (angulo = 180°)
tapa_interno_4 = sim.add_volume("Tubs", "tapa_interno_4")
tapa_interno_4.mother = "world"
tapa_interno_4.material = "Polypropilene"
tapa_interno_4.rmin = 0.0 * mm
tapa_interno_4.rmax = 9.5 * mm
tapa_interno_4.dz = 15.5 / 2 * mm
tapa_interno_4.translation = [0 * mm, 42.75 * mm, -20.5 * mm]  # X=20.5sin(180°), Y=42.75, Z=20.5cos(180°)
tapa_interno_4.rotation = rotation_matrix
tapa_interno_4.user_info.vis = True
tapa_interno_4.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_interno_4.user_info.style = "wireframe"

tubo_interno_4 = sim.add_volume("Tubs", "tubo_interno_4")
tubo_interno_4.mother = "world"
tubo_interno_4.material = "Glass"
tubo_interno_4.rmin = 6.52 * mm
tubo_interno_4.rmax = 8.5 * mm
tubo_interno_4.dz = 87. / 2 * mm
tubo_interno_4.translation = [0 * mm, -9 * mm, -20.5 * mm]   # X=20.5sin(180°), Y=-9, Z=20.5cos(180°)
tubo_interno_4.rotation = rotation_matrix
tubo_interno_4.user_info.vis = True
tubo_interno_4.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_interno_4.user_info.style = "wireframe"

aguafricke16 = sim.add_volume("Tubs", "aguafricke16")
aguafricke16.mother = "world"
aguafricke16.material = "FrickeSolution"
aguafricke16.rmin = 0. * mm
aguafricke16.rmax = 6.52 * mm
aguafricke16.dz = (75 / 2) * mm  # 37.5 mm
aguafricke16.translation = [0 * mm, -15 * mm, -20.5 * mm]  # X=20.5sin(180°), Y=-15, Z=20.5cos(180°)
aguafricke16.rotation = rotation_matrix
aguafricke16.user_info.vis = True
aguafricke16.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke16.user_info.style = "wireframe"

#Tubo interno 5 (angulo = 240°)
tapa_interno_5 = sim.add_volume("Tubs", "tapa_interno_5")
tapa_interno_5.mother = "world"
tapa_interno_5.material = "Polypropilene"
tapa_interno_5.rmin = 0.0 * mm
tapa_interno_5.rmax = 9.5 * mm
tapa_interno_5.dz = 15.5 / 2 * mm
tapa_interno_5.translation = [-17.753 * mm, 42.75 * mm, -10.25 * mm]  # X=20.5sin(240°), Y=42.75, Z=20.5cos(240°)
tapa_interno_5.rotation = rotation_matrix
tapa_interno_5.user_info.vis = True
tapa_interno_5.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_interno_5.user_info.style = "wireframe"

tubo_interno_5 = sim.add_volume("Tubs", "tubo_interno_5")
tubo_interno_5.mother = "world"
tubo_interno_5.material = "Glass"
tubo_interno_5.rmin = 6.52 * mm
tubo_interno_5.rmax = 8.5 * mm
tubo_interno_5.dz = 87. / 2 * mm
tubo_interno_5.translation = [-17.753 * mm, -9 * mm, -10.25 * mm]   # X=20.5sin(240°), Y=-9, Z=20.5cos(240°)
tubo_interno_5.rotation = rotation_matrix
tubo_interno_4.user_info.vis = True
tubo_interno_4.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_interno_4.user_info.style = "wireframe"

aguafricke17 = sim.add_volume("Tubs", "aguafricke17")
aguafricke17.mother = "world"
aguafricke17.material = "FrickeSolution"
aguafricke17.rmin = 0. * mm
aguafricke17.rmax = 6.52 * mm
aguafricke17.dz = (75 / 2) * mm  # 37.5 mm
aguafricke17.translation = [-17.753 * mm, -15 * mm, -10.25 * mm]  # X=20.5sin(240°), Y=-15, Z=20.5cos(240°)
aguafricke17.rotation = rotation_matrix
aguafricke17.user_info.vis = True
aguafricke17.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke17.user_info.style = "wireframe"

#Tubo interno 6 (angulo = 300°)
tapa_interno_6 = sim.add_volume("Tubs", "tapa_interno_6")
tapa_interno_6.mother = "world"
tapa_interno_6.material = "Polypropilene"
tapa_interno_6.rmin = 0.0 * mm
tapa_interno_6.rmax = 9.5 * mm
tapa_interno_6.dz = 15.5 / 2 * mm
tapa_interno_6.translation = [-17.753 * mm, 42.75 * mm, 10.25 * mm]  # X=20.5sin(300°), Y=42.75, Z=20.5cos(300°)
tapa_interno_6.rotation = rotation_matrix
tapa_interno_6.user_info.vis = True
tapa_interno_6.user_info.color = [1, 1, 1, 1]  # Blanco
tapa_interno_6.user_info.style = "wireframe"

tubo_interno_6 = sim.add_volume("Tubs", "tubo_interno_6")
tubo_interno_6.mother = "world"
tubo_interno_6.material = "Glass"
tubo_interno_6.rmin = 6.52 * mm
tubo_interno_6.rmax = 8.5 * mm
tubo_interno_6.dz = 87. / 2 * mm
tubo_interno_6.translation = [-17.753 * mm, -9 * mm, 10.25 * mm]   # X=20.5sin(300°), Y=-9, Z=20.5cos(300°)
tubo_interno_6.rotation = rotation_matrix
tubo_interno_6.user_info.vis = True
tubo_interno_6.user_info.color = [0.5, 0.5, 0.5, 1]  # Gris
tubo_interno_6.user_info.style = "wireframe"

aguafricke18 = sim.add_volume("Tubs", "aguafricke18")
aguafricke18.mother = "world"
aguafricke18.material = "FrickeSolution"
aguafricke18.rmin = 0. * mm
aguafricke18.rmax = 6.52 * mm
aguafricke18.dz = (75 / 2) * mm  # 37.5 mm
aguafricke18.translation = [-17.753 * mm, -15 * mm, 10.25 * mm]  # X=20.5sin(300°), Y=-15, Z=20.5cos(300°)
aguafricke18.rotation = rotation_matrix
aguafricke18.user_info.vis = True
aguafricke18.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke18.user_info.style = "wireframe"

#TUBO CENTRAL (aguafricke19)
# Tapa del tubo central
tapa = sim.add_volume("Tubs", "tapa")
tapa.mother = "world"
tapa.material = "Polypropilene"
tapa.rmin = 0.0 * mm
tapa.rmax = 9.5 * mm
tapa.dz = 15.5 / 2 * mm
tapa.translation = [0 * mm, 42.75 * mm, 0 * mm]
tapa.rotation = rotation_matrix
tapa.user_info.vis = True
tapa.user_info.color = [1, 1, 1, 1]  # Blanco
tapa.user_info.style = "wireframe"

#Tubo central (ya definido, ajustado como hija del mundo)
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

# AGUA FRICKE (aguafricke19)(detector) (la altura 75.00 mm es acorde a volumen colocado en la experimentacion)
aguafricke19 = sim.add_volume("Tubs", "aguafricke19")
aguafricke19.mother = "world"
aguafricke19.material = "FrickeSolution"
aguafricke19.rmin = 0. * mm
aguafricke19.rmax = 6.52 * mm
aguafricke19.dz = (75 / 2) * mm  # 37.5 mm
aguafricke19.translation = [0 * mm, -15 * mm, 0 * mm]
aguafricke19.rotation = rotation_matrix
aguafricke19.user_info.vis = True
aguafricke19.user_info.color = [0.0, 0.0, 1.0, 1.0]  # Azul
aguafricke19.user_info.style = "wireframe"

sim.user_info.verbose_level = 4  # Maximo detalle

# PROCESOS DE FISICA
sim.physics_manager.physics_list_name = "QGSP_BERT_EMZ"
sim.physics_manager.energy_range_min = (1 * keV)
sim.physics_manager.energy_range_max = (3 * GeV)

# FUENTES DE Co-60 (16 lapices radiales)
#Actividad total de fuente 07/03/2023=119.20 Ci, como son 16 lapices la actividad por cada lapiz = 7.45 Ci

# Parametros generales
actividad_total = 1e6 * Bq
actividad_por_lapiz = actividad_total / 16
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
    fuente.activity = actividad_por_lapiz
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

for i in range(1, 20):  # De 1 a 19 inclusive
    actor = sim.add_actor("DoseActor", f"dose_fricke{i}")
    actor.attached_to = f"aguafricke{i}"
    actor.dose.active = True
    actor.edep.active = False
    actor.hit_type = "post"
    actor.dose.algorithm = "VolumeWeighting"
    actor.output_filename = f"detector{i}/dose_fricke{i}.mhd"
    actor.write_to_disk = True


# CONFIGURACION DE TIEMPO Y SEMILLA

# Tiempo de ejecucion de la simulacion 
sim.run_timing_intervals = [(0 * s, 10 * s)]

# Motor de numeros aleatorios y semilla
sim.random_engine = "MersenneTwister"
sim.random_seed = "auto"  # Semilla automatica (diferente en cada ejecucion)
sim.user_info.verbose_level = 4 
sim.g4_verbose_level = 1        


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
print("- Tiempo simulado: 10 s")  # Se toma del run_timing_intervals
