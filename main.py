# These are all installed globally on my system :)
# Somehow no dependency hell????
import socket
import datetime
import time
import os
import platform
try:
    import GPUtil
except:
    pass
import psutil
import sys
import random
from geopy.geocoders import Nominatim
import requests
from cpuinfo import get_cpu_info
from pygame import mixer

RED = '\033[38;5;203m'
ORANGE = '\033[38;5;208m'
GREEN = '\033[38;5;120m'
YELLOW = '\033[38;5;226m'
BLUE = '\033[38;5;117m' #dark-aqua sort of colour
BLUE2 = '\033[96m' #darker blue

UA = {'User-Agent': 'Mozilla/5.0 (compatible; github.com/thiscatlikescrypto/we-know-your-ip-address)'}

def producesyntaxed(text, ifend=False):
    try:
        colour = random.choice([RED, ORANGE, GREEN, YELLOW, BLUE, BLUE2])
        if ifend:
            sys.stdout.write(colour + text + '\033[0m')
        else:
            sys.stdout.write(colour + text + '\033[0m' + "\n")
    except Exception as e:
        print(text)

def download_audio():
    producesyntaxed(f"Downloading song with link https://dl.wilburwilliams.uk/api/raw/?path=/assets/we-know-your-ip-address/song.mp4...")
    try:
        audio_file = requests.get("https://dl.wilburwilliams.uk/api/raw/?path=/assets/we-know-your-ip-address/song.mp4")
        with open("song.mp4", "wb") as f:
            f.write(audio_file.content)
        os.system("ffmpeg -i song.mp4 -vn song.mp3")
        os.remove("song.mp4")
        producesyntaxed("Success")
    except Exception as e:
        producesyntaxed("Error downloading audio:" + str(e))

def play_song():
    """play song.mp3 with mixer"""
    mixer.init()
    mixer.music.load("song.mp3")
    mixer.music.play()

producesyntaxed("Checking for song presence...")
if not os.path.exists("song.mp3"):
    download_audio()

def get_processor_name():
    cpu_info = get_cpu_info()
    try:
        return cpu_info['brand_raw'], cpu_info['hz_actual_friendly'] #Windows
    except:
        return cpu_info['brand'], cpu_info['hz_actual'] #Linux (well, Debian at least)
    

def getIPv4():
    d = requests.get('https://ipv4.icanhazip.com/', headers=UA).text.strip()
    return d

def getIPV6():
    ip6 = requests.get('https://ipv6.icanhazip.com/', headers=UA).text.strip()
    return ip6

def getCoords():
    return requests.get('https://ipinfo.io/loc', headers=UA).text.strip()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def getGPU():
    try:
        gpu0 = GPUtil.getGPUs()[0]
        return gpu0
    except:
        return "fucked"

def main():
    global starttime, timeslept, ipv6, interfaceb4, hostip, if_addrs, net_io, extIP, hostname, cpu, uname, haddress, boot_time_timestamp, bt, cpufreq
    global logical, physical, cpuuse, coresuse, svmem, swap, totalmem, availmem, usemem, totalswap, freeswap, usedswap, latitude, longitude, gpu0, username

    starttime = time.time()
    timeslept = 0.475
    interfaceb4 = []

    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
    producesyntaxed("Getting info...")

    try:
        print("PSUtil stuff...")
        if_addrs = psutil.net_if_addrs()
        net_io = psutil.net_io_counters()
        boot_time_timestamp = psutil.boot_time()
        logical = psutil.cpu_count(logical=True)
        physical = psutil.cpu_count(logical=False)
        cpuuse = psutil.cpu_percent()
        coresuse = []

        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            coresuse.append(f"Core {i}: {percentage}%")
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        print("External API stuff...")
        try:
            extIP = getIPv4()
        except:
            extIP = "failed"
        try:
            ipv6 = getIPV6()
        except:
            ipv6 = "failed (get IPv6 if you don't have it)"
        g = getCoords().split(",")
        latitude = g[0]
        longitude = g[1]
        try:
            app = Nominatim(user_agent="github/thiscatlikescrypto/we-know-your-ip-address")
            coordinates = f"{latitude}, {longitude}"
            haddress = app.reverse(coordinates, language="en").raw
        except:
            haddress = {'address': {'town': "failed, probably something complaining about ssl (occurs on windows frequently)"}}

        print("Other stuff...")
        hostname = socket.gethostname()
        hostip = socket.gethostbyname(hostname)
        cpu, cpufreq = get_processor_name()
        uname = platform.uname()
        bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
        totalmem = get_size(svmem.total)
        availmem = get_size(svmem.available)
        usemem = get_size(svmem.used)
        totalswap = get_size(swap.total)
        freeswap = get_size(swap.free)
        usedswap = get_size(swap.used)
        gpu0 = getGPU()
        username = os.getlogin()

        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

        producesyntaxed("Waiting for song...")

        while True:
            if starttime+13.4<time.time():
                producesyntaxedtheshit()
                break
            
    except Exception as e:
        producesyntaxed(f"Well, shit: {e}")
        sys.exit()

