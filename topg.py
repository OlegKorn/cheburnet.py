import requests, sys, re
from bs4 import BeautifulSoup as bs


URL = 'http://www.girlstop.info/models.php?name=Iveta-B'
site_root = 'http://www.girlstop.info'
headers = {'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
home = '/home/o/python/ero/gtop/ivetab/'
links = []
checked = []
img_links = []


def check():
    for i in links:
        if i in checked:
            pass
           
        else:
            checked.append(i)

                      
def get_entries_urls():
    
    try:
        session = requests.Session()
        request = session.get(URL, headers=headers)
        soup = bs(request.content, 'html.parser')
       
        for i in soup.find('table', attrs={'id':'models'}).find_all('td'):
            link_container = i.find('a')
           
            if not link_container is None:
                link = site_root + link_container.get('href')
                links.append(link)

    except Exception as e:
        print(e)

    check() #лень было копаться, сделал проверку дублирующихся ссылок на посты, т.к. там было по 2 подряд
    

def save():
    
    try:
        for psto in checked:
            session = requests.Session()
            request = session.get(psto, headers=headers)
            soup = bs(request.content, 'html.parser')

            for img in soup.find_all('a', class_='fullimg'):
                try:
                    img_prelink = img.get('href')
                    img_subname = img_prelink[17:].replace('/', '_') #нечто вроде 4d22c934.89326920_11.jpg, меняем /, т.к. недопустимый символ
                    img_link = site_root + img_prelink 
                    session = requests.Session()
                    request = session.get(img_link, headers=headers)
                    r = requests.get(img_link, stream=True)
                    image = r.raw.read()
                    open(home + img_subname, "wb").write(image)

                except Exception:
                    pass

    except Exception:
        pass


get_entries_urls()
save()
