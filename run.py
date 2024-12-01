import requests
from bs4 import BeautifulSoup
from os.path import join
from os import makedirs
import sys
import time
import random
import re

debug_html = join(sys.path[0],"debug.html")
debug_html_ch = join(sys.path[0],"debug_ch.html")

start_time = time.time()

#https://stackoverflow.com/questions/14587728/what-does-this-error-in-beautiful-soup-means
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
    #debug
    #with open(debug_html_ch, 'w', encoding='utf8') as f:
    #    f.write(str(soup))
    # Tìm thẻ h1 có class
    h1_tag = soup.find("h1", class_="detail-title txt-primary")

    # Trích xuất văn bản từ thẻ h1
    if h1_tag:
        #h1_text = h1_tag.text.replace("\n","").strip()
        #h1_text = re.sub(r'\s+', ' ', h1_text).strip()
        h1_text = re.sub(r'\s+', ' ', h1_tag.text).strip()
        print(h1_text)
    img_links = []
    for x in soup.find_all("div", class_="page-chapter"):#, id="image"):
        for y in x.find_all("img"):
            img_links.append(y.get("data-original"))
    #debug
    print(img_links)
    #parts = web.split("/")
    #title_tag = soup.find('title')
    #title = title_tag.string.replace(":"," -")
    #title = web.split("/")[-1]
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

def allchapters(web, headers, domain, parts_only=False, part_start = int(), part_end = int()):
    res = requests.get(web,headers=headers)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    chapters = []
    for x in soup.find_all("div", class_="works-chapter-item"):
        for y in x.find_all("a"):
            chapters.append(f'{domain}{y.get("href")}')
    chapters = chapters[::-1]
    print(chapters)
    #title_tag = soup.find("title")
    #title = title_tag.string
    h1_tag = soup.find("h1", attrs={'itemprop': 'name'})
    # Trích xuất văn bản từ thẻ h1
    if h1_tag:
        #h1_text = h1_tag.text.replace("\n","").strip()
        #h1_text = re.sub(r'\s+', ' ', h1_text).strip()
        title = re.sub(r'\s+', ' ', h1_tag.text).strip()
        print(title)
    output_dir = join(sys.path[0],"downloads",title)
    if parts_only:
        for x in range(part_start, part_end):
            link = chapters[x-1]
            onechapter(link, headers, output_dir)
    else:
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
   #'referer': random.choice(reffer_list)
   'referer': referer
    }
if "chap" in web:
    print("Có vẻ đây là link của 1 chap đơn. Tiến hành tải...")
    output_dir = ''
    onechapter(web, headers, output_dir)
else:
    print("Có vẻ như đây là đường link của cả một truyện.")
    print("Bạn muốn tải tất cả các chương truyện hiện có hay chỉ một phần?")
    choose = input("(T) Toàn Bộ - (M) Một Phần: ")
    if choose == "T":
        print("Bạn đã chọn tải toàn bộ các chương truyện.")
        print("Tiến hành tải tất cả chương mà truyện hiện có...")
        allchapters(web, headers, domain)
    elif choose == "M":
        print("Bạn đã chọn tải một phần của truyện.")
        print("Xin hãy nhập phần các chương bạn muốn tải:")
        print("""Ví dụ:
                Đầu: 60
                Cuối: 100
                Vậy chương trình sẽ tiến hành tải các chương từ 60 đến 100.
        """)
        part_start = int(input("Đầu: "))
        part_end = int(input("Cuối: "))
        print("Tiến hành tải tất cả chương trong phần được chỉ định...")
        allchapters(web, headers, domain,parts_only=True,part_start=part_start,part_end=part_end)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Thời gian chạy: {elapsed_time} giây")
print("Tất cả đã hoàn thành!")
input("Nhấn Enter để tiếp tục...")