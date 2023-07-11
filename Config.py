"""
配置文件
"""
# 当前登录用户
CurrentUser = None

# 用户列表
UserList = []

# Cookies字典
CookiesDict = {}

# 实例
Browser = None

# 是否需要登陆，默认读取Cookie登录
login_status = False

# 标题，描述
title = ""
describe = ""

# 图片存放路径
catalog_image = r"C:\Users\Administrator\Desktop\小红书图片素材"
# 文件后缀
suffix = ['.jpg', '.jpeg', '.png', '.webp']

# Excel文件配置
excel_file = r"C:\Users\Administrator\Desktop\小红书文字内容\小红书.xlsx"
sheet_name = "Sheet1"
title_column = "A"
describe_column = "B"

# 图片路径数量
num_images = 0