from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.edge.service import Service
import time
import random
import datetime
import pandas as pd


# 配置文件部分
# 浏览器位置
broswer_path = 'msedgedriver.exe'
# cookie
cookie_path = '/html/body/div[7]/div[2]/div/div[1]/div/div[2]/div/button[2]'
# 目标url
url = "https://www.proquest.com/advanced?accountid=171768"
# 搜索框
queryfield_path = '#queryTermField'
# 查询文本
wenben = '(“nuclear war*” OR “atomic war*” OR “nuclear missile*” OR “nuclear bomb*” OR “atomic bomb*” OR “h-bomb*” OR “hydrogen bomb*” OR “nuclear test” OR “nuclear weapon*” OR “nuclear proliferation” OR “nuclear program” OR “nuclear weapons” OR “China’s Nuclear Forces”) OR (missile* OR "arms" OR "military power" OR "military equipment" OR WMD OR "weapons of mass destruction" OR "CBRN attack" OR "CBRN threats" OR "biological warfare" OR Biotechnology*) OR ("Internet of Things" OR IoT OR "Artificial Intelligence" OR AI OR "Augmented Reality" OR AR OR "Virtual Reality" OR VR OR "cyber eapability" OR "cyber attacks" OR "cyber threats" OR "cyber espionage" OR 5G OR telecommunication OR 6G OR 2G OR 3G OR 4G OR "digital economy" OR cryptocurrency OR blockchain OR bitcoin OR "distributed sensors" OR "edge computing" OR "autonomous systems" OR "quantum information science" OR QIS OR quantum OR "quantum information*" OR quantum* OR gis* OR "advanced microelectronics" OR "BeiDou Navigation Satellite System") OR ("precision medicine" OR "genomic technologies" OR "space technologies" OR "undersea technologies" OR Robotics OR "decentralized energy methods" OR Nanotechnology OR "new materials")'

# 选定出版物类型中的报纸
newsPapers_xpath = '//*[@id="SourceType_Newspapers"]'
# 选定文档类型
article_xpath = '//*[@id="DocumentType_Article"]'
commentary_xpath = '//*[@id="DocumentType_Commentary"]'
editorial_xpath = '//*[@id="DocumentType_Editorial"]'
feature_xpath = '//*[@id="DocumentType_Feature"]'
frontPage_xpath = '//*[@id="DocumentType_Front_Page/Cover_Story"]'
news_xpath = '//*[@id="DocumentType_News"]'
report_xpath = '//*[@id="DocumentType_Report"]'
review_xpath = '//*[@id="DocumentType_Review"]'
# 选定语言
# 1.定位到语言选择框
js_code = 'document.getElementsByClassName("dySrchScroller")[2].scrollBy(0, document.body.scrollHeight)'
# 2. 定位英语
language_path = '#Language_ENG'
# 月份设置
month = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']
# 自定义日期路径
time_field_path = '//*[@id="select_multiDateRange"]'
# 日期输入框路径
day_path1 = '//*[@id="day2"]'
day_path2 = '//*[@id="day2_0"]'
month_path1 = '//*[@id="month2"]'
month_path2 = '//*[@id="month2_0"]'
year_path1 = '//*[@id="year2"]'
year_path2 = '//*[@id="year2_0"]'
# 搜索按钮路径
search_xpath = '//*[@id="searchToResultPage"]'
# 检索结果路径
result_xpath = '//*[@id="pqResultsCount"]'

# 定义浏览器
def set_broswer(driver_type = 'edge', path = broswer_path):
    if driver_type == 'edge':
        driver = webdriver.Edge(service=Service(path))
    elif driver_type == 'chrome':
        driver = webdriver.Chrome(path)
    else:
        raise ValueError (" use edge or chrome!")
    return driver

# 定义勾选复选框操作
def run_select_config():
    # Source type: Newspapers
    driver.find_element(By.XPATH, newsPapers_xpath).click()
    driver.implicitly_wait(20)

    driver.find_element(By.XPATH,article_xpath).click()
    driver.find_element(By.XPATH,commentary_xpath).click()
    driver.find_element(By.XPATH,editorial_xpath).click()
    driver.find_element(By.XPATH,feature_xpath).click()
    driver.find_element(By.XPATH,frontPage_xpath).click()
    driver.find_element(By.XPATH,news_xpath).click()
    driver.find_element(By.XPATH,report_xpath).click()
    driver.find_element(By.XPATH,review_xpath).click()
    driver.implicitly_wait(20)

    # 定位到语言选择框
    driver.execute_script(js_code)
    # 选择英语//
    driver.find_element(By.CSS_SELECTOR, language_path).click()
    driver.implicitly_wait(20)
    
