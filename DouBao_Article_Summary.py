# 导入所需的库
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pyperclip
import time
import getpass
import sys  # 导入 sys 模块以获取命令行参数
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 获取文件路径作为参数
if len(sys.argv) < 2:
    print("请提供文件路径作为参数。")
    sys.exit(1)

file_path = sys.argv[1]  # 从命令行参数获取文件路径
print(file_path)

# 获取当前用户的用户名
username = getpass.getuser()
# 设置用户 Chrome 配置文件路径
user_profile_path = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data' % username
print(user_profile_path)

# 配置 Chrome 驱动选项
options = Options()
options.add_argument(f"user-data-dir={user_profile_path}")

# 等待 5 秒以确保环境准备好
time.sleep(5)

# 初始化 WebDriver
driver = webdriver.Chrome(options=options)

try:
    # 打开目标网页
    driver.get('https://www.doubao.com/chat/')  # 替换为你要抓取的网址

    # 等待页面加载
    time.sleep(2)

    # 模拟鼠标操作，点击“新对话”按钮
    element_to_click = driver.find_element(By.XPATH, "//*[text()='新对话']")  
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    # 点击“阅读总结”按钮
    element_to_click = driver.find_element(By.XPATH, "//*[text()='阅读总结']")  
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    # 等待操作完成
    time.sleep(2)

    # 上传文件
    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file_path)

    # 提示词输入框
    iuput_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='chat_input_input']") 
    iuput_field.send_keys("详细整理这篇文档，输出格式清晰的总结")

    # 发送按钮
    element_to_click = driver.find_element(By.ID, "flow-end-msg-send") 
    is_disabled = True

    # 等待发送按钮可用
    while is_disabled:
        try:
            time.sleep(1)
            print(element_to_click.is_enabled())
            is_disabled = not element_to_click.is_enabled()
        except:
            print("except")  # 状态变化时可能会抛出异常
            break

    # 点击发送按钮
    actions = ActionChains(driver)
    time.sleep(3)
    actions.move_to_element(element_to_click).click().perform()

    # 等待生成的内容可用
    generating = True
    while generating:
        try:
            element_to_click = driver.find_element(By.CSS_SELECTOR, "[data-testid='message_action_copy']")
            generating = False
        except:
            time.sleep(5)
    
    # 点击复制生成的内容
    actions = ActionChains(driver)
    actions.move_to_element(element_to_click).click().perform()

    # 获取剪贴板内容
    clipboard_content = pyperclip.paste()

    # 打印剪贴板内容
    print(clipboard_content)

    # 将内容写入文件
    with open("sample.txt", "w", encoding="utf-8") as file:
        file.write(clipboard_content)

    # 点击发送按钮
    element_to_click = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'chat-message-container')]/div[contains(@class, 'flex flex-col')]/div[contains(@class, 'self-end')]/div[contains(@class, 'items-center')]/button[contains(@class, 'p-1 rounded-md')]")))
    element_to_click.click()

finally:
    # 关闭浏览器
    # driver.quit()
    pass
