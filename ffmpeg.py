import subprocess
from zipfile import ZipFile
from io import BytesIO
from os import getcwd as cwd, mkdir
from os.path import exists
from requests import get
from shutil import copyfileobj

#return ffmpeg path
def ffmpeg_path():

    #test if ffmpeg is already in system
    try:
        subprocess.run('ffmpeg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return 'ffmpeg'
    
    #check if ffmpeg has been installed by this program
    except FileNotFoundError:
        installed_path = cwd() + '\\ffmpeg\\ffmpeg.exe'

        if exists(installed_path):
            return installed_path
        
        #return none if true
        return None

#download ffmpeg.exe if it is not available
def acquire_ffmpeg():

    #download address
    address = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'

    #download the file and initialize zipfile
    fetch = get(address, stream=True)
    zip = ZipFile(BytesIO(fetch.content))

    #find ffmpeg.exe in the zipfile
    for name in zip.namelist():
        if name.endswith('ffmpeg.exe'):
            target = name

    #check ffmpeg subdirectory exists
    if not exists(cwd() + '\\ffmpeg'):
        mkdir(cwd() + '\\ffmpeg')
    
    #extract ffmpeg.exe into \ffmpeg\ffmpeg.exe
    with zip.open(target) as zippedFile, open(cwd() + '\\ffmpeg\\ffmpeg.exe', 'wb') as targetFile:
        copyfileobj(zippedFile, targetFile)

#ensure that ffmpeg is installed
#force_dl makes the program download ffmpeg regardless of its availability
def ensure_ffmpeg(force_dl = False):
    if ffmpeg_path() == None or force_dl:
        acquire_ffmpeg()

#test code
if __name__ == '__main__':
    ensure_ffmpeg()