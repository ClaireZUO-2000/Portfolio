import pandas as pd
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 读取CSV文件
df = pd.read_csv('data_cleaned.csv')

# 确保CSV文件中有一个名为'text'的列，包含文本数据
text_data = df['text'].dropna().tolist()  # 将文本数据转换为列表

# 将文本数据合并成一个字符串
all_text = ' '.join(text_data)


# 从stopwords.txt文件中读取停用词列表
def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f]
    return set(stopwords)

# 加载停用词列表
stopwords_file = 'stopwords.txt'
stop_words = load_stopwords(stopwords_file)

# 分词并去除停用词
def cut_text(text):
    words = jieba.cut(text)
    return ' '.join([word for word in words if word.strip() and word not in stop_words])

# 分词并去除停用词
cut_words = cut_text(all_text)

# 使用Counter统计词频
word_counts = Counter(cut_words.split())

# 获取频率最高的前50个词
top_words = word_counts.most_common(20)

# 提取词和词频
words = [word for word, count in top_words]
counts = [count for word, count in top_words]

# 设置中文字体
font_path = "C:\Windows\Fonts\Dengl.ttf"  # 替换为你下载的中文字体文件路径
font = FontProperties(fname="C:\Windows\Fonts\Dengl.ttf" , size=10)

# 绘制词云
plt.figure(figsize=(10, 8))
plt.barh(words, counts, color='skyblue')
plt.xlabel(' ', fontsize=14)
plt.ylabel(' ', fontsize=14)
plt.title(' ', fontsize=16)
plt.gca().invert_yaxis()  # 反转y轴，让词频高的词显示在上面
plt.xticks(fontsize=10)
plt.yticks(fontsize=10, fontproperties=font)
plt.show()
