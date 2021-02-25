import subprocess, time
import pathlib
import os
import threading

def popen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return process

class Nebula(threading.Thread):
    stop=False
    def __init__(self, lineCallback, doneCallback, directory, config):
        threading.Thread.__init__(self)
        self.threadID = "nebula"
        self.setName("nebula")
        self.lineCallback = lineCallback
        self.doneCallback = doneCallback
        self.directory = directory
        self.config = config
    def run(self):
        self.lineCallback("Nebula running\n")
        self.startProcess()
    
    def startProcess(self):
        print(str(self.directory)+os.sep+"nebula.exe")
        proc = popen([str(self.directory)+os.sep+"nebula.exe", "--config", self.config])
        for line in iter(proc.stdout.readline, ''):
            if line.decode('utf-8') != '':
                self.lineCallback(line.decode('utf-8'))
            if proc.poll() is not None:
                self.doneCallback()
                proc.kill()
                break
            if self.stop:
                self.doneCallback()
                self.lineCallback("Stopping")
                proc.kill()
                break

    def disconnect(self):
        self.stop=True