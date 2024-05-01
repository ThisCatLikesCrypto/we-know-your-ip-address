import socket
from urllib.request import urlopen
import datetime
import time
import os
import platform
import subprocess
import re
import psutil
import multiprocessing
from pytube import YouTube
from playsound import playsound
import sys

#Audio downloader (from youtube)
def download_audio(yt_link):
    print(f"Downloading new background song with link {yt_link}...")
    try:
        yt = YouTube(yt_link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(os.path.join(os.getcwd(), "resources"), "song.mp4")
        print("Success")
        return audio_file
    except Exception as e:
        print("Error downloading audio:" + str(e))
        return None

def play_song():
    try:
        playsound(os.path.join(os.getcwd(), "resources", "song.mp4"))
    except Exception as e:
        print("playsound error "+ str(e))

print("Checking for song presence...")
if not os.path.exists(os.path.join(os.getcwd(), "resources", "song.mp4")):
    download_audio("https://www.youtube.com/watch?v=VCrxUN8luzI") #Gotta love using YouTube as a CDN

def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command ="sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""

def getIP():
    d = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


musicgobrr = multiprocessing.Process(target=play_song)
musicgobrr.start()
starttime = time.time()
if os.name == "nt":
    os.system('cls')
else:
    os.system('clear')
print("Getting info...")

try:
    if_addrs = psutil.net_if_addrs()
    net_io = psutil.net_io_counters()
    extIP = getIP()
    hostname = socket.gethostname()
    cpu = get_processor_name().split("@")
    uname = platform.uname()
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
    cpufreq = psutil.cpu_freq()
    logical = psutil.cpu_count(logical=True)
    physical = psutil.cpu_count(logical=False)
    cpuuse = psutil.cpu_percent()
    coresuse = []

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        coresuse.append(f"Core {i}: {percentage}%")

    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    totalmem = get_size(svmem.total)
    availmem = get_size(svmem.available)
    usemem = get_size(svmem.used)
    totalswap = get_size(swap.total)
    freeswap = get_size(swap.free)
    usedswap = get_size(swap.used)
except Exception as e:
    print(f"Well, shit: {e}")
    musicgobrr.terminate()
    sys.exit()

timeslept = 0.505
interfaceb4 = []

def printtheshit():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
    print("Computer Name: " + hostname)
    time.sleep(timeslept)
    print("External IP: " + extIP)
    time.sleep(timeslept)
    for interface_name, interface_addresses in if_addrs.items():
            print(f"Interface: {interface_name}")
            interfaceb4.append(interface_name)
            time.sleep(timeslept)
            for address in interface_addresses:
                print(f"    MAC Address: {address.address}")
                time.sleep(timeslept)
                print(f"        Netmask: {address.netmask}")
                time.sleep(timeslept)
                print(f"        Broadcast MAC: {address.broadcast}")
                time.sleep(timeslept)
    print("System Type: " + os.name)
    time.sleep(timeslept)
    print("OS Name: " + uname.system)
    time.sleep(timeslept)
    print(f"Machine: {uname.machine}")
    time.sleep(timeslept)
    print(f"Boot Time: {bt.year}-{bt.month}-{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    time.sleep(timeslept)

    print("CPU:" + cpu[0])
    time.sleep(timeslept)
    print("CPU speed: " + cpu[1].removeprefix(" "))
    time.sleep(timeslept)
    print(f"Physical cores: {physical}")
    time.sleep(timeslept)
    print(f"Total cores: {logical}")
    time.sleep(timeslept)
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    time.sleep(timeslept)
    print("Cores usage: ")
    time.sleep(timeslept)

    for core in coresuse:
        print(f"    {core}")
        time.sleep(timeslept)

    print(f"Total CPU Usage: {cpuuse}%")
    time.sleep(timeslept)

    print(f"Total Memory Usage: {totalmem}")
    time.sleep(timeslept)
    print(f"Available Memory: {availmem}")
    time.sleep(timeslept)
    print(f"Used Memory: {usemem}")
    time.sleep(timeslept)
    print(f"Percentage of Memory Used: {svmem.percent}%")
    time.sleep(timeslept)

    print(f"Total Swap Usage: {totalswap}")
    time.sleep(timeslept)
    print(f"Free Swap: {freeswap}")
    time.sleep(timeslept)
    print(f"Used Swap: {usedswap}")
    time.sleep(timeslept)
    print(f"Percentage of Swap Used: {swap.percent}%")

if os.name == "nt":
    os.system('cls')
else:
    os.system('clear')
print("Waiting for song...")

while True:
    if starttime+13.6<time.time():
        printtheshit()
        musicgobrr.terminate()
        break