import os
import django
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from collections import Counter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'font_extractor_project.settings')
django.setup()

from webcolors.models import Country, WebsiteColor

def capture_screenshot(url, output_path):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    driver.save_screenshot(output_path)
    driver.quit()

def analyze_colors(image_path, num_colors=10):
    image = Image.open(image_path)
    image = image.convert('RGB')
    image = image.resize((100, 100))
    result = image.quantize(colors=num_colors)
    palette = result.getpalette()
    color_counts = Counter(result.getdata())
    colors = []
    for color, count in color_counts.items():
        r, g, b = palette[color*3:color*3+3]
        colors.append((f'#{r:02x}{g:02x}{b:02x}', count))
    total_count = sum(count for _, count in colors)
    return [(color, count / total_count * 100) for color, count in colors]

def populate_database(country_name, websites):
    country, created = Country.objects.get_or_create(name=country_name)
    for website in websites:
        screenshot_path = f'screenshots/{website.replace("https://", "").replace("http://", "").replace("/", "_")}.png'
        capture_screenshot(website, screenshot_path)
        colors = analyze_colors(screenshot_path)
        for color, percentage in colors:
            WebsiteColor.objects.create(country=country, website=website, color=color, percentage=percentage)



# Example usage
websites = {
        'America': [
            'https://www.google.com', 'https://www.facebook.com', 'https://www.youtube.com','https://www.reddit.com', 'https://www.amazon.com','https://www.yahoo.com','https://www.duckduckgo.com','https://www.wikipedia.org','https://twitter.com','https://www.trc.taboola.com','https://www.instagram.com','https://www.taboolanews.com','https://www.bing.com','https://www.weather.com','https://www.microsoftonline.com','https://www.nytimes.com','https://www.search.yahoo.com','https://www.cnn.com'
            # Add more URLs...
        ],
        'China': [
            'https://bilibili.com','https://bing.com','https://qq.com','https://www.zhihu.com','https://google.com','https://www.csdn.net','https://www.youtube.com','https://www.douyin.com','https://www.github.com','https://www.weibo.com','https://www.taobao.com','https://www.163.com','https://openai.com','https://www.douyu.com','https://aliyun.com','https://www.sohu.com','https://www.jd.com','https://www.cnblogs.com','https://www.baidu.com', 'https://www.qq.com', 'https://www.taobao.com','https://www.feishu.cn','https://www.huya.com','https://www.xiaohongshu.com'
            # Add more URLs...
        ],
        'India': [
            'https://www.google.co.in', 'https://www.youtube.com', 'https://www.amazon.in','https://facebook.com','https://www.instagram.com','https://www.whatsapp.com','https://www.cricbuzz.com','https://www.wikipedia.org','https://www.openai.com','https://www.twitter.com','https://www.timesofindia.com','https://www.flipkart.com','https://www.jiocinema.com','https://www.reddit.com','https://www.indiatimes.com'
            # Add more URLs...
        ],
        'Japan': [
            'https://www.google.co.jp', 'https://www.yahoo.co.jp', 'https://www.amazon.co.jp','https://www.rakuten.co.jp','https://www.ambelo.co.jp','https://www.tenki.co.jp','https://www.instagram.com','https://www.girlschannel.net','https://www.note.com','https://goo.ne.jp','https://togetter.com','https://cookpad.com','https://www.trilltrill.jp', "https://www.tabelog.com","https://kakaku.com","https://www.line.me",'https://www.nhk.or.jp','https://www.wikiwiki.jp','https://www.rakuten.co.jp','https://www.kakuyomu.co.jp','https://www.atwiki.jp', 'https://www.mercari.com'
            # Add more URLs...
        ],
        'South Korea': [
            'https://www.naver.com', 'https://www.daum.net', 'https://www.google.co.kr',
            # Add more URLs...
        ]
    }

populate_database('us', websites['America'])

