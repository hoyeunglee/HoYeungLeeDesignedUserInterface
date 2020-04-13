import asyncio
import datetime
import random
import websockets
from subprocess32 import STDOUT, check_output
import re
import sys
import traceback
#import paramiko
#from netmiko import ConnectHandler
import pyttsx3
import subprocess
import speech_recognition as sr
import os
import subprocess
from os import listdir
from os.path import isfile, join
currentdirectory = os.getcwd()
#from gensim.test.utils import common_texts
#from gensim.models import Word2Vec
#import gensim.downloader as api

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

def savewave():
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE=44100
    CHUNK=1024
    RECORD_SECONDS=2
    FILE_NAME="demo.wav"
    audio=pyaudio.PyAudio() #instantiate the pyaudio
    #recording prerequisites
    stream=audio.open(format=FORMAT,channels=CHANNELS, 
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)
    #starting recording
    frames=[]
    for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
        data=stream.read(CHUNK)
        data_chunk=array('h',data)
        vol=max(data_chunk)
        if(vol>=300):
            frames.append(data)
        #else:
            #print("nothing")
        #print("\n")        
    #end of recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    #writing to file
    wavfile=wave.open(FILE_NAME,'wb')
    wavfile.setnchannels(CHANNELS)
    wavfile.setsampwidth(audio.get_sample_size(FORMAT))
    wavfile.setframerate(RATE)
    wavfile.writeframes(b''.join(frames))#append frames recorded to file
    wavfile.close()

#model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)
#word_vectors = model.wv

#word_vectors = api.load("glove-wiki-gigaword-100")

complain = ["enlarge","next"]
controls1 = ["enlarge","next"]

r = sr.Recognizer()
mic = sr.Microphone()
proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
engine = pyttsx3.init()

#officefiles = [f for f in listdir(os.path.join("C:\Program Files (x86)\Microsoft Office\Office16","")) if isfile(os.path.join("C:\Program Files (x86)\Microsoft Office\Office16", "Excel.exe"))]

result = ""
r.dynamic_energy_threshold = False
r.energy_threshold = 400
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0")

onceerror = 0
currentwindow = 0
controlres = 0
doneit = 0
async def time(websocket, path):
    onceerror = 0
    currentwindow = 0
    controlres = 0
    doneit = 0
    while True:
        try:
            #with mic as source:
            #print("Hello. Please speak")
            #engine.say('Hello. Please speak')
            #engine.runAndWait()
            #print("begin")
            savewave()
            #print("end record")
            jackhammer = sr.AudioFile('demo.wav')
            with jackhammer as source:
                audio = r.record(source)
                onceerror = 0
                r.adjust_for_ambient_noise(source, duration=2)
                result = r.recognize_google(audio, show_all=True)
                print(result["alternative"])
                lengthofcomplain = 7
                doneit = 0
                for mess in result["alternative"]:
                    try:
                        if doneit == 0:
                            complain2 = mess["transcript"]
                            if complain2.lower().startswith("le") or complain2.lower().startswith("ne") or complain2.lower().startswith("s") or complain2.lower().startswith("x") or complain2.lower().startswith("ex") or complain2.lower().startswith("le"):
                                print("next is called 1")
                                controlres = currentwindow
                                print("next is called 1a")
                                currentwindow = currentwindow + 1
                                print("next is called 1aa")
                                if currentwindow == 3:
                                    currentwindow = 0
                                    print("next is called 1aaa")
                                controlres = currentwindow
                                print("next is called 2")
                                print("sent " + str(controlres))
                                await websocket.send(str(controlres).strip())
                                print("sent " + str(controlres))
                                doneit = 1
                            elif complain2.lower() in ["back"] or complain2.lower().startswith("ba") or complain2.lower().startswith("be"):
                                await websocket.send(str("99").strip())
                                doneit = 1
                            elif complain2.lower() in ["enlarge"] or complain2.lower().startswith("en") or complain2.lower().startswith("an"):
                                await websocket.send(str("100").strip())
                                doneit = 1
                            else:
                                stdout, stderr = subprocess.Popen(complain1.lower()+".exe")
                                stdout
                    except:
                        print("can not open")
        except Exception as e: 
            if onceerror == 0:
                print(e)
                print("try again")
                onceerror = 1
        
start_server = websockets.serve(time, '127.0.0.1', 5679)
subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe --chrome --start-fullscreen  C:\Users\mas\Documents\VoiceWebControl-Success90marks\magic-master\controlx2.html --incognito --disable-pinch --overscroll-history-navigation=0")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()