#/usr/bin/env python3
import requests, os, time, sys
from bs4 import BeautifulSoup as bs
import re
import shutil 
from urllib.request import Request, urlopen  # https://qna.habr.com/q/167569



class DD:

    HOME_DIR = '/home/o/Документы/PYTHON_SCRIPTS/ero/dd/'
    urls = [
        # 'http://vintage-erotica-forum.com/t19047-lynne-austin.html',
        # 'http://vintage-erotica-forum.com/t17350-tiffany-sloan.html'
        # 'http://vintage-erotica-forum.com/t25009-lesley-adams.html'
        # 'http://vintage-erotica-forum.com/t7494-jan-fairbrother.html'
        # 'http://vintage-erotica-forum.com/t15708-jennifer-lyn-jackson.html'
        # 'http://vintage-erotica-forum.com/t6044-janie-dickens.html'
        # 'http://vintage-erotica-forum.com/t2929-danni-ashe.html'
        # 'http://vintage-erotica-forum.com/t264053-adele-rein.html'
        # 'http://vintage-erotica-forum.com/t10822-claire-nicholson.html'
        # 'http://vintage-erotica-forum.com/t5880-vicki-lynn-lasseter.html'
        # 'http://vintage-erotica-forum.com/t15293-pamela-jean-stein.html'
        # 'http://vintage-erotica-forum.com/t6544-wendy-hamilton.html'
        # 'http://vintage-erotica-forum.com/t10567-jolanda-egger.html'
        # 'http://vintage-erotica-forum.com/t315097-katia.html'
        # 'http://vintage-erotica-forum.com/t53989-zahra-norbo.html'
        # 'http://vintage-erotica-forum.com/t201703-sylvia-hand.html'
       # 'http://vintage-erotica-forum.com/t8557-bonnie-logan.html'
       # 'http://vintage-erotica-forum.com/t201391-sasha-vinni.html'
       # 'http://vintage-erotica-forum.com/t8213-candace-l-collins.html'
       # 'http://vintage-erotica-forum.com/t7304-liz-glazowski.html'
       # 'http://vintage-erotica-forum.com/t9128-penelope-parker.html'
       # 'http://vintage-erotica-forum.com/t68754-joanne-szmereta.html'
       # 'http://vintage-erotica-forum.com/t34826-marie-ekorre.html'
       # 'http://vintage-erotica-forum.com/t4575-karen-thornton.html'
       # 'http://vintage-erotica-forum.com/t11737-antonia-bell.html'
       # 'http://vintage-erotica-forum.com/t5578-donna-edmondson.html'
       # 'http://vintage-erotica-forum.com/t201605-stephanie-page.html'
       # 'http://vintage-erotica-forum.com/t173-erica-amp-nicole-amp-jaclyn-dahm.html'
       'http://vintage-erotica-forum.com/t7787-rowan-moore.html'
    ]
    
    headers = {
           'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

   
    def get_name(self, url):
        self.model_name = re.search(r'\d+\-(.*).html', url).group(1)
        print(self.model_name)

        if not os.path.exists(DD.HOME_DIR + self.model_name):
            os.mkdir(DD.HOME_DIR + self.model_name, mode=0o777)
        else:
        	print(f'{DD.HOME_DIR + self.model_name} exists')

        return self.model_name


    def get_soup(self, url):
        self.session = requests.Session()
        self.request = self.session.get(url)
        self.soup = bs(self.request.content, 'html.parser')
        return self.soup


    def get_last_page(self, url):
        self.get_soup(url)
        self.soup = self.get_soup(url)
        
        try:
            self.last_page = self.soup.find('div', class_='pagenav awn-ignore').find('td', attrs={'nowrap': 'nowrap'}).a
            self.last_page = re.search(r'page=(\d+)', self.last_page['href']).group(0).replace('page=', '')
            print(self.last_page)
            

        except Exception as e:
            print(e)
            self.last_page = re.search(r'of (\d*)', self.soup.find('div', class_='pagenav awn-ignore'). \
                             find_all('td')[0].text). \
                             group(0). \
                             replace('of ', '')
            print(self.last_page)

        return self.last_page

    
    def write_all_pages_urls_of_model(self, url):
        f = open(DD.HOME_DIR + self.model_name + '/' + self.model_name + '.txt', 'w')
            
        self.pages_num = self.get_last_page(url)
        for i in range(1, int(self.pages_num) + 1): 
            self.url_ = url.replace(self.model_name, 'p' + str(i) + '-' + self.model_name) 
            print(self.url_)
            f.write(self.url_.strip())
            f.write('\n')

        f.close()
    

    def get_all_fotos_url_of_model(self):
        f = open(DD.HOME_DIR + self.model_name + '/' + self.model_name + '.txt', 'r')
        f2 = open(DD.HOME_DIR + self.model_name + '/' + self.model_name + '_links.txt', 'w')
        for url in f:
            regex = re.compile('.*post_message_.*')
            self.soup = self.get_soup(url)
            self.all_posts = self.soup.find_all('div', attrs={'id': regex})
            
            for i in self.all_posts:
                try:
                    print(i['id'], end='\n')
                    a_ = i.find_all('a', attrs={'target': '_blank'})
                    if not a_ is None:
                        for i_ in a_:
                            self.im = i_['href']  

                            # getting the dinamically changed url
                            self.r = Request(self.im, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)' \
                                                          'AppleWebKit/537.36 (KHTML, like Gecko)' \
                                                          'Chrome/72.0.3626.121 Safari/537.36'})
                            self.webpage = urlopen(self.r)
                            
                            print(self.webpage.geturl())
                            f2.write(self.webpage.geturl())
                            f2.write('\n')

                except TypeError:
                    pass


        f.close()
        f2.close()




dd = DD()

for url in DD.urls:
    dd.get_name(url)
    # dd.get_last_page(url)
    # dd.write_all_pages_urls_of_model(url)
    dd.get_all_fotos_url_of_model()

