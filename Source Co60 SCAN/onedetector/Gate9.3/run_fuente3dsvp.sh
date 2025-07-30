#!/bin/bash
# Script para ejecutar fuente3dsvp.mac con 4 n�cleos

# === Configuraci�n de rutas ===
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

# === Configurar variables para ejecuci�n multihilo ===
export OMP_NUM_THREADS=4
export G4FORCENUMBEROFTHREADS=4
export G4MULTITHREADED=1

{
echo "=================================================="
echo "INICIO DE SIMULACI�N: $(date)"
echo "Configuraci�n del entorno:"
echo "OMP_NUM_THREADS=$OMP_NUM_THREADS"
echo "G4FORCENUMBEROFTHREADS=$G4FORCENUMBEROFTHREADS"
echo "G4MULTITHREADED=$G4MULTITHREADED"
echo "Informaci�n del sistema:"
lscpu | grep -E 'Model name|Socket|Thread|Core' || true
echo "=================================================="
} >> "$LOGFILE"

# === Tiempo de inicio ===
start=$(date +%s)

echo "Iniciando simulaci�n con $OMP_NUM_THREADS n�cleos..." | tee -a "$LOGFILE"

# === Ejecutar GATE ===
cd "$WORKDIR" || exit 1
Gate "$MACFILE" >> "$LOGFILE" 2>&1

# === Tiempo de fin ===
end=$(date +%s)
duration=$((end - start))

echo "Simulaci�n completada correctamente en $duration segundos." | tee -a "$LOGFILE"

# === Guardar salida estad�stica adicional ===
echo "Tiempo de ejecuci�n (segundos): $duration" >> "ROOT_FILE2"
echo "Fecha de finalizaci�n: $(date)" >> "ROOT_FILE2"

# === Guardar logs del sistema ===
dmesg | tail -n 100 >> "$DMESG_LOG"

echo "Archivos generados:"
echo "- Log principal: $LOGFILE"
echo "- Dmesg: $DMESG_LOG"
echo "- Dosis: $ROOT_FILE1"
echo "- Estad�sticas: $ROOT_FILE2"
echo "- Tiempo total: $STAT_FILE"

# Mostrar archivos generados
echo "Archivos en output:"
ls -lh /fuente3/undetector/output/
