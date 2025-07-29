#!/bin/bash
# Script para ejecutar fuente3mdsvp.mac con 1 núcleo y 19 detectores

# === Configuración de rutas ===
WORKDIR="/fuente3/mdetectores"
MACFILE="$WORKDIR/fuente3mdsvp.mac"
LOGDIR="$WORKDIR/output/log"
LOGFILE="$LOGDIR/test_jobp.log"

# ROOT_FILE1 a ROOT_FILE19 ? dose_frickeX.txt
for i in $(seq 1 19); do
  export ROOT_FILE$i="$WORKDIR/output/detector$i/dose_fricke$i.txt"
done

# ROOT_FILE20 ? stat.txt
export ROOT_FILE20="$WORKDIR/output/stat.txt"

# ROOT_FILE21 a ROOT_FILE39 ? trajProductionStoppingX.txt
for i in $(seq 1 19); do
  idx=$((20 + i))
  export ROOT_FILE$idx="$WORKDIR/output/detector$i/trajProductionStopping$i.txt"
done

# === Crear directorios si no existen ===
mkdir -p "$LOGDIR"
mkdir -p "$WORKDIR/output"

for i in $(seq 1 19); do
  mkdir -p "$WORKDIR/output/detector$i"
done

# === Verificar existencia de archivo .mac ===
if [ ! -f "$MACFILE" ]; then
  echo "Error: El archivo .mac no existe: $MACFILE" | tee -a "$LOGFILE"
  exit 1
fi

# === Preparar entorno ===
ulimit -v unlimited
ulimit -a >> "$LOGFILE"

# === Configurar variables para ejecución multihilo ===
export OMP_NUM_THREADS=1
export G4FORCENUMBEROFTHREADS=1
export G4MULTITHREADED=1
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=1

{
echo "=================================================="
echo "INICIO DE SIMULACIÓN: $(date)"
echo "Configuración del entorno:"
echo "OMP_NUM_THREADS=$OMP_NUM_THREADS"
echo "G4FORCENUMBEROFTHREADS=$G4FORCENUMBEROFTHREADS"
echo "G4MULTITHREADED=$G4MULTITHREADED"
echo "Información del sistema:"
lscpu | grep -E 'Model name|Socket|Thread|Core' || true
echo "=================================================="
} >> "$LOGFILE"

# === Tiempo de inicio ===
start=$(date +%s)

# === Ejecutar simulación ===
echo "Ejecutando simulación con Gate..." | tee -a "$LOGFILE"
Gate "$MACFILE" >> "$LOGFILE" 2>&1

# === Tiempo de finalización ===
end=$(date +%s)
runtime=$((end - start))

echo "==================================================" >> "$LOGFILE"
echo "FIN DE SIMULACIÓN: $(date)" >> "$LOGFILE"
echo "Tiempo total de ejecución: $runtime segundos" >> "$LOGFILE"
echo "==================================================" >> "$LOGFILE"
