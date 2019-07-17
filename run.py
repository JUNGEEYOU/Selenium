from selenium import webdriver as wd
from selenium.webdriver.common.by import By
# 명시적 대기를 위해서
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# 인터파크 투어 사이트에서 여행지를 입력 후 검색 -> 잠시후 -> 결과
# 로그인 시, PC 웹 사이트에서 처리가 어려울 경우 -> 모바일 로그인 진입
# 1. 모듈 가져오기
 # pip install selenium

# 2. 사전에 필요한 정보를 로드 => 디비 or 쉘, 베치 파일에서 인자로 받아서 세팅
main_url = "https://tour.interpark.com/"
keyword = "괌"

# 3. 드라이버 로드
    # 차후 -> 옵션 부여하여( 프록시, 에이전트 조작, 이미지를 배제)
    # 크롤링을 오래돌리면 => 임시파`일들이 쌓인다!!!! -> tmp 파일 삭제
driver = wd.Chrome(executable_path='./chromedriver.exe')

# 4. 사이트 접속 (get)
driver.get(main_url)

# 5. 검색창을 찾아서 검색어 입력 : .send_keys
    # id : SearchGNBText
    # find_element: 한개 / find_elements: 여러개
    # 수정할 경우, 뒤에 내용이 붙어 버림 => .clear() => send_keys(내용)
driver.find_element_by_id('SearchGNBText').send_keys(keyword)

# 6. 검색 버튼 클릭: .click()
    # class: search-btn
driver.find_element_by_css_selector('button.search-btn').click()

# 7. 잠시 대기 => 페이지가 로드되고 나서 즉각적으로 데이터를 획득하는 행위는 자제 필요
    # 1) 명시적 대기 => 특정 요소가 발견될때까지 대기
try:
    element = WebDriverWait(driver, 10).until(
        # 지정한 한개 요소가 올라오면 웨이트 종료
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'oTravelBox'))
    )
except Exception as e:
    print("오류 발생", e)
    # 2) 암묵적 대기=> dom이 다 로드될 때까지 대기하고 먼저 로드되면 바로 진행
    # driver.implicitly_wait(10)

# 8. 더보기 클릭 => 게시판 진입
driver.find_element_by_css_selector('div.oTravelBox > ul > li.moreBtnWrap > .moreBtn').click()

# 게시판에서 데이터를 가져올 때, 데이터가 많으면 세션(로그인을 해서 접근되는 사이트린 경우> 특정 단위별로 로그아웃 로그인 계속 시도)
# 특정 게시물이 사라질 경우 => 팝업 발생(없는 경우....) => 팝업 처리 검토
# 게시판 스캔 시, => 임계점을 모름! => 수집이 안되는 순간
# 게시판 스캔 => 메타 정보 획득 => loop를 돌려서 일괄적으로 방문 접근 처리
# 페이지 이동 : searchModule.SetCategoryList(2, '') 스크립트 실행!!!
# 68은 임시값, 게시물을 넘어갈 경우 현상을 확인차
for page in range(1,68):
    try:
        # 자바스트립트 구동하기
        driver.execute_script("searchModule.SetCategoryList(%s, '')" %page)
        time.sleep(2)
        print("%s 페이지 이동" %page)
    except Exception as e1:
        print('오류',  e1)
