import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt

# 读取 CSV 文件
df = pd.read_csv('data_cleaned.csv')

# 定义情感分析函数
def analyze_sentiment(text):
    s = SnowNLP(text)
    return s.sentiments

# 对文本列进行情感分析
df['sentiment'] = df['text'].apply(analyze_sentiment)

# 定义情感分类
def sentiment_category(score):
    if score > 0.6:
        return 'positive'
    elif score < 0.4:
        return 'negative'
    else:
        return 'neutral'

# 将情感得分分类
df['sentiment_category'] = df['sentiment'].apply(sentiment_category)

# 统计情感分类的分布
sentiment_counts = df['sentiment_category'].value_counts()

# 绘制饼图
plt.figure(figsize=(8, 8))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Sentiment Distribution')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
