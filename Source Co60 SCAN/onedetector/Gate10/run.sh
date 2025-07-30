#!/bin/bash

# Exportar variables necesarias para evitar error TLS
export LD_LIBRARY_PATH=/root/opengate_env/lib/python3.12/site-packages/opengate_core.libs:$LD_LIBRARY_PATH
export LD_PRELOAD=$(ls /root/opengate_env/lib/python3.12/site-packages/opengate_core.libs/libG4*.so | tr '\n' ':')
export GLIBC_TUNABLES=glibc.rtld.optional_static_tls=2000000


# Crear carpeta de logs si no existe
mkdir -p /fuente3/undetector/output/log

# Ejecutar simulacion y guardar salida en log
python fuente3dsvp.py > /fuente3/undetector/output/log/simulacion.log 2>&1
