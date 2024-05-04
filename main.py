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
import random
import geocoder
from geopy.geocoders import Nominatim
import ipaddress


RED = '\033[38;5;203m'
ORANGE = '\033[38;5;208m'
GREEN = '\033[38;5;120m'
YELLOW = '\033[38;5;226m'
BLUE = '\033[38;5;117m' #dark-aqua sort of colour
BLUE2 = '\033[96m' #darker blue

def producesyntaxed(text):
    try:
        colour = random.choice([RED, ORANGE, GREEN, YELLOW, BLUE, BLUE2])
        sys.stdout.write(colour + text + '\033[0m' + "\n")
    except Exception as e:
        print(text)

#Audio downloader (from youtube)
def download_audio(yt_link):
    producesyntaxed(f"Downloading new background song with link {yt_link}...")
    try:
        yt = YouTube(yt_link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(os.getcwd(), "song.mp4")
        producesyntaxed("Success")
        return audio_file
    except Exception as e:
        producesyntaxed("Error downloading audio:" + str(e))
        return None

def play_song():
    print("IF PLAYSOUND ERRORS OCCUR IGNORE THEM UNLESS EXPLICITLY 'playsound error'")
    try:
        playsound("song.mp4")
    except Exception as e:
        try:
            playsound("song.mp4")
        except Exception as e:
            try:
                playsound("song.mp4")
            except Exception as e:
                producesyntaxed("playsound error "+ str(e))

producesyntaxed("Checking for song presence...")
if not os.path.exists("song.mp4"):
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

def getIPV6(ip4):
    ip4 = ipaddress.IPv4Address(ip4)
    prefix6to4 = int(ipaddress.IPv6Address("2002::"))
    ip6 = ipaddress.IPv6Address(prefix6to4 | (int(ip4) << 80))
    return ip6

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def main():
    global starttime, timeslept, ipv6, interfaceb4, hostip, if_addrs, net_io, extIP, hostname, cpu, uname, haddress, boot_time_timestamp, bt, cpufreq, logical, physical, cpuuse, coresuse, svmem, swap, totalmem, availmem, usemem, totalswap, freeswap, usedswap, latitude, longitude

    starttime = time.time()
    timeslept = 0.488
    interfaceb4 = []

    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
    producesyntaxed("Getting info...")

    try:
        if_addrs = psutil.net_if_addrs()
        net_io = psutil.net_io_counters()
        extIP = getIP()
        hostname = socket.gethostname()
        ipv6 = getIPV6(extIP)
        hostip = socket.gethostbyname(hostname)
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
        g = geocoder.ip('me')

        latitude = g.latlng[0]
        longitude = g.latlng[1]
        try:
            app = Nominatim(user_agent="tutorial")
            coordinates = f"{latitude}, {longitude}"
            # sleep for a second to respect Usage Policy
            time.sleep(1)
            haddress = app.reverse(coordinates, language="en").raw
        except:
            haddress = {'address': {'town': "failed, probably something complaining about ssl (occurs on windows frequently)"}}

        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

        producesyntaxed("Waiting for song...")

        while True:
            if starttime+13.6<time.time():
                producesyntaxedtheshit()
                break
            
    except Exception as e:
        producesyntaxed(f"Well, shit: {e}")
        musicgobrr.terminate()
        sys.exit()

def producesyntaxedtheshit():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
    producesyntaxed("External IP: " + extIP)
    time.sleep(timeslept)
    producesyntaxed("Hostname: " + hostname)
    time.sleep(timeslept)
    producesyntaxed("Hostname IP: " + hostip)
    time.sleep(timeslept)
    producesyntaxed("IPv6: " + str(ipv6))
    time.sleep(timeslept)
    producesyntaxed("Latitude: " + str(latitude))
    time.sleep(timeslept)
    producesyntaxed("Longitude: " + str(longitude))
    time.sleep(timeslept)
    producesyntaxed("Location: " + str(haddress['address']['town']))
    time.sleep(timeslept)
    producesyntaxed("System Type: " + os.name)
    time.sleep(timeslept)
    producesyntaxed("OS Name: " + uname.system)
    time.sleep(timeslept)
    producesyntaxed(f"Machine: {uname.machine}")
    time.sleep(timeslept)
    producesyntaxed(f"Boot Time: {bt.year}-{bt.month}-{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    time.sleep(timeslept)

    producesyntaxed("CPU:" + cpu[0])
    time.sleep(timeslept)
    try:
        producesyntaxed("CPU speed: " + cpu[1].removeprefix(" "))
        time.sleep(timeslept)
    except:
        pass
    producesyntaxed(f"Physical cores: {physical}")
    time.sleep(timeslept)
    producesyntaxed(f"Total cores: {logical}")
    time.sleep(timeslept)
    producesyntaxed(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    time.sleep(timeslept)
    producesyntaxed("Cores usage: ")
    time.sleep(timeslept)

    for core in coresuse:
        producesyntaxed(f"    {core}")
        time.sleep(timeslept)

    producesyntaxed(f"Total CPU Usage: {cpuuse}%")
    time.sleep(timeslept)

    producesyntaxed(f"Total Memory Usage: {totalmem}")
    time.sleep(timeslept)
    producesyntaxed(f"Available Memory: {availmem}")
    time.sleep(timeslept)
    producesyntaxed(f"Used Memory: {usemem}")
    time.sleep(timeslept)
    producesyntaxed(f"Percentage of Memory Used: {svmem.percent}%")
    time.sleep(timeslept)

    producesyntaxed(f"Total Swap Usage: {totalswap}")
    time.sleep(timeslept)
    producesyntaxed(f"Free Swap: {freeswap}")
    time.sleep(timeslept)
    producesyntaxed(f"Used Swap: {usedswap}")
    time.sleep(timeslept)
    producesyntaxed(f"Percentage of Swap Used: {swap.percent}%")

if __name__ == "__main__":
    musicgobrr = multiprocessing.Process(target=play_song)
    musicgobrr.start()
    main()