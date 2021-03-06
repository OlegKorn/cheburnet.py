import requests, os
from bs4 import BeautifulSoup as bs
import re



headers = {'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}



class Downloader:

    url = 'https://www.erosberry.com/model/Nansy_A.html'
    url_root = 'https://www.erosberry.com'
    root_dir = '/home/o/Документы/LINUXOLEG/py/ero/erosberry.com/'

    model_name = re.search('model/(.*).html', url).group(1) 
    print(model_name)   
    model_dir = root_dir + model_name

    posts_file = model_name + '_posts.txt' 
    #imgs_file =  model_dir + '/' + '_imgs2.txt'


    def __init__(self):
        if not os.path.exists(Downloader.model_dir):
            os.mkdir(Downloader.model_dir)
            print('Folder "{}" created'.format(Downloader.model_dir))
        else: 
            print('{} already exists'.format(Downloader.model_dir))



    def get_request(self, x):
        self.req = requests.get(x, stream=True)
        return self.req



    def get_soup(self, url):
        self.session = requests.Session()
        self.request = self.session.get(url, headers=headers)
        self.soup = bs(self.request.content, 'html.parser')
        
        return self.soup



    def get_posts(self):
        self.f_posts = open(Downloader.posts_file, 'w')

        for post in self.soup.find('div', attrs={'girl_thumbs'}).find_all('div', attrs={'container'}):
            post_link = Downloader.url_root + post.a.get('href').strip()
            self.f_posts.write(post_link + '\n')

        self.f_posts.close()



    def get_imgs(self):

        self.f_posts = open(Downloader.posts_file, 'r')

        for post in self.f_posts:
            x = re.search('com/(.*)', post)
            marker = x.group(1)     #iveta-the-front-office-by-mpl-studios
 
            self.imgs = self.get_soup(post.strip())
                
            for i in self.imgs.find('div', id='photo').find_all('div', attrs={'container'}):
                must_match = i.a.get('href')
                
                if marker in must_match:
                    print(i.img['src'])
                    img = 'http://' + i.img['src'].replace('//c', 'c').replace('tn_', '').strip()
                                         
                    #скачиваем картинку
                    self.r = self.get_request(img)
                    self.image = self.r.raw.read()

                    print(Downloader.model_dir + '/' + img[44:-4].replace('/', '_') + '.jpg')
                    open(Downloader.model_dir + '/' + img[44:-4].replace('/', '_') + '.jpg', "wb").write(self.image)

            del self.imgs


          


d = Downloader()
#d.get_soup(Downloader.url)
#d.get_posts()
d.get_imgs()



'''
import requests, sys, time
from bs4 import BeautifulSoup as bs
import wget


URL = 'https://www.erosberry.com/model/Veronika_F.html'

MODEL_NAME = 'veronica-f'

home = 'G:/Desktop/py/eb/veronika-f/'
fi = home + MODEL_NAME + '_erosberry.txt'
fi1 = home + MODEL_NAME + '_erosberry_links.txt'



def main():
    
    f = open(fi, 'w')

    try: 
        session = requests.Session()
        request = session.get(URL)
        soup = bs(request.content, 'html.parser')

        for imgset in soup.find('div', class_='girl_thumbs') \
                          .find_all('div', class_='container'):
            set_link = 'https://www.erosberry.com' + imgset.a['href'].strip()
            f.write(set_link + '\n')

    except Exception as e:
        print(e)
        pass

    f.close()



def save_urls():
    
    f = open(fi, 'r')
    file = f.readlines()
    f1 = open(fi1, 'w')
    
    for img_url in file:

        img_url_replaced = img_url.replace('\n', '')
        pattern = img_url_replaced.replace('https://www.erosberry.com/', '')

        session = requests.Session()
        request = session.get(img_url_replaced)
        soup = bs(request.content, 'html.parser')
            
        #image link
        for post in soup.find_all('a'):
            try:
                link = post['href']
                if pattern in link:
                    print(link)
                    f1.write('https://www.erosberry.com' + link)
                    f1.write('\n')

            except Exception:
                pass

        print(img_url_replaced + '\n')

    f.close()
    f1.close()


def save_img():

    f = open(fi1, 'r')
    
    for i in f:
        
        try:            
            i = i.strip()
            pattern = i.replace('https://www.erosberry.com/', '') \
                       .replace('.html', '')

            print('==================')
            print(i)
            print('==================')

            session = requests.Session()
            request = session.get(i)
            soup = bs(request.content, 'html.parser')
            
            img_ = soup.find('a', class_='photo').img['src']
            
            img_link = 'https:' + img_.strip()
            image_title = img_link[len(img_link)-6:len(img_link)]
            print(pattern + image_title)

            # wget.download(img_link, 'G:/Desktop/py/eb/')
            r = requests.get(img_link, stream=True)
            image = r.raw.read()
            open(home + pattern + image_title, "wb").write(image)
        
        except Exception:
            print('error')
            continue
        
    f.close()

# main()
# save_urls()
save_img()
'''
