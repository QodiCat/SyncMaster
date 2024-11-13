import time
from time import sleep
# 导入selenium包
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
# 打开Chome浏览器
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--disable-save-password-bubble")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# 创建一个Chrome浏览器实例
driver = webdriver.Chrome(chrome_options)
driver.get("https://www.csdn.net/")  # 打开网页
driver.maximize_window()  # 最大化
wait = WebDriverWait(driver, 3)  # 等待网页加载完成
# 等待登录按钮出现
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".toolbar-btn-loginfun"))).click()
# 切换到login iframe 中
login_iframe = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "iframe[name='passport_iframe']")))
driver.switch_to.frame(login_iframe)
time.sleep(2)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-box-tabs-items > span:last-child"))).click()
# 输入用户名和密码
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))).send_keys(
    "XXXXXXXXXXX")
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']"))).send_keys(
    "XXXXXXXXXXX")
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".icon-nocheck"))).click()
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-form-item button"))).click()
time.sleep(2)
print("go on!!!")
# 切回默认上下文
driver.switch_to.default_content()
# browser.refresh()0
driver.get("https://mp.csdn.net/mp_blog/creation/editor?spm=1000.2115.3001.5352")  # 打开"发布-写文章"页面
wait = WebDriverWait(driver, 3)
#定位到文章标题
title = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtTitle"]')))
#清空文章标题
title.clear()
#自动填写文章标题
title.send_keys("这篇文章的标题是CSDN发表文章自动化")
sleep(5)
driver.quit()