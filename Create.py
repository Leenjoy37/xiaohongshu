import os.path
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import Config
import openpyxl
from openpyxl import load_workbook
import random


def create(create_js):
    print("等待资源上传……")
    time.sleep(10)
    create_js = f'return document.querySelector("{create_js}")'
    Config.Browser.execute_script(create_js).click()
    print("发布成功！")
    print("等待页面返回！")
    time.sleep(5)



def input_content():
    # 打开Excel文件
    wb = openpyxl.load_workbook(Config.excel_file)

    # 选择工作表
    sheet = wb[Config.sheet_name]

    # 获取标题和描述的内容
    title = sheet[Config.title_column + '2'].value
    describe = sheet[Config.describe_column + '2'].value

    # 如果标题或描述为空，则弹出提示
    if title is None or describe is None:
        print("标题或描述为空，请检查 Excel 文件的第二行内容。")
        return

    # 删除对应行的内容
    sheet.delete_rows(2)

    # 保存Excel文件
    wb.save(Config.excel_file)

    # 关闭Excel文件
    wb.close()

    # 将内容保存到 Config 对象
    Config.title = title
    Config.describe = describe

    # 使用 Config.Browser 对象进行操作
    Config.Browser.find_element(By.CSS_SELECTOR, ".c-input_inner").send_keys(Config.title)
    Config.Browser.find_element(By.CSS_SELECTOR, "#post-textarea").send_keys(Config.describe)

# def input_content():
#     Config.title = input("请输入标题：")
#     Config.describe = input("请输入描述：")
#     Config.Browser.find_element(By.CSS_SELECTOR, ".c-input_inner").send_keys(Config.title)
#     Config.Browser.find_element(By.CSS_SELECTOR, "#post-textarea").send_keys(Config.describe)


def get_video():
    while True:
        path_mp4 = input("视频路径：")
        path_cover = input("封面路径(不输入使用默认封面)：")
        if not os.path.isfile(path_mp4):
            print("视频不存在！")
        elif path_cover != '':
            if not os.path.isfile(path_cover):
                print("封面图片不存在")
            else:
                return path_mp4, path_cover
        else:
            return path_mp4


def create_video():
    path_mp4, path_cover = get_video()

    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, "div.tab:nth-child(1)")).click()
    except TimeoutException:
        print("网页好像加载失败了！请重试！")

    # 点击上传视频
    Config.Browser.find_element(By.CSS_SELECTOR, ".upload-input").send_keys(path_mp4)
    time.sleep(10)
    WebDriverWait(Config.Browser, 20).until(
        EC.presence_of_element_located((By.XPATH, r'//*[contains(text(),"重新上传")]'))
    )
    while True:
        time.sleep(3)
        try:
            Config.Browser.find_element(By.XPATH, r'//*[contains(text(),"重新上传")]')
            break
        except Exception:
            print("视频还在上传中···")

    if path_cover != "":
        Config.Browser.find_element(By.CSS_SELECTOR, "button.css-k3hpu2:nth-child(3)").click()

        Config.Browser.find_element(By.XPATH, r'//*[text()="上传封面"]').click()
        # 上传封面
        Config.Browser.find_element(By.CSS_SELECTOR, "div.upload-wrapper:nth-child(2) > input:nth-child(1)").send_keys(
            path_cover)

        # 提交封面
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".css-8mz9r9 > div:nth-child(1) > button:nth-child(2)")).click()
    input_content()
    # 发布
    create(".publishBtn")


# def get_image():
#     while True:
#         path_image = input("图片路径：").split(",")
#         if 0 < len(path_image) <= 9:
#             for i in path_image:
#                 if not os.path.isfile(i):
#                     print("图片不存在！")
#                     break
#             else:
#                 return "\n".join(path_image)
#         else:
#             print("图片最少1张，最多9张")
#             continue


def get_image():
    folder_path = Config.catalog_image  # 从配置文件中获取图片存放路径

    if not os.path.isdir(folder_path):
        print("图片文件夹不存在！")
        return None

    image_files = os.listdir(folder_path)
    if not image_files:
        print("图片文件夹中没有图片文件！")
        return None

    num_images = input("请输入要获取的图片数量：")
    try:
        num_images = int(num_images)
        if 0 < num_images <= len(image_files):
            num_images = min(num_images, 9)  # 限制图片数量为最大 9
            selected_images = random.sample(image_files, num_images)
            selected_paths = [os.path.join(folder_path, image) for image in selected_images]

            # 删除对应的图片文件
            # for path in selected_paths:
            #     os.remove(path)

            return "\n".join(selected_paths)
        else:
            print(f"请输入有效的图片数量（范围：1-{len(image_files)}）")
            return None
    except ValueError:
        print("请输入有效的整数")
        return None


def create_image():
    path_image = get_image()
    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, "div.tab:nth-child(2)")).click()
    except TimeoutException:
        print("网页好像加载失败了！请重试！")
    #  上传图片
    Config.Browser.find_element(By.CSS_SELECTOR, ".upload-wrapper > div:nth-child(1) > input:nth-child(1)").send_keys(
        path_image)
    input_content()

    create("button.css-k3hpu2:nth-child(1)")
