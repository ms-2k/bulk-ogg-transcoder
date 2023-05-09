from os import listdir, rename, mkdir, remove
from os.path import join as join_path, isdir, exists
from multiprocessing import Process
from time import sleep
import subprocess

#encodes each file
#ffmpeg = FFmpeg path
#ipath = input path
#opath = output path
#file_name = name of the file to encode
#num = counter for temporary filename
#bitrate = target bitrate
#verbose = for debugging
def encode(ffmpeg, ipath, opath, file_name, num, bitrate, verbose):
    
    #get full file path for inputs and outputs
    #set a temporary path for outputs as ffmpeg breaks for lots of special characters
    input_path = join_path(ipath, file_name)
    output_temp = join_path(opath, str(num) + '.ogg')
    output_path = join_path(opath, file_name[:-5] + '.ogg')

    #check if the file to output to already exists
    #remove it if it does
    if exists(output_path):
        remove(output_path)

    #the command to call for ffmpeg
    cmd = f'{ffmpeg} -i "{input_path}" -y -c:a libvorbis -map 0:a -b:a {bitrate}k "{output_temp}"'

    #throw it into a subprocess
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd, startupinfo = startupinfo)
    process.wait()

    #print return code if verbose
    if verbose:
        print('return code:', process.returncode)

    #if the encoding succeeds, rename the temp file to proper filename matching the original
    if process.returncode == 0:
        rename(output_temp, output_path)

#calls encode for every .flac file
#ffmpeg = FFmpeg path
#ipath = input path
#opath = output path
#bitrate = target bitrate
#verbose = for debugging
def encode_all(ffmpeg, ipath, opath, bitrate, verbose = False):

    #check if the target directory exists
    if not isdir(opath):
        mkdir(opath)

    #counter
    num = 0
    #process list
    proc_list = []

    #iterate over every file in input path
    for file_name in listdir(ipath):
        #skip if it isn't .flac
        if not file_name.endswith('.flac'):
            continue
        
        #call the process and start it
        proc = Process(target = encode, args = (ffmpeg, ipath, opath, file_name, num, bitrate, verbose))
        proc.start()
        proc.join(timeout=0)

        #append to process list
        proc_list.append(proc)

        #increment counter
        num += 1
    
    #wait for processes to finish
    for proc in proc_list:
        while proc.is_alive():
            sleep(0.5)
