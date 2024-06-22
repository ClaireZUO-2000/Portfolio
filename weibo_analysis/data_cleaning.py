import pandas as pd
import jieba

# 读取停用词表
def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        stopwords = set(line.strip() for line in f)
    return stopwords

stopwords = load_stopwords('stopwords.txt')

# 读取 CSV 文件
df = pd.read_csv('2803301701.csv')

# 分词和去除停用词函数
def jieba_cut(text):
    return ' '.join(jieba.cut(text))

def remove_stopwords(text):
    words = text.split()
    return ' '.join([word for word in words if word not in stopwords])

# 对数据框中的每一行进行分词和去除停用词
df['text'] = df['text'].apply(jieba_cut).apply(remove_stopwords)

# 保存处理后的数据回 CSV 文件
df.to_csv('data_cleaned.csv', index=False)

print("CSV 文件处理完成并保存为 'data_cleaned.csv'")
