import subprocess

path1 = 'src/scraper/antartica.py'
path2 = 'src/scraper/feriachilena.py'
path3 = 'src/scraper/buscalibre.py'

def __main__():
    subprocess.run(['python', path1])
    subprocess.run(['python', path2])
    subprocess.run(['python', path3])

__main__()

