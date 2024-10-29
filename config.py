# 配置文件
import os

API_KEY = "填你的API_KEY"  # 请替换为你的实际密钥
API_URL = "https://api.siliconflow.cn/v1/images/generations"
MODEL = "black-forest-labs/FLUX.1-schnell"
WALLPAPER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wallpaper")  # 当前文件夹下的wallpaper子文件夹
CHANGE_INTERVAL = 300  # 更换壁纸的间隔(秒)
WALLPAPER_SIZE = "2560x1600"  # 屏幕比例的分辨率

# 不同类型的 prompt
PROMPTS = {
    "美女": "Full-body shot of a young beautiful sexy chinese female model in a photoshoot, looking directly at the camera. Real photo, The image is enticing and refreshing, showcasing a great figure. Captured with a professional camera in 4:3 aspect ratio.",
    "风景": "A breathtaking landscape scene with mountains, lakes, and forests. Vibrant colors and dramatic lighting. Captured with a high-resolution camera.",
    "抽象": "An abstract digital artwork with vibrant colors and geometric shapes. Modern and visually striking design.",
    "动物": "A close-up portrait of a majestic wild animal in its natural habitat. Sharp details and expressive eyes.",
    "城市": "A stunning cityscape at night, showcasing modern architecture and city lights. Long exposure shot with a wide-angle lens."
}

# 默认 prompt 类型
DEFAULT_PROMPT_TYPE = "风景"
