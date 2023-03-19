import os, os.path
import errno
import time
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request
import requests


# Input user for valid 4chan thread link
chan_thread = input('Please insert the url of the fapello profile you want to scrap: ')

# Input user for a folder path to save the media

# folder_path = input('Please insert a folder path to save the media: ')
folder_path = 'N:\TORRENTS\System\_fapello\\'
folder_path.replace("\\","/")
download_video = input('Do you want to try downloading videos too? Type Y or N: ')


# Set up requests
my_url = Request(f"{chan_thread}", headers={'User-Agent': 'Mozilla/5.0'})
uClient = uReq(my_url)
time.sleep(0.5)
page_html = uClient.read()
time.sleep(0.5)
uClient.close()


# html parsing
page_soup = soup(page_html, "html.parser")


# Folder creation function
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# Variables
webm = page_soup.findAll("div",{'class': 'file'})
thread_title = page_soup.findAll("div",{'class': 'max-w-full'})

number = page_soup.findAll("div",{'class': 'flex lg:flex-row flex-col'})

# Number of pages
numbers =[]
for i in number[0]:
    numbers.append(i)

pages_amount = int(numbers[0])
print(f'Number of pages to download: {pages_amount}')

# Avatar
avatars = page_soup.findAll("div",{'class': 'bg-gradient-to-tr'})
avatars_list = []

for i in avatars[-1]:
    for y in i:
        if y != '\n':
            avatars_list.append(y)

avatar = avatars_list[0]['src']

# Scrap the content

profile_name = chan_thread.split('.com/')[-1]
mkdir_p(f'{folder_path}/{profile_name}')

video_pages = []

base_url = chan_thread
counter = 1

for image in range(pages_amount):
    try:
        my_url = Request(f"{base_url}{counter}", headers={'User-Agent': 'Mozilla/5.0'})
        print(f'Analyzing images in page {base_url}{counter} ...')
        uClient = uReq(my_url)
        time.sleep(0.1)
        page_html = uClient.read()
        time.sleep(0.1)
        uClient.close()
        # html parsing
        page_soup = soup(page_html, "html.parser")
        videos = page_soup.findAll('video')
        extended_images = page_soup.findAll('img')

        if videos:
            video_pages.append(counter)
            counter += 1
        else:
            try:
                for image in extended_images:
                    if profile_name in image['src'] and avatar not in image['src']:
                        # extended_image_list.append(image['src'])
                        non_formatted = image['src'].split('/')[-1]
                        webm_link = image['src']
                        webm_data = requests.get(f'{webm_link}').content
                        with open(f'{folder_path}/{profile_name}/{non_formatted}','wb') as handler:
                            handler.write(webm_data)
                        print(f'Image {image["src"]} downloaded successfully!')
                    else:
                        continue
            except:
                continue
            counter += 1
    except:
        pass

print(f'Total of {counter} images downloaded successfully!')

counter = 1
# VIDEO
if download_video.lower() == 'y':
    for page in video_pages:
        try:
            my_url = Request(f"{base_url}{page}", headers={'User-Agent': 'Mozilla/5.0'})
            print(f'Analyzing videos in page {base_url}{page} ...')
            uClient = uReq(my_url)
            time.sleep(0.1)
            page_html = uClient.read()
            time.sleep(0.1)
            uClient.close()
            # html parsing
            page_soup = soup(page_html, "html.parser")
            videos = page_soup.findAll('video')
            try:
                # print('entrou 0')
                for _video in videos:
                    # print('entrou 0.5')
                    for video in _video:
                        try:
                            # extended_image_list.append(image['src'])
                            non_formatted = video['src'].split('/')[-1]
                            webm_link = video['src']
                            webm_data = requests.get(f'{webm_link}').content

                            with open(f'{folder_path}/{profile_name}/{non_formatted}', 'wb') as handler:
                                handler.write(webm_data)
                            print(f'Video {video["src"]} downloaded successfully!')
                            continue
                        except:
                            pass
                            # counter += 1
                # counter += 1
            except:
                pass
                # print('entrou aqui 1')
                # counter += 1

        except:
            continue
            # counter += 1
print(f'Total of {len(video_pages)} videos downloaded successfully!')


