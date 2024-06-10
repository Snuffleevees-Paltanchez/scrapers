import subprocess

path1 = 'src/scraper/antartica.py'
path2 = 'src/scraper/feriachilena.py'
path3 = 'src/scraper/buscalibre.py'
path4 = 'src/scraper/contrapunto.py'

def __main__():
    subprocess.run(['python', path1])
    subprocess.run(['python', path2])
    subprocess.run(['python', path3])
    subprocess.run(['python', path4])

__main__()

