import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# ChromeDriverオプションを設定
op = Options()
op.add_argument("--disable-gpu")
op.add_argument("--disable-extensions")
op.add_argument("--proxy-server='direct://'")
op.add_argument("--proxy-bypass-list=*")
op.add_argument("--start-maximized")
op.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=op)

try :

    # ページング用パラメータ
    start = 1
    # 次へリンクの有無
    next = True

    # 「次へ」リンクが存在する限り実行
    while next != None:

        # サービス・都道府県から「静岡県」の結果が表示されたページを取得(startでページ数を指定)
        driver.get(f'https://www.kfc.co.jp/search/fuken.html?t=attr_con&kencode=22&start={start}')

        # 描画されるまで5秒程待つ
        time.sleep(5)

        # 描画されたHTMLをBeautifulSoupで解析
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 「次へ」のリンクの有無をチェック
        next = soup.find('li', class_='next')

        # id=outShopの<ul>から
        for ul in soup.find_all('ul', id=['outShop']):
            # class=even or oddの<li>を取得し
            for li in ul.find_all('li', class_=['even', 'odd']):
                # <li>配下の<span>から店名と住所だけを抽出
                shop_name = li.find('span', class_ =['scShopName']).text
                address = li.find('span', class_=['scAddress']).text
                # 表示
                print(f'{shop_name} {address}')
        
        # 「次へ」が存在する場合はページ数をインクリメント
        if next != None:
            start+=1

except Exception as e:
    print('Error', e)

finally:
    # ドライバを終了する
    driver.quit()