#!/bin/bash


cd /home/tapis; uvicorn service.api:app --host 0.0.0.0 --port 8000

if [ "$DEBUG_SLEEP_LOOP" == "sleep" ]; then
  while true; do sleep 86400; done
fi
