import requests
from PIL import Image
from io import BytesIO
import os
import time
from datetime import datetime

time_sleep = 20

image_crawl_info = [
    {'location': 'dinhbolinh_bach_dang', 'id': '5a8253bc5058170011f6eac1',
     'img_path': 'http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=5a8253bc5058170011f6eac1&t=1727798941757'},
    {'location': 'phamvandong_phanvantri2', 'id': '58d7c20ac1e33c00112b321c',
     'img_path': 'http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=58d7c20ac1e33c00112b321c&t=1727799356604'}
]

session = requests.Session()

session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'http://giaothong.hochiminhcity.gov.vn/Map.aspx',
})

session.get('http://giaothong.hochiminhcity.gov.vn/Map.aspx')

base_folder = 'data'
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

def save_image(session, img_url, folder_name, image_id):
    response = session.get(img_url)
    
    if response.status_code == 200:
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y%m%d_%H%M%S')

        img_name = f"{folder_name}/{image_id}_{timestamp}.jpg"

        img = Image.open(BytesIO(response.content))
        img.save(img_name)
        print(f"save image: {img_name}")
    else:
        print(f"cannot save image {img_url}, response: {response.status_code}")

def create_folders(image_crawl_info):
    for location_info in image_crawl_info:
        folder_name = os.path.join(base_folder, location_info['location'])
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

def process_images_sequentially(image_crawl_info):
    for location_info in image_crawl_info:
        folder_name = os.path.join(base_folder, location_info['location'])
        save_image(session, location_info['img_path'], folder_name, location_info['id'])

try:
    create_folders(image_crawl_info)
    while True:
        process_images_sequentially(image_crawl_info)
        print(f"waiting {time_sleep} ...")
        time.sleep(time_sleep)
except KeyboardInterrupt:
    print("Stopped.")
