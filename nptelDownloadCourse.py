import requests
from bs4 import BeautifulSoup

def nptel(link):

    url = link
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'lxml')
    count=0
    for link in soup.findAll('a'):
        if 'mp4' in link.get('href'):
            count=count+1   
            filename = "https://nptel.ac.in"+link.get('href')
            r = requests.get(filename,stream = True)
            print("https://nptel.ac.in"+link.get('href'))
            print('Downloading')
            n = str(count) + str('.mp4')
            done = 0
            file_size = float(r.headers['content-length'])
            with open(n,'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)
                        done += len(chunk)
                        print('progress ',float((done/file_size)*100.0),' percent')
            print('Downloaded 1 video in current directory!')
    print('Total Videos',count)
nptel('https://nptel.ac.in/courses/nptel_download.php?subjectid=106105184')
