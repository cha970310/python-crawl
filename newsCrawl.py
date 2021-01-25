import sys, os
import requests
import selenium
from selenium import webdriver
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pickle, progressbar, json, glob, time
from tqdm import tqdm

###### 날짜 저장 ##########
date = str(datetime.now())
date = date[:date.rfind(':')].replace(' ', '_')
date = date.replace(':','시') + '분'

sleep_sec = 1.3


####### 언론사별 본문 위치 태그 파싱 함수 ###########
print('본문 크롤링에 필요한 함수를 로딩하고 있습니다...\n' + '-' * 100)
def crawling_main_text(url):

    req = requests.get(url)
    req.encoding = None
    soup = BeautifulSoup(req.text, 'html.parser')
    
    # 연합뉴스
    if ('://yna' in url) | ('app.yonhapnews' in url): 
        main_article = soup.find('div', {'class':'story-news article'})
        if main_article == None:
            main_article = soup.find('div', {'class' : 'article-txt'})
            
        text = main_article.text
     
    # 매일경제(미라클), req.encoding = None 설정 필요
    elif 'mirakle.mk' in url:
        text = soup.find('div', {'class' : 'view_txt'}).text
        
    # 매일경제, req.encoding = None 설정 필요
    elif 'mk.co' in url:
        text = soup.find('div', {'class' : 'art_txt'}).text
        
    #서울신문

    elif 'seoul.co.kr' in url:
        main_article = soup.find('div',{'id':'atic_txt1'})
        if main_article == None:
                main_article = soup.find('div',{'id':'atic_txt1'})
        text=main_article.text  
# 그 외
    else:
        text == None
        
    return text.replace('\n','').replace('\r','').replace('<br>','').replace('\t','')
    
    
press_list = ['경향신문','국민일보','내일신문','동아일보','서울신문','세계일보','아시아투데이','조선일보','중앙일보',]

print('검색할 언론사 : {} | {}개 \n'.format(press_list, len(press_list)))


############### 브라우저를 켜고 검색 키워드 입력 ####################
query = input('검색할 키워드  : ')
news_num = int(input('수집 뉴스의 수(숫자만 입력) : '))

print('\n' + '=' * 100 + '\n')

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
print('브라우저를 실행시킵니다(자동 제어)\n')
chrome_path = '크롬드라이버 '
browser = webdriver.Chrome(options=options,executable_path=chrome_path)

news_url = 'https://search.naver.com/search.naver?where=news&query={}'.format(query)
browser.get(news_url)
time.sleep(sleep_sec)


sortByCurrent =  browser.find_element_by_xpath('//*[@id="main_pack"]/div[1]/div[1]/a[2]')  
sortByCurrent.click()
######### 언론사 선택 및 confirm #####################
print('설정한 언론사를 선택합니다.\n')
search_opt_box = browser.find_element_by_xpath('//*[@id="search_option_button"]')
search_opt_box.click()
time.sleep(0.1)

press_box = browser.find_element_by_xpath('//*[@id="snb"]/div/ul/li[5]')
press_box.click()
#경제 전체
press_category_box =browser.find_element_by_xpath('//*[@id="order_cat"]/div[1]/div/a[1]')
li_list = press_category_box.find_elements_by_xpath('//*[@id="ca_p1"]')
li_list[0].click()
# 확인 버튼
press_button  = browser.find_element_by_xpath('//*[@id="snb"]/div/ul/li[5]/div/span/span[1]/button/span')
press_button.click()

################ 뉴스 크롤링 ########################

print('크롤링을 시작합니다.')
time.sleep(sleep_sec)
# ####동적 제어로 페이지 넘어가며 크롤링
news_dict = {}
idx = 1
cur_page = 1

pbar = tqdm(total=news_num)

while idx < news_num:

    table = browser.find_element_by_xpath('//*[@id="main_pack"]/section/div/div[3]/ul')
    table_li_list = table.find_elements_by_xpath('//*[@id="sp_nws1"]/div')
    li_a_list = [t_li.find_element_by_xpath('//*[@id="sp_nws1"]/div/div/a') for t_li in table_li_list]

    for n in li_a_list[:min(len(li_a_list), news_num-idx+1)]:
        n_url = n.get_attribute('href')
        news_dict[idx] = {'title' : n.get_attribute('title'), 
                          'url' : n_url,
                          'text' : crawling_main_text(n_url)}
        
        idx += 1
        pbar.update(1)
        ㅁ
    if idx < news_num:
        cur_page +=1

        pages = browser.find_element_by_xpath('//div[@class="paging"]')
        next_page_url = [p for p in pages.find_elements_by_xpath('.//a') if p.text == str(cur_page)][0].get_attribute('href')

        browser.get(next_page_url)
        time.sleep(sleep_sec)
    else:
        pbar.close()
        
        print('\n브라우저를 종료합니다.\n' + '=' * 100)
        time.sleep(0.1)
        browser.close()
        break

#### 데이터 전처리하기 ###################################################### 

print('데이터프레임 변환\n')
news_df = DataFrame(news_dict).T

folder_path = os.getcwd()
xlsx_file_name = '네이버뉴스_본문_{}개_{}_{}.xlsx'.format(news_num, query, date)

news_df.to_excel(xlsx_file_name)

print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))

os.startfile(folder_path)

print('=' * 100 + '\n결과물의 일부')
news_df
