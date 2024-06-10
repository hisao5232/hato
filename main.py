from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

#変数定義
href_list=[]
detail_list=[]
url="https://www.hatomarksite.com/search/zentaku/agent/area/08"

#トップページ表示
driver.get(url)
time.sleep(3)

#チェックボックスを見るため画面スクロール
driver.execute_script("window.scrollTo(0, 400)")
time.sleep(3)

#市町村チェックボックの数取得
check_boxes=driver.find_elements(By.CSS_SELECTOR,"div.area-container>div>label")
i=0
for i in range(len(check_boxes)):
    #チェックボックス１つクリック
    check_boxes_t=driver.find_elements(By.CSS_SELECTOR,"div.area-container>div>label")
    check_boxes_t[i].click()
    time.sleep(1)

#検索ボタンクリック
driver.find_element(By.CSS_SELECTOR,"div.sticky-footer>button").click()
time.sleep(3)
    
#1ページ目の各社のhref要素取得
a_tags=driver.find_elements(By.CSS_SELECTOR,"div.ms-auto>a")

#hrefのみリストに格納
for a_tag in a_tags:
    href=a_tag.get_attribute("href")
    href_list.append(href)
    print((len(href_list)))

#次のページへクリック
while True:
    try:
        driver.find_element(By.CSS_SELECTOR,'a[aria-label="Next"]').click()
        print("next_page")
        time.sleep(3)

        #現在のページの各社のhref要素取得
        a_tags=driver.find_elements(By.CSS_SELECTOR,"div.ms-auto>a")

        #hrefのみリストに追加
        for a_tag in a_tags:
            href=a_tag.get_attribute("href")
            href_list.append(href)

    #次のページがない場合
    except:
        print("page_end")
        print(len(href_list))
        break

#詳細取得
for shop_href in href_list:
    #会社詳細のページへ移動
    driver.get(shop_href)
    time.sleep(3)

    #詳細取得
    name=driver.find_element(By.CSS_SELECTOR,"div.agent-name").text
    name=name.replace("\u3000"," ")
    address=driver.find_element(By.XPATH,"//p[contains(text(), '住所')]/following-sibling::p").text
    address=address.replace("\u3000"," ")
    tell=driver.find_element(By.XPATH,"//p[contains(text(), '連絡先')]/following-sibling::p").text
    tell_t=tell.split()
    tell=tell_t[0]
    tell=tell.replace("[TEL]","")
    fax=tell_t[1]
    fax=fax.replace("[FAX]","")
    ceo=driver.find_element(By.XPATH,"//p[contains(text(), '代表者')]/following-sibling::p").text
    ceo=ceo.replace("\u3000"," ")
    dict_detail={"会社名":name,"会社住所":address,"TELL番号":tell,"FAX番号":fax,"代表者名":ceo}
    print(dict_detail)
    detail_list.append(dict_detail)

driver.quit()

#エクセル出力
df=pd.DataFrame(detail_list)
df.to_excel("hato_ibaragi_deta.xlsx")