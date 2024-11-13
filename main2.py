import time
from time import sleep
# 导入selenium包
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
# 打开Edge浏览器
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

edge_options = Options()
edge_options.add_argument("--disable-save-password-bubble")
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
edge_options.add_argument('--disable-blink-features=AutomationControlled')
# 创建一个Edge浏览器实例
driver = webdriver.Edge(options=edge_options)
driver.get("https://www.csdn.net/")  # 打开网页
driver.maximize_window()  # 最大化
wait = WebDriverWait(driver, 3)  # 等待网页加载完成

# 等待登录按钮出现
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".toolbar-btn-loginfun"))).click()
# 切换到login iframe 中
login_iframe = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "iframe[name='passport_iframe']")))
driver.switch_to.frame(login_iframe)
time.sleep(5)
print("阶段一")
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-box-tabs-items > span:last-child"))).click()
# 输入用户名和密码
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))).send_keys(
    "19847776607")
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']"))).send_keys(
    "JUEYU0905..")
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".icon-nocheck"))).click()
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-form-item button"))).click()
time.sleep(2)
print("go on!!!")

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
wait.until(EC.visibility_of_element_located((By.ID, "cke_36"))).click()
import_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label[for='import-markdown-file-input']")))
import_button.click()
while True:
    pass

wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "cke_button cke_button__switchmarkdown cke_button_off"))).click()



# 定位到文章内容  寻找类为
# <body class="htmledit_views cke_editable cke_editable_themed cke_contents_ltr cke_show_borders" contenteditable="true" spellcheck="false" style="height: auto; min-height: auto;"><p>454544546546544654654564564</p><p>5456454564545645646</p><p><br></p><p>4546545456454564564564</p><p><br></p><p><br></p></body>

content=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'htmledit_views cke_editable cke_editable_themed cke_contents_ltr cke_show_borders')))
# 清空文章内容
content.clear()
# 自动填写文章内容
content.send_keys("这篇文章的内容是CSDN发表文章自动化")

sleep(5)
