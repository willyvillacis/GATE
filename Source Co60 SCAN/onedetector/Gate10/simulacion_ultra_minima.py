import opengate as gate
from opengate.simulation import units as u

# Crear la simulación
sim = gate.Simulation()
sim.output_dir = "output"
sim.verbose_level = 1
sim.g4_verbose_level = 0

# Geometría: Cubo de agua
water_box = sim.add_volume("Box", "waterbox")
water_box.material = "G4_WATER"
water_box.size = [10 * u.cm, 10 * u.cm, 10 * u.cm]
water_box.translation = [0, 0, 0]

# Fuente puntual de baja actividad
src = sim.add_source("GenericSource", "test_source")
src.particle = "gamma"
src.activity = 1 * u.Bq
src.position.type = "point"
src.position.translation = [0, 0, 0]
src.energy.type = "spectrum_discrete"
src.energy.spectrum_energies = [1.25]  # MeV
src.energy.spectrum_weights = [1.0]
src.direction.type = "iso"

# Actor de dosis
actor = sim.add_actor("DoseActor", "dose_actor")
actor.attached_to = "waterbox"
actor.dose.active = True
actor.edep.active = True
actor.output_filename = "dose_test.mhd"

# Física
sim.physics_manager.physics_list_name = "QGSP_BERT_EMZ"
sim.physics_manager.energy_range_min = 1 * u.keV
sim.physics_manager.energy_range_max = 3 * u.GeV

# Tiempo de simulación ultra corto
sim.run_timing_intervals = [(0 * u.s, 0.01 * u.s)]

# Semilla aleatoria
sim.random_engine = "MersenneTwister"
sim.random_seed = "auto"

# Multithreading (opcional)
sim.number_of_threads = 4

# Lanzar simulación
print("Iniciando simulación ultra mínima...")
sim.run()
print("Simulación completada.")
