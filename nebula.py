import subprocess, time
import pathlib
import os
import threading

def windowsPopen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return process

class Nebula(threading.Thread):
    proc=None
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
        if type(self.config) == list:
            self.doneCallback()
            self.lineCallback("Please select 1 config file")
            return
        if os.name == "nt":
            self.proc = windowsPopen([str(self.directory)+os.sep+"nebula.exe", "--config", self.config], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            self.proc = subprocess.Popen([str(self.directory)+os.sep+"nebula", "--config", self.config], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            for line in iter(self.proc.stdout.readline, ''):
                if self.proc.poll() is not None:
                    self.doneCallback()
                    self.proc.kill()
                    break
                if line.decode('utf-8') != '':
                    self.lineCallback(line.decode('utf-8'))
                if line.decode('utf-8') == '':
                    print("sleeping")
                    time.sleep(1)
            print("out of loop")
        except AttributeError as e:
            self.doneCallback()
            out, err = self.proc.communicate()
            if out is not None:
                self.lineCallback(out)
            if err is not None:
                self.lineCallback(err)
            if "NoneType" in str(e):
                self.lineCallback("Please run as sudo\n")
            self.proc.kill()

    def disconnect(self):
        self.lineCallback("Stopping")
        if self.proc is not None:
            self.proc.kill()