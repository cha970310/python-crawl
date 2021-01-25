from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
# error solution , chromedriver option 불러와서 에러 처리
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 드라이버 실행
driver = webdriver.Chrome(options=options,executable_path='C:\\Users\\Peter\\Downloads\\chromedriver_win32\\chromedriver')

# 드라이버 주소 이동 명령
# 2s sleep
time.sleep(2)
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")
#  이동할 때 검색(안될 때) 시간 기다리기
driver.implicitly_wait(2)
# searchElem 변수 안에 input클래스 name q; 검색창에 대입 
searchElem = driver.find_element_by_name("q")
# 내가 원하는 검색어 변수 설정. (* 후에 input으로 받아보기)
# searchKey = ''
searchKey=input('검색할 키워드:')
# 내가원하는 검색어 입력
searchElem.send_keys(searchKey)
#  내가원하는 검색어 엔터 전송
searchElem.send_keys(Keys.RETURN)
#  css 셀렉터로 클릭메소드 구현    index[0]은 첫번째, driver.find_elements_by_css_selector('.rg_i.Q4LuWd')[0].click()

SCROLL_PAUSE_TIME=1.3
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector('.mye4qd').click()
        except:
            break
    last_height = new_height

images = driver.find_elements_by_css_selector('.rg_i.Q4LuWd')
count = 1
# images 라는 배열에 전체를 담아줌.
for image in images:
#  image라는 이름의 배열요소들로 반복문
# exception을 요구해서 try 구문
    try:
        # 각기 이미지마다 클릭
        image.click()
        # 2초쉬고
        time.sleep(2)
        # img태그 src 속성주기 + imgUrl 변수에 담기, 그런데 class로 갖고오면 세개가 들어와서 xpath로 하나만 가져오기.
        imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
        # 차단되었을 수도 있어서 추가해준 가상 사용자 코드
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        # 다운로드 로직 구현. imgUrl  변수에서 다운받고 받는 파일명 검색키워드 + 이미지 갯수 + 확장자명
        urllib.request.urlretrieve(imgUrl,searchKey+str(count)+".jpg")
        # 카운트 수 ++
        count= count+1
        # 카운트 30번 됐을때 종료시키기
        if count ==30:
            break

    except:
        pass
driver.close()