def dots():
    for i in range(100):
        sys.stdout.flush()
        producesyntaxed(".", True)
        time.sleep(timeslept/100)
    print()

def producesyntaxedtheshit():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
    producesyntaxed("External IPv4: " + extIP)
    time.sleep(timeslept)
    producesyntaxed("IPv6: " + str(ipv6))
    time.sleep(timeslept)
    producesyntaxed("Hostname: " + hostname)
    time.sleep(timeslept)
    producesyntaxed("Hostname IP: " + hostip)
    time.sleep(timeslept)
    producesyntaxed("Username: " + username)
    time.sleep(timeslept)
    producesyntaxed("Latitude: " + str(latitude))
    time.sleep(timeslept)
    producesyntaxed("Longitude: " + str(longitude))
    time.sleep(timeslept)
    try:
        producesyntaxed("Location: " + str(haddress['address']['town']))
    except:
        producesyntaxed("Location failed lmao")
    time.sleep(timeslept)
    producesyntaxed("System Type: " + os.name)
    time.sleep(timeslept)
    producesyntaxed("OS Name: " + uname.system)
    time.sleep(timeslept)
    producesyntaxed(f"Machine: {uname.machine}")
    time.sleep(timeslept)
    producesyntaxed(f"Boot Time: {bt.year}-{bt.month}-{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    time.sleep(timeslept)
    producesyntaxed("CPU: " + cpu)
    time.sleep(timeslept)
    producesyntaxed("CPU Speed: " + cpufreq)
    time.sleep(timeslept)
    producesyntaxed(f"Physical cores: {physical}")
    time.sleep(timeslept)
    producesyntaxed(f"Total cores: {logical}")
    time.sleep(timeslept)
    producesyntaxed("Cores usage: ")
    time.sleep(timeslept)

    for core in coresuse:
        producesyntaxed(f"    {core}")
        time.sleep(timeslept)

    producesyntaxed(f"Total CPU Usage: {cpuuse}%")
    time.sleep(timeslept)

    producesyntaxed(f"Total Memory: {totalmem}")
    time.sleep(timeslept)
    producesyntaxed(f"Available Memory: {availmem}")
    time.sleep(timeslept)
    producesyntaxed(f"Used Memory: {usemem}")
    time.sleep(timeslept)
    producesyntaxed(f"Percentage of Memory Used: {svmem.percent}%")
    time.sleep(timeslept)

    producesyntaxed(f"Total Swap: {totalswap}")
    time.sleep(timeslept)
    producesyntaxed(f"Free Swap: {freeswap}")
    time.sleep(timeslept)
    producesyntaxed(f"Used Swap: {usedswap}")
    time.sleep(timeslept)
    producesyntaxed(f"Percentage of Swap Used: {swap.percent}%")
    time.sleep(timeslept)

    try:
        producesyntaxed(f"GPU0: {gpu0.name}")
        time.sleep(timeslept)
        producesyntaxed(f"GPU0 Memory: {gpu0.memoryUsed}")
        time.sleep(timeslept)
        producesyntaxed(f"GPU0 Temperature: {gpu0.temperature}")
        time.sleep(timeslept)
        producesyntaxed(f"GPU0 Load: {gpu0.load*100}%")
    except:
        producesyntaxed("GPU0 not found")
    time.sleep(timeslept)

    producesyntaxed('"Hacking" your computer (aka doing nothing)...', True)
    dots()
    producesyntaxed("Injecting your IP into the system (also aka doing nothing)...", True)
    dots()
    producesyntaxed("Injecting your username into the system (also also aka doing nothing)...", True)
    dots()
    producesyntaxed("maybe you should do something else instead of running this script...", True)
    dots()
    producesyntaxed("maybe go touch grass (or do nothing)...", True)
    dots()
    producesyntaxed("wait what am i doing", True)
    dots()
    producesyntaxed("fun fact: producesyntaxed is a stronge reference", True)
    dots()
    producesyntaxed("what is stronge i hear you ask", True)
    # it is eyescary.uk/stronge
    dots()
    producesyntaxed("maybe you should look at the source code", True)
    dots()
    producesyntaxed("anyway song nearly over so cya", True)

    time.sleep(15)

if __name__ == "__main__":
    play_song()
    main()
