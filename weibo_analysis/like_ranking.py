import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 读取 CSV 文件
df = pd.read_csv('data_cleaned.csv')

# 选择点赞量最高的前十项
top10 = df.nlargest(10, 'likes', keep='first')[::-1]

# 设置中文字体
# 对于 Windows 系统，假设字体文件路径为 C:\Windows\Fonts\simhei.ttf
# 对于 MacOS 系统，假设字体文件路径为 /System/Library/Fonts/STHeiti Light.ttc
font_path = "C:\\Windows\\Fonts\\Dengl.ttf"  # 请根据实际情况调整路径

# 创建字体属性对象
my_font = fm.FontProperties(fname="C:\\Windows\\Fonts\\Dengl.ttf")

# 创建绘图
plt.figure(figsize=(10, 6))

# 绘制条形图
plt.barh(top10['tag'], top10['likes'], color='skyblue')  # 假设标题列为 'title'

# 添加标题和标签，指定字体属性
plt.title('十大点赞数量最高tag', fontproperties=my_font)
plt.xlabel('点赞数', fontproperties=my_font)
plt.ylabel('Tag', fontproperties=my_font)

# 设置刻度字体
plt.xticks(fontproperties=my_font)
plt.yticks(fontproperties=my_font)

# 显示绘图
plt.show()
