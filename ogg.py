from os import listdir, getcwd, rename, mkdir
from os.path import join as join_path, isdir
from multiprocessing import Process
import subprocess

#wip

def encode(path, opath, file_name, num, bitrate):
    input_path = join_path(path, file_name)
    output_path = join_path(opath, str(num) + '.ogg')
    cmd = f'ffmpeg -i "{input_path}" -y -c:a libvorbis -map 0:a -b:a {bitrate}k "{output_path}"'
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if process.returncode == 0:
        print(process.stdout.decode())
        rename(output_path, join_path(opath, file_name[:-5] + '.ogg'))

def encode_all(path, opath, bitrate):
    if not isdir(opath):
        mkdir(opath)
    num = 0
    for file_name in listdir(path):
        if not file_name.endswith('.flac'):
            continue
        Process(target = encode, args = (path, opath, file_name, num, bitrate)).start()
        num += 1

if __name__ == '__main__':
    path = input('input: ')
    if path[0] == '"' and path[-1] == '"':
        path = path[1:-1]
    opath = input('output: ')
    if path in ('*', ''):
        path = getcwd()
    if opath in ('*', ''):
        opath = join_path(path, path.split('\\')[-1])
    try:
        bitrate = int(input('bitrate: '))
    except:
        bitrate = 160
    encode_all(path, opath, bitrate)
