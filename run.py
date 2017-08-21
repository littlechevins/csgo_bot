#!/usr/bin/python
import subprocess

subprocess.call('sudo node csgo.js && python filter.py | python upload.py', shell=True)
