import requests
from pathlib import Path
from ftplib import FTP
from os.path import exists
from os import mkdir,listdir

if not exists('wget-list'):
    print('"wget-list" not found. Downloading.')
    req = requests.get('http://www.linuxfromscratch.org/lfs/downloads/stable/wget-list')
    open('wget-list','wb').write(req.content)
    print('Downloaded "wget-list".')

Path('lib-src').mkdir(exist_ok=True)
with open('wget-list','r') as f:
    links = [line.strip() for line in f.readlines()]
    files = listdir('lib-src')
    for link in links:
        fname = link.split('/')[-1]
        proto = link.split(':')[0]
        if not fname in files:
            try:
                print(f"Downloading {fname} from {link}...")
                if proto in ('http','https'):
                    req = requests.get(link,allow_redirects=True)
                    open(f"lib-src/{fname}",'wb').write(req.content)
                else:
                    link = link[6:].split('/')
                    domain = link[0]
                    path = '/'.join(link[1:-1])
                    fname = link[-1]

                    ftp = FTP(domain)
                    ftp.login()
                    ftp.cwd(path)
                    with open(f"lib-src/{fname}",'wb') as fp:
                        ftp.retrbinary(f"RETR {fname}", fp.write)
                    ftp.quit()
            except:
                print(f"Error while downloading {fname} from {link}.")
        else:
            print(f"{fname} already present.")