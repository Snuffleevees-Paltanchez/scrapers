import subprocess

path1 = 'src/scraper/antartica.py'
path2 = 'src/scraper/feriachilena.py'
path3 = 'src/scraper/buscalibre.py'
path4 = 'src/scraper/contrapunto.py'
path5 = 'src/scraper/googleapi.py'

csvRead = {
    'antartica': 'src/scraper/librerias/antartica.csv',
    'feriachilena': 'src/scraper/librerias/feriachilena.csv',
    'buscalibre': 'src/scraper/librerias/buscalibre.csv',
    'contrapunto': 'src/scraper/librerias/contrapunto.csv',
}

csvWrite = {
    'antartica': 'src/scraper/libreriasExtra/antartica.csv',
    'feriachilena': 'src/scraper/libreriasExtra/feriachilena.csv',
    'buscalibre': 'src/scraper/libreriasExtra/buscalibre.csv',
    'contrapunto': 'src/scraper/libreriasExtra/contrapunto.csv',
}

def __main__():
    subprocess.run(['python', path1])
    subprocess.run(['python', path2])
    subprocess.run(['python', path3])
    subprocess.run(['python', path4])

    subprocess.run(['python', path5, csvRead['antartica'], csvWrite['antartica']])
    subprocess.run(['python', path5, csvRead['feriachilena'], csvWrite['feriachilena']])
    subprocess.run(['python', path5, csvRead['buscalibre'], csvWrite['buscalibre']])
    subprocess.run(['python', path5, csvRead['contrapunto'], csvWrite['contrapunto']])

__main__()

