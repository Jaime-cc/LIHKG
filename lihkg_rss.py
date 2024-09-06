import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 獲取 LIHKG 頁面
url = 'https://lihkg.com/category/1'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 解析網頁內容
posts = soup.find_all('div', class_='thread')  # 確保選擇正確的類名

# 創建 RSS 源
rss_items = []
for post in posts:
    title = post.find('a', class_='title').text
    link = post.find('a', class_='title')['href']
    pub_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    rss_items.append(f"""
    <item>
        <title>{title}</title>
        <link>{link}</link>
        <description>Discussion on LIHKG</description>
        <pubDate>{pub_date}</pubDate>
    </item>
    """)

rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>LIHKG Discussion Forum</title>
    <link>{url}</link>
    <description>Latest discussions on LIHKG</description>
    {''.join(rss_items)}
  </channel>
</rss>
"""

# 將 RSS 源寫入文件
with open('lihkg_feed.xml', 'w', encoding='utf-8') as f:
    f.write(rss_feed)

print("RSS feed has been created as 'lihkg_feed.xml'.")