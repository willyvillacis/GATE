#!/bin/bash
# Script para ejecutar fuente3dsvp.mac con soporte multihilo

# === Configuración de rutas ===
WORKDIR="/fuente3/undetector"
MACFILE="$WORKDIR/fuente3dsvp.mac"
LOGDIR="$WORKDIR/output/log"
LOGFILE="$LOGDIR/test_jobp.log"
DMESG_LOG="$LOGDIR/dmesgp.log"
ROOT_FILE1="$WORKDIR/output/dose_fricke.txt"
ROOT_FILE2="$WORKDIR/output/stat.txt"
ROOT_FILE3="$WORKDIR/output/trajProductionStopping.txt"

# === Crear directorios si no existen ===
mkdir -p "$LOGDIR"
mkdir -p "$WORKDIR/output"

# === Verificar existencia de archivo .mac ===
if [ ! -f "$MACFILE" ]; then
  echo "Error: El archivo .mac no existe: $MACFILE" | tee -a "$LOGFILE"
  exit 1
fi

# === Preparar entorno ===
ulimit -v unlimited
ulimit -a >> "$LOGFILE"

# === Configurar número de hilos (ajustar según núcleos físicos) ===
export OMP_NUM_THREADS=4  # Probar con 4 para 128 núcleos lógicos
export G4FORCENUMBEROFTHREADS=4
export G4MULTITHREADED=1

# === Información de depuración ===
{
echo "=================================================="
echo "INICIO DE SIMULACIÓN: $(date)"
echo "Configuración del entorno:"
echo "OMP_NUM_THREADS=$OMP_NUM_THREADS"
echo "G4FORCENUMBEROFTHREADS=$G4FORCENUMBEROFTHREADS"
echo "G4MULTITHREADED=$G4MULTITHREADED"
echo "Información del sistema:"
lscpu | grep -E 'Model name|Socket|Thread|Core' || true
echo "Configuración de hilos en Geant4:"
env | grep -E 'OMP_|G4' || true
echo "Afinidad de núcleos:"
cat /proc/self/status | grep Cpus_allowed_list || true
echo "=================================================="
} >> "$LOGFILE"

# === Tiempo de inicio ===
start=$(date +%s)

echo "Iniciando simulación con $OMP_NUM_THREADS núcleos..." | tee -a "$LOGFILE"

# === Ejecutar GATE con afinidad explícita ===
cd "$WORKDIR" || exit 1
taskset -c 0-63,128-191 Gate -v "$MACFILE" >> "$LOGFILE" 2>&1

# === Tiempo de fin ===
end=$(date +%s)
duration=$((end - start))

echo "Simulación completada correctamente en $duration segundos." | tee -a "$LOGFILE"

# === Guardar salida estadística adicional ===
echo "Tiempo de ejecución (segundos): $duration" >> "$ROOT_FILE2"
echo "Fecha de finalización: $(date)" >> "$ROOT_FILE2"

# === Guardar logs del sistema ===
dmesg | tail -n 100 >> "$DMESG_LOG"

echo "Archivos generados:"
echo "- Log principal: $LOGFILE"
echo "- Dmesg: $DMESG_LOG"
echo "- Dosis: $ROOT_FILE1"
echo "- Estadísticas: $ROOT_FILE2"
echo "- Trayectorias: $ROOT_FILE3"

# Mostrar archivos generados
echo "Archivos en output:"
ls -lh /fuente3/undetector/output/