#!/usr/bin/env bash
set -euo pipefail

curl -s http://127.0.0.1:8000/health
echo
curl -s -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"MedInc":8.3252,"HouseAge":41.0,"AveRooms":6.984127,"AveBedrms":1.02381,"Population":322.0,"AveOccup":2.555556,"Latitude":37.88,"Longitude":-122.23}'
echo
