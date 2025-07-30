#!/bin/bash

# Exportar variables necesarias para evitar error TLS
export LD_LIBRARY_PATH=/root/opengate_env/lib/python3.12/site-packages/opengate_core.libs:$LD_LIBRARY_PATH
export LD_PRELOAD=$(ls /root/opengate_env/lib/python3.12/site-packages/opengate_core.libs/libG4*.so | tr '\n' ':')
export GLIBC_TUNABLES=glibc.rtld.optional_static_tls=2000000


# Crear carpeta de logs si no existe
mkdir -p /fuente3/undetector/output/log

# Definir rutas
LOGFILE="/fuente3/mdetectores/output/log/simulacion.log"
SCRIPT="fuente3mdsvp.py"

# Marcar hora de inicio
start=$(date +%s)

echo "==================================================" | tee -a "$LOGFILE"
echo "INICIO DE SIMULACIÓN: $(date)" | tee -a "$LOGFILE"
echo "Ejecutando script: $SCRIPT" | tee -a "$LOGFILE"
echo "==================================================" | tee -a "$LOGFILE"

# Ejecutar la simulación
python "$SCRIPT" >> "$LOGFILE" 2>&1

# Marcar hora de finalización
end=$(date +%s)
runtime=$((end - start))

# Guardar tiempo total
{
  echo "=================================================="
  echo "FIN DE SIMULACIÓN: $(date)"
  echo "Tiempo total de ejecución real: $runtime segundos"
  echo "=================================================="
} >> "$LOGFILE"
