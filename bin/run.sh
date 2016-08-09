#!/bin/bash
set -e

SPARK_HOME=~/spark
MASTER=local[2]

${SPARK_HOME}/bin/spark-submit \
  --num-executors 3 \
  --driver-memory 2g \
  --executor-memory 1g \
  --executor-cores 3 \
  --master ${MASTER} \
  --py-files dist/pg_reverse_geocoder-1.0.zip \
  "reverse_geocoder/cleanup_job.py"

