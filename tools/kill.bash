#!/bin/bash

# Identify the process using port 8080
PID=$(lsof -t -i:8080)

# Check if the PID exists
if [ -z "$PID" ]; then
    echo "No process is using port 8080"
else
    # Kill the process
    kill $PID
    echo "Process using port 8080 has been killed"
fi