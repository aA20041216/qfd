from util import *
import time
import sys
import os

# 从accounts.txt读取账号信息
with open("accounts.txt", "r") as f:
    accounts = [line.strip().split("-") for line in f.readlines() if line.strip() and "-" in line]

img_path = os.getcwd() + "/1.png"

@retry(stop_max_attempt_number=5)
def moyupai(username, password):
    try:
        driver = get_web_driver()
        driver.get("https://www.91tvg.com")
        
        # 登录
        driver.find_element_by_xpath("//input[@placeholder='请输入手机号']").send_keys(username)
        driver.find_element_by_xpath("//input[@type='password' and @class='input' and @placeholder='请输入密码']").send_keys(password)
        driver.find_element_by_xpath("//button[@class='primary-btn' and text()='登录']").click()
        
        time.sleep(3)
        
        # 处理"已读"按钮 - 只在检测到时点击
        try:
            if driver.find_elements_by_xpath("//button[@class='ann-primary' and text()='已读']"):
                driver.find_element_by_xpath("//button[@class='ann-primary' and text()='已读']").click()
                print(f'{username} 已点击"已读"按钮')
                time.sleep(1)
            else:
                print(f'{username} 未检测到"已读"按钮，继续执行')
        except Exception as e:
            print(f'{username} 处理"已读"按钮时出错: {str(e)}，继续执行签到流程')
        
        # 签到流程
        if driver.find_elements_by_xpath("//span[text()='签到']"):
            driver.find_element_by_xpath("//span[text()='签到']").click()
            time.sleep(2)
            
            if driver.find_elements_by_xpath("//span[contains(text(), '立即签到')]"):
                driver.find_element_by_xpath("//span[contains(text(), '立即签到')]").click()
                print(f'{username} moyupai签到成功')
            else:
                print(f'{username} 未找到立即签到按钮，可能已签到')
        else:
            print(f'{username} 未找到签到按钮')
            
    except Exception as e:
        print(f'{username} 签到失败: {str(e)}')
        raise
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == '__main__':
    print(f"开始执行签到，共有 {len(accounts)} 个账号")
    
    for i, account in enumerate(accounts, 1):
        if len(account) == 2:
            username, password = account
            print(f"正在处理第 {i} 个账号: {username}")
            try:
                moyupai(username, password)
                print(f"第 {i} 个账号处理完成")
            except Exception as e:
                print(f"第 {i} 个账号处理失败: {str(e)}")
            
            if i < len(accounts):  # 不是最后一个账号时等待
                print("等待5秒后处理下一个账号...")
                time.sleep(5)
        else:
            print(f"账号格式错误: {'-'.join(account)}")
    
    print("所有账号处理完成！")
