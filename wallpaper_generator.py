import os
import base64
import json
import time
import requests
import random
from config import API_KEY, API_URL, WALLPAPER_DIR, MODEL, WALLPAPER_SIZE
from PIL import Image

class WallpaperGenerator:
    def __init__(self):
        self.api_url = API_URL
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

    def generate_wallpaper(self, prompt, max_retries=3, retry_delay=5):
        width, height = map(int, WALLPAPER_SIZE.split('x'))
        
        payload = {
            "model": MODEL,
            "prompt": f"{prompt} The image should be in {width}x{height} resolution, perfect for a desktop wallpaper.",
            "n": 1,
            "size": WALLPAPER_SIZE,
            "seed": random.randint(1, 4294967295)  # 使用随机种子
        }

        for attempt in range(max_retries):
            try:
                print(f"尝试 {attempt + 1}/{max_retries} 生成壁纸")
                print(f"使用提示词: {prompt}")
                print(f"图片尺寸: {WALLPAPER_SIZE}")
                print(f"使用种子: {payload['seed']}")
                
                response = requests.post(self.api_url, json=payload, headers=self.headers)
                response.raise_for_status()
                
                result = response.json()
                image_url = result['data'][0]['url']
                
                # 下载图片
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                
                os.makedirs(WALLPAPER_DIR, exist_ok=True)
                
                file_name = f"wallpaper_{prompt[:10]}_{os.urandom(4).hex()}.png"
                file_path = os.path.join(WALLPAPER_DIR, file_name)
                
                with open(file_path, 'wb') as f:
                    f.write(image_response.content)
                
                print(f"壁纸已保存到: {file_path}")
                return file_path
            except Exception as e:
                print(f"生成壁纸失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                else:
                    print("达到最大重试次数，放弃。")
                    return None

    def get_screen_resolution(self):
        screen = screeninfo.get_monitors()[0]
        return screen.width, screen.height

    def adjust_image(self, image_path, target_width, target_height):
        with Image.open(image_path) as img:
            # 计算缩放比例，保持原始宽高比
            img_ratio = img.width / img.height
            target_ratio = target_width / target_height

            if img_ratio > target_ratio:
                # 图片较宽，以高度为基准缩放
                new_height = target_height
                new_width = int(new_height * img_ratio)
            else:
                # 图片较高，以宽度为基准缩放
                new_width = target_width
                new_height = int(new_width / img_ratio)

            # 调整图片大小
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img.save(image_path)
