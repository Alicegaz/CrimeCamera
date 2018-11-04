#!/bin/bash
docker run -it seal-save SCRIPT_DIR="$( cd "$( ./SEALPythonExamples/ "${BASH_SOURCE[0]}" )" && pwd )"
docker run -it seal-save python3 -m compileall ./SEALPythonExamples/encrypt.py
docker run -it seal-save python3 SEALPythonExamples/encrypt.py
