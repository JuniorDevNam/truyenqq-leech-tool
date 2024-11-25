import requests
from bs4 import BeautifulSoup
from os.path import join
from os import makedirs
import sys
import time
import random
import re

user_agent_list = [
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
   "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.99 Mobile/15E148 Safari/604.1",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0",
   "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.3"
]


def onechapter(web, headers, output_dir):
    res = requests.get(web,headers=headers)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_tag = soup.find("h1", class_="detail-title txt-primary")
    if h1_tag:
        h1_text = re.sub(r'\s+', ' ', h1_tag.text).strip()
        print(h1_text)
    img_links = []
    for x in soup.find_all("div", class_="page-chapter"):
        for y in x.find_all("img"):
            img_links.append(y.get("data-original"))
    if output_dir == '':
        folder = join(sys.path[0],"downloads",h1_text)
    else:
        folder = join(output_dir,h1_text)
    makedirs(folder, exist_ok=True)
    for index, link in enumerate(img_links):
        print(link)
        file = join(folder,f"image_{index}.jpg")
        response = requests.get(link, headers=headers)
        with open(file, "wb") as f:
            f.write(response.content)
    time.sleep(1)
    print("Xong.")

def allchapters(web, headers, domain):
    res = requests.get(web,headers=headers)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    chapters = []
    for x in soup.find_all("div", class_="works-chapter-item"):
        for y in x.find_all("a"):
            chapters.append(f'{domain}{y.get("href")}')
    chapters = chapters[::-1]
    print(chapters)
    h1_tag = soup.find("h1", attrs={'itemprop': 'name'})
    if h1_tag:
        title = re.sub(r'\s+', ' ', h1_tag.text).strip()
        print(title)
    output_dir = join(sys.path[0],"downloads",title)
    for link in chapters:
        onechapter(link, headers, output_dir)

web = str(input("Nhập đường link của truyện: "))
print("**!** Tool còn nhiều hạn chế, và mình sẽ luôn cố gắng cập nhật để bắt kịp với trang web.")
time.sleep(5)
print("Running...")
referer = f'https://{web.split("/")[2]}/'
domain = f'https://{web.split("/")[2]}'
print("Server:",referer)
headers = {
   'Connection': 'keep-alive',
   'Cache-Control': 'max-age=0',
   'Upgrade-Insecure-Requests': '1',
   'User-Agent': random.choice(user_agent_list),
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   'Accept-Encoding': 'gzip, deflate',
   'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
   'referer': referer
    }
if "chap" in web:
    print("Có vẻ đây là link của 1 chap đơn. Tiến hành tải...")
    output_dir = ''
    onechapter(web, headers, output_dir)
else:
    print("Có vẻ như đây là đường link của cả một truyện. Tiến hành tải tất cả chương mà truyện hiện có...")
    allchapters(web, headers, domain)