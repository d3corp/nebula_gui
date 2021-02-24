import subprocess, time
import pathlib
import os

def popen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return process

def runNebula(threadName, lineCallback, executable, config, directory, done):

    lineCallback("Nebula running\n")
    proc = popen([str(directory)+os.sep+"nebula.exe", "--config", config])
    for line in iter(proc.stdout.readline, ''):
        if line.decode('utf-8') != '':
                lineCallback(line.decode('utf-8'))
        if proc.poll() is not None:
            done()
            proc.kill()
            break