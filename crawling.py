# # Voyagerx 를 통한 자막 추출  
# 
# ###   환경 :
#     1) 윈도우  + python 3.7.x  
#     2) 현재 디렉토리에 Chrome_webdriver 존재
#     3) 현재 디렉토리 중 하위 폴더 (movie)에 동영상 파일만 존재  
#     4) 다운로드는 디폴트로 설정된 곳으로 바로 다운로드 됨  

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm_notebook
import time
import pywinauto
import os

from utils import save_text

def crawling(df, chrome_dir, links_videos_texts_dir):
    save_file = links_videos_texts_dir
    with open(save_file, 'a') as f:
        f.write('links,videos,texts\n')

    browser = webdriver.Chrome(chrome_dir)
    browser.get('https://vrew.voyagerx.com/ko/try/')
    wait = WebDriverWait(browser, 4)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'close')))
    browser.find_element_by_class_name('close').click()
    time.sleep(2)
    print('-'*50)

    # 크롤링 루프
    for idx, row in df.iterrows():
        video = row['videos'][2:]
        print(video,'추출')
        
        # 기본 변수 생성
        path = os.path.join(os.getcwd(), video)
        check = browser.find_elements_by_class_name('word')[:10]
        new_check = browser.find_elements_by_class_name('word')[:10]
        # 파일 탭으로 이동
        browser.find_element_by_tag_name('button').click()
        
        # 업로드 클릭
        wait = WebDriverWait(browser, 5)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]')))
        browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]').click()

        # 업로드 실행
        time.sleep(1)
        app = pywinauto.application.Application().connect(title_re='열기')
        app.열기.Edit.SetText(path)
        time.sleep(1)
        app.열기.Button.click()
        try :
            app.열기.Button.click()
        except:
            pass

        # 변환 확인
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'blue-button')))
        browser.find_element_by_class_name('blue-button').click()
        new_check = browser.find_elements_by_class_name('word')[:10]

        i=0
        while check == new_check:
            new_check = browser.find_elements_by_class_name('word')[:10]
            print(i*30,' 초째아직 추출중')
            i += 1
            time.sleep(30)

    
        # 파일 탭에서 추출 누르기, 전체화면 이어야 함
        browser.find_element_by_tag_name('button').click() # 탭
        browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[7]').click()
        browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/ul/li[2]/div/button').click()   
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/label/span[1]').click()
        browser.find_element_by_class_name('blue-button').click() 
        print('추출완료')
        time.sleep(10)
        text_file = save_text(video)
        with open(save_file, 'a') as f:
            f.write('{},{},{}\n'.format(row['links'], row['videos'], text_file))
        print("저장완료")
        print('-'*50)       