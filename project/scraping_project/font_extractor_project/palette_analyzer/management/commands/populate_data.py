# palette_analyzer/management/commands/populate_data.py
import time
from io import BytesIO
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from colorthief import ColorThief
from PIL import Image
from palette_analyzer.models import Website

class Command(BaseCommand):
    help = 'Populate the database with top 20 websites for each country'

    COUNTRIES = ['America', 'China', 'India', 'Japan', 'South Korea']
    TOP_WEBSITES = {
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

    def handle(self, *args, **kwargs):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        for country in self.COUNTRIES:
            top_sites = self.TOP_WEBSITES[country]
            for url in top_sites:
                palette = self.fetch_palette(driver, url)
                if palette:
                    Website.objects.update_or_create(
                        url=url,
                        country=country,
                        defaults={'palette': palette}
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully added palette for {url}'))
        driver.quit()

    def fetch_palette(self, driver, url):
        try:
            driver.get(url)
            time.sleep(2)  # Give the page time to load
            screenshot = driver.get_screenshot_as_png()
            image = Image.open(BytesIO(screenshot))
            color_thief = ColorThief(image)
            palette = color_thief.get_palette(color_count=10)  # Assuming up to 10 colors
            return palette
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching {url}: {e}'))
        return None
