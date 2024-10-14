# 导入必要的库
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pyperclip
import time
import getpass

# 获取当前用户名并设置Chrome用户数据目录路径
username = getpass.getuser()
user_profile_path = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data' % username
print(user_profile_path)

# 设置要处理的文件路径
file_name = "20240517 上午第2节.txt"
file_path = r'D:\My.Dev\DouBao\DouBao_Art_Summary\SampleTxt\%s' % file_name
print(file_path)

# 配置Chrome选项
options = Options()
options.add_argument(f"user-data-dir={user_profile_path}")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

# 等待5秒
time.sleep(5)

# 使用配置的选项初始化WebDriver
driver = webdriver.Chrome(options=options)

try:
    # 打开豆包AI的聊天页面
    driver.get('https://www.doubao.com/chat/')

    # 等待页面加载
    time.sleep(2)

    # 点击"新对话"按钮
    element_to_click = driver.find_element(By.XPATH, "//*[text()='新对话']")  
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    # 点击"阅读总结"按钮
    element_to_click = driver.find_element(By.XPATH, "//*[text()='阅读总结']")  
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    # 等待操作完成
    time.sleep(2)

    # 上传文件
    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file_path)

    # 在提示词输入框中输入文本
    iuput_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='chat_input_input']")
    iuput_field.send_keys("详细整理这篇文档，输出格式清晰的总结")

    # 等待发送按钮变为可用状态
    element_to_click = driver.find_element(By.ID, "flow-end-msg-send")
    is_disabled = True
    while is_disabled:
        try:
            time.sleep(1)
            print("发送按钮 状态： " + str(element_to_click.is_enabled()))
            is_disabled = not element_to_click.is_enabled()
        except:
            print("except: 状态变化的时候，element 会变化报错")
            break

    # 点击发送按钮
    element_to_click = driver.find_element(By.ID, "flow-end-msg-send")
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    # 等待生成完成
    generating = True
    while generating:
        try:
            element_to_click = driver.find_element(By.CSS_SELECTOR, "[data-testid='message_action_copy']")
            generating = False
        except:
            time.sleep(5)

    # 点击复制按钮
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    # 等待5秒
    time.sleep(5)

    # 获取剪贴板内容
    clipboard_content = pyperclip.paste()

    # 打印剪贴板内容
    print(clipboard_content)

    # 等待10秒
    time.sleep(10)

    # 将内容写入文件
    with open("sample.txt", "w", encoding="utf-8") as file:
        file.write(clipboard_content)

finally:
    # 脚本结束，但不关闭浏览器
    pass
