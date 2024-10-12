from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pyperclip
import time
import getpass

# 设置 Chrome 驱动路径
# driver_path = 'D:\Workplace\SOM10_SSME\Somaris10\packages\Selenium.Chrome.WebDriver.78.0.0\driver\chromedriver.exe'  # 替换为你的 chromedriver 路径
# driver_path = r"C:\Users\z004m64b\Downloads\chromedriver_win32\chromedriver.exe"
# driver = webdriver.Chrome()

username = getpass.getuser()
user_profile_path = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data' % username
print(user_profile_path)

file_name = "20240517 上午第2节.txt"
file_path = r'D:\My.Dev\DouBao\DouBao_Art_Summary\SampleTxt\%s' % file_name
print(file_path)

options = Options()
options.add_argument(f"user-data-dir={user_profile_path}")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

# Specify the profile directory (e.g., Profile 1, Profile 2)
# options.add_argument("profile-directory=Profile 1")

time.sleep(5)

# Initialize the WebDriver with the specified options
driver = webdriver.Chrome(options=options)


try:
    # time.sleep(15)
    # 打开网页
    driver.get('https://www.doubao.com/chat/')  # 替换为你要抓取的网址

    # 等待页面加载
    time.sleep(2)

    # 抓取网页内容
    # page_content = driver.page_source
    # print(page_content)
    
    # 模拟鼠标操作，例如点击一个元素
    element_to_click = driver.find_element(By.XPATH, "//*[text()='新对话']")  
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    element_to_click = driver.find_element(By.XPATH, "//*[text()='阅读总结']")  
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    # 等待操作完成
    time.sleep(2)

    # element_to_click = driver.find_element(By.XPATH, "//*[text()='浏览文件']")  # 替换为你要点击的元素的 XPath
    # actions = ActionChains(driver)
    # actions.move_to_element(element_to_click).click().perform()

    # time.sleep(2)

    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file_path)

    # uploadingfile = True
    # while uploadingfile:
    #     try:
    #         element_to_click = driver.find_element(By.XPATH, "//*[contains(text(), '输出格式清晰的总结')]")  
    #         uploadingfile = False
    #     except:
    #         time.sleep(5)
    
    iuput_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='chat_input_input']") # 提示词输入框
    iuput_field.send_keys("详细整理这篇文档，输出格式清晰的总结")

    element_to_click = driver.find_element(By.ID, "flow-end-msg-send") # 发送按钮
    is_disabled = True

    while is_disabled:
        try:
            time.sleep(1)
            print("发送按钮 状态： " + str(element_to_click.is_enabled()))
            is_disabled = not element_to_click.is_enabled()
        except:
            print("except: 状态变化的时候，element 会变化报错") # 状态变化的时候，element 会变化报错
            break

    element_to_click = driver.find_element(By.ID, "flow-end-msg-send") # 发送按钮
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    generating = True
    while generating:
        try:
            element_to_click = driver.find_element(By.CSS_SELECTOR, "[data-testid='message_action_copy']")
            generating = False
        except:
            time.sleep(5)
    
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    # Get the current contents of the clipboard
    clipboard_content = pyperclip.paste()

    # Print the clipboard content
    print(clipboard_content)

    with open("sample.txt", "w", encoding="utf-8") as file:
        file.write(clipboard_content)

finally:
    # 关闭浏览器
    # driver.quit()
    pass