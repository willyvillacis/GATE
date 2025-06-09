import uproot
import pandas as pd
import numpy as np
import os
import sys

def export_data_from_histogram(input_file, output_file):
    try:
        # 1. Abrir archivo ROOT
        print("🔍 Abriendo archivo ROOT...")
        with uproot.open(input_file) as file:
            # 2. Acceder al árbol 'Singles;1'
            singles_tree = file["Singles;1"]
            
            # 3. Configuración del histograma (mismos parámetros que en C++)
            n_bins = 2000
            min_energy = 0.
            max_energy = 2.0
            
            # 4. Obtener datos de energía y crear histograma
            print("📊 Procesando datos de energía...")
            energy_data = singles_tree["energy"].array(library="np")
            counts, bin_edges = np.histogram(energy_data, bins=n_bins, range=(min_energy, max_energy))
            
            # 5. Calcular centros de los bins
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            
            # 6. Crear DataFrame y exportar
            print("💾 Exportando datos...")
            df = pd.DataFrame({
                "Energy": bin_centers,
                "Counts": counts
            })
            
            df.to_csv(output_file, sep='\t', index=False, header=False)
            
            # 7. Mostrar progreso simulado
            for i in range(0, 101, 5):
                print(f"\rProgreso: [{i:3d}%]", end='', flush=True)
                sys.stdout.flush()
                import time; time.sleep(0.05)
            
            print("\n✅ Exportación finalizada correctamente.")
            print(f"📁 Archivo creado: {output_file}")
            print(f"📊 Total de bins: {n_bins}")
            print(f"⚡ Rango de energía: {min_energy}-{max_energy} MeV")

    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}")
        print(f"Detalles: {str(e)}")
        if isinstance(e, uproot.exceptions.KeyInFileError):
            print("\nPosibles soluciones:")
            print("1. Verifica que el árbol se llame exactamente 'Singles;1'")
            print("2. Revisa las claves disponibles con:")
            print(f"   uproot.open('{input_file}').keys()")

# Configuración
if __name__ == "__main__":
    input_path = r"C:\William\Willy\Doctorado en FIUBA\Tesis\Datos experimentales\Simulación\GATE\EstructuraVGate 9.1\fuente2\output\testCo60_merged.root"
    output_path = r"C:\William\Willy\Doctorado en FIUBA\Tesis\Datos experimentales\Simulación\GATE\EstructuraVGate 9.1\fuente2\output\energia_cuentas.txt"
    
    export_data_from_histogram(input_path, output_path)
