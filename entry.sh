#!/bin/bash


cd /home/tapis; uvicorn service.api:app --reload --host 0.0.0.0 --port 8000

while true; do sleep 86400; done