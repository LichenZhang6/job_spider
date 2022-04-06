import csv
import time
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = Chrome(options=options)
driver.implicitly_wait(10)

job_dict = {
    '计算机软件': '01',
    '会计审计': '41',
}
city_dict = {
    '杭州': '080200',
    '上海': '020000',
    '宁波': '080300',
}
limit = 20

for city_name, city_num in city_dict.items():
    for field_name, field_num in job_dict.items():
        count = 1
        file_name = '{}_{}.csv'.format(city_name, field_name)
        print(file_name[:-4])
        header = ['详细链接', '招聘职位', '发布时间', '工作薪资',
                  '职位详情', '公司链接', '公司名称', '公司性质', '所属行业']
        with open(file_name, 'a', encoding='utf8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        start_url = 'https://search.51job.com/list/{},000000,0000,{},9,99,+,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(
            city_num, field_num)
        while count <= limit:
            print(count, start_url)
            driver.get(start_url)
            time.sleep(1)
            content = driver.page_source
            html = BeautifulSoup(content, 'html.parser')
            for tag in html.find(name='div', attrs={'class': 'j_joblist'}):
                job_link = tag.find('a', href=True)['href']
                title = tag.find('span', title=True)['title']
                release_time = tag.find('span', attrs={'class': 'time'}).text
                salary = tag.find('span', attrs={'class': 'sal'}).text
                job_info = tag.find('span', attrs={'class': 'd at'}).text
                # welfare = tag.find('p', title=True)['title']
                company_link = tag.find(name='div', attrs={'class': 'er'}).find(
                    'a', href=True)['href']
                company_name = tag.find('a', attrs={'class': 'cname at'}).text
                company_type = tag.find('p', attrs={'class': 'dc at'}).text
                field = tag.find('p', attrs={'class': 'int at'}).text
                with open(file_name, 'a', encoding='utf8') as f:
                    writer = csv.writer(f)
                    writer.writerow([job_link, title, release_time, salary,
                                     job_info, company_link, company_name, company_type, field])
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'next'))).click()
            start_url = driver.current_url
            count += 1
driver.quit()
