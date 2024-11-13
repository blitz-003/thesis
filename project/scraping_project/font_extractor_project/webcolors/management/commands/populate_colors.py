# your_app/management/commands/populate_colors.py
import os
from django.core.management.base import BaseCommand
from webcolors.models import Country, WebsiteColor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from collections import Counter

from django.core.management.base import BaseCommand
from webcolors.models import Country, WebsiteColor
from colorthief import ColorThief
import os

# class Command(BaseCommand):
#     help = 'Populates the database with website colors'

#     def capture_screenshot(self, url, output_path):
#         options = Options()
#         options.add_argument("--headless")
#         options.add_argument("--window-size=1920x1080")
#         driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
#         driver.get(url)
#         driver.save_screenshot(output_path)
#         driver.quit()

#     def analyze_colors(self, image_path, num_colors=10):
#         color_thief = ColorThief(image_path)
#         palette = color_thief.get_palette(color_count=num_colors)

#         # Calculate total count of colors
#         total_count = sum(palette)

#         # Calculate color percentages
#         colors = [(color, 1 / total_count * 100) for color in palette]


#         return colors






#     def handle(self, *args, **options):
#         country_name = 'us'  # Change to the desired country name
#         websites = [
#             'https://www.google.com', 'https://www.facebook.com', 'https://www.youtube.com','https://www.reddit.com', 'https://www.amazon.com','https://www.yahoo.com','https://www.duckduckgo.com','https://www.wikipedia.org','https://twitter.com','https://www.instagram.com','https://www.taboolanews.com','https://www.bing.com','https://www.weather.com','https://www.nytimes.com','https://www.search.yahoo.com','https://www.cnn.com'
#             # Add more URLs...
#         ]
#         other_websites={
#         'China': [
#             'https://bilibili.com','https://bing.com','https://qq.com','https://www.zhihu.com','https://google.com','https://www.csdn.net','https://www.youtube.com','https://www.douyin.com','https://www.github.com','https://www.weibo.com','https://www.taobao.com','https://www.163.com','https://openai.com','https://www.douyu.com','https://aliyun.com','https://www.sohu.com','https://www.jd.com','https://www.cnblogs.com','https://www.baidu.com', 'https://www.qq.com', 'https://www.taobao.com','https://www.feishu.cn','https://www.huya.com','https://www.xiaohongshu.com'
#             # Add more URLs...
#         ],
#         'India': [
#             'https://www.google.co.in', 'https://www.youtube.com', 'https://www.amazon.in','https://facebook.com','https://www.instagram.com','https://www.whatsapp.com','https://www.cricbuzz.com','https://www.wikipedia.org','https://www.openai.com','https://www.twitter.com','https://www.timesofindia.com','https://www.flipkart.com','https://www.jiocinema.com','https://www.reddit.com','https://www.indiatimes.com'
#             # Add more URLs...
#         ],
#         'Japan': [
#             'https://www.google.co.jp', 'https://www.yahoo.co.jp', 'https://www.amazon.co.jp','https://www.rakuten.co.jp','https://www.ambelo.co.jp','https://www.tenki.co.jp','https://www.instagram.com','https://www.girlschannel.net','https://www.note.com','https://goo.ne.jp','https://togetter.com','https://cookpad.com','https://www.trilltrill.jp', "https://www.tabelog.com","https://kakaku.com","https://www.line.me",'https://www.nhk.or.jp','https://www.wikiwiki.jp','https://www.rakuten.co.jp','https://www.kakuyomu.co.jp','https://www.atwiki.jp', 'https://www.mercari.com'
#             # Add more URLs...
#         ],
#         'South Korea': [
#             'https://www.naver.com', 'https://www.daum.net', 'https://www.google.co.kr',
#             # Add more URLs...
#         ]
#         }

#         # Create or get the country object
#         country, _ = Country.objects.get_or_create(name=country_name)

#         # Directory to save screenshots
#         screenshots_dir = 'screenshots'
#         os.makedirs(screenshots_dir, exist_ok=True)

#         for website in websites:
#             screenshot_path = f'{screenshots_dir}/{website.replace("https://", "").replace("http://", "").replace("/", "_")}.png'
#             self.capture_screenshot(website, screenshot_path)
#             colors = self.analyze_colors(screenshot_path)
#             for color, percentage in colors:
#                 # Save color data to the database
#                 WebsiteColor.objects.create(country=country, website=website, color=color, percentage=percentage)
#                 self.stdout.write(self.style.SUCCESS(f'Added color {color} with percentage {percentage:.2f}% for website {website}'))






# ###############################################################################################################

# from django.core.management.base import BaseCommand
# from webcolors.models import Country, WebsiteColor
# from colorthief import ColorThief
# import os

from django.core.management.base import BaseCommand
from webcolors.models import Country, WebsiteColor
from colorthief import ColorThief
import os

class Command(BaseCommand):
    help = 'Populates the database with website colors'

    def capture_screenshot(self, url, output_path):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        driver.save_screenshot(output_path)
        driver.quit()

    def analyze_colors(self, image_path, num_colors=10):
        color_thief = ColorThief(image_path)
        palette = color_thief.get_palette(color_count=num_colors)

        return palette

    def handle(self, *args, **options):
        country_name = 'us'  # Change to the desired country name
        us_done =['https://www.google.com', 'https://www.facebook.com', 'https://www.youtube.com','https://www.reddit.com', 'https://www.amazon.com','https://www.yahoo.com','https://www.duckduckgo.com','https://www.wikipedia.org','https://twitter.com','https://www.instagram.com','https://www.taboolanews.com',]
        websites = [
           'https://www.bing.com','https://www.weather.com','https://www.nytimes.com','https://www.search.yahoo.com','https://www.cnn.com'
            # Add more URLs...
        ]
        # Create or get the country object
        country, _ = Country.objects.get_or_create(name=country_name)

        # Directory to save screenshots
        screenshots_dir = 'screenshots'
        os.makedirs(screenshots_dir, exist_ok=True)

        for website in websites:
            screenshot_path = f'{screenshots_dir}/{website.replace("https://", "").replace("http://", "").replace("/", "_")}.png'
            self.capture_screenshot(website, screenshot_path)
            colors = self.analyze_colors(screenshot_path)
            for color in colors:
                # Save color data to the database
                WebsiteColor.objects.create(country=country, website=website, color=color)

                # Alternatively, you can store the color as a hexadecimal string
                # hex_color = '#{0:02x}{1:02x}{2:02x}'.format(*color)
                # WebsiteColor.objects.create(country=country, website=website, color=hex_color)

                self.stdout.write(self.style.SUCCESS(f'Added color {color} for website {website}'))