# 定义保存函数
def save(result_list, begin_time, end_time):
    """定义一个保存函数,时间格式："1990-01"

    Args:
        result_list (list): numresult
        begin_time (str): "1991-01"
        end_time (str): "1991-01"

    Returns:
        _type_: _description_
    """
    date = pd.date_range(start=begin_time, end=end_time,freq='M')
    temp = pd.DataFrame({"date":date,"index":result_list})
    time = "{}-{}".format(begin_time,end_time)
    temp.to_csv('index({}).csv'.format(time),index=False,header=True,encoding='utf8')
    return f"index({time}.csv) save!"

# 定义生成日期函数
def getDate(start_date, end_date):
    """_summary_

    Args:
        start_date (_type_): _description_
        end_date (_type_): _description_

    Returns:
        list: list(元组)：元组第一个元素是月初1号，第二个元素是月末
    """
    dates = []
    current_date = start_date

    while current_date <= end_date:
        if current_date.day == 1:
            last_day = current_date.replace(day=28) + datetime.timedelta(days=4)  # last day of month
            last_day = last_day - datetime.timedelta(days=last_day.day)  # adjust for shorter months
            dates.append((current_date.strftime("%Y-%#m-%#d"), last_day.strftime("%Y-%#m-%#d")))
        current_date += datetime.timedelta(days=1)
    return dates

start_date = datetime.date(1995, 1, 1)
end_date = datetime.date(2023, 4, 30)  # change end_date to last day of month
date_list = getDate(start_date, end_date)

flag = True
while flag:
    try:
        driver = set_broswer('edge')# 这个地方你换成"chrome",然后修改配置文件中的browser_path为你自己的路径就行
        driver.get(url)
        time.sleep(3)
        # 点击确认cookies
        cookie_path = '//*[@id="onetrust-accept-btn-handler"]'
        driver.find_element(By.XPATH, cookie_path).click()
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,cookie_path))).click()
        driver.implicitly_wait(20)
        # 刷新
        driver.refresh()
        driver.implicitly_wait(20)
        # 复选框勾选
        run_select_config()
        results_list = []
        # 选择自定义日期
        Select(driver.find_element(By.XPATH, time_field_path)).select_by_value('RANGE')
        driver.implicitly_wait(20)
        # 主循环
        for (i,j) in date_list:
            # 输入文本
            driver.find_element(By.CSS_SELECTOR, queryfield_path).send_keys(wenben)
            
            # 因为开始日期中的年和月与结束日期中的年和月是一样的，因此不用单独设置结束年和结束月，只要设置结束日就行
            st_y, st_m, st_d = i.split('-')[0],i.split('-')[1],i.split('-')[2]
            ed_d = j.split('-')[2]
            
            # 输入开始日期
            driver.implicitly_wait(20)
            Select(driver.find_element(By.XPATH, day_path1)).select_by_value(st_d)
            time.sleep(random.random()+1.5)
            Select(driver.find_element(By.XPATH, month_path1)).select_by_value(month[int(st_m)-1])
            start_year = driver.find_element(By.XPATH, year_path1)
            start_year.clear()
            start_year.send_keys(st_y)
            
            # 输入结束时间
            driver.implicitly_wait(20)
            Select(driver.find_element(By.XPATH, day_path2)).select_by_value(ed_d)
            Select(driver.find_element(By.XPATH, month_path2)).select_by_value(month[int(st_m)-1])
            end_year = driver.find_element(By.XPATH, year_path2)
            end_year.clear()
            end_year.send_keys(st_y)

            
            # Click Search
            driver.find_element(By.XPATH, search_xpath).click()
            driver.implicitly_wait(20)
            
            # 返回搜索结果数量
            result = driver.find_element(By.XPATH, result_xpath).text
            print(i,' -->', j, ' : ',result)
            results_list.append(result)
            driver.implicitly_wait(20)

            # 找到高级搜索链接并点击跳转
            link_href = driver.find_element(By.XPATH,"//a[contains(text(),'高级检索')]").get_attribute('href')
            driver.get(link_href)
            driver.implicitly_wait(20)
    except:
        # 先保存
        save(results_list, start_date, )
        # 重置开始时间
        start_date = datetime.date(st_y, st_m, st_d)
        date_list = getDate(start_date, end_date)    
    else:
        flag = False