# 【爬虫+数据清洗+数据可视化】Python分析人民日报微博近五日发布内容


## 一、数据准备

### 1.使用开源Crawler对微博内容进行抓取：https://github.com/dataabc/weibo-crawler/tree/master
### 2.安装依赖库:
   ```pip install -r requirements.txt```
### 3.在config文件中修改配置，确保抓取到自己所需数据:
   ```
{"user_id_list": ["2803301701"],
    "only_crawl_original": 1,
    "since_date": 5,
    "start_page": 1,
    "write_mode": ["csv", "json"],
    "original_pic_download": 0,
    "retweet_pic_download": 0,
    "original_video_download": 0,
    "retweet_video_download": 0,
    "download_comment": 1,
    "comment_max_download_count": 100,
    "download_repost": 0,
    "repost_max_download_count": 0,
    "user_id_as_folder_name": 0,
    "remove_html_tag": 1,
    "cookie": "your cookie",
  }
```
#### 配置说明
##### **user_id_list**代表我们要爬取的微博用户的user_id，可以是一个或多个，也可以是文件路径，例如人民日报微博uid为2803301701。
###### 如何获取user_id：
![image](https://github.com/ClaireZUO-2000/Portfolio/assets/172008743/e2993d0f-561e-4566-9220-1b1cc2c03c7b)
###### 进入用户主页，网址栏将显示https://m.weibo.cn/u/2803301701?...，其中u/后面的一串数字就是user_id。
##### **only_crawl_original**的值为1代表爬取全部原创微博，值为0代表爬取全部微博（原创+转发）；
##### **since_date**代表我们要爬取since_date日期之后发布的微博，因为我要爬迪丽热巴的全部原创微博，所以since_date设置了一个非常早的值；
##### query_list代表要爬取的微博关键词，为空（[]）则爬取全部；
##### **write_mode**代表结果文件的保存类型，我想要把结果写入csv文件和json文件，所以它的值为["csv", "json"]；
##### **original_pic_download**值为1代表下载原创微博中的图片，值为0代表不下载；
##### **retweet_pic_download**值为1代表下载转发微博中的图片，值为0代表不下载；
##### **original_video_download**值为1代表下载原创微博中的视频，值为0代表不下载；
##### **retweet_video_download**值为1代表下载转发微博中的视频，值为0代表不下载；,,,,likes,comment_number,repost_number,tag,@用户,date
### 4.得到原始数据集（2803301701.csv）:
#### 字段说明

| Option         | Description                             | Default Value |
|----------------|-----------------------------------------|---------------|
| `bid`   | 序号     | `48144574285026`       |
| `text` | 正文  | `【#华山绝美云海武侠感拉满#】近日，陕西...`  |
| `img_url`  | 原始图片url |   |
| `video_url`  | 原始视频url| `https://f.video.weibocdn.com/o0/Sm003t5Klx08fQJTG6BW01041200g4cy0E010.mp4?label=mp4_720p&template=720x1280.24.0&ori=0&ps=1Cx9YB1mmR49jS&Expires=1719059453&ssig=8tJVI76r05&KID=unistore,video`|
| `location`  | 地点 |   |
| `date`  | 发布日期 | `2024-06-22T16:24:08`  |
| `tools`  | 发布渠道 | `微博视频号`  |
| `likes`  | 点赞数量 | `1954`  |
| `comment_number`  | 评论数量 | `479`  |
| `repost_number`  | 转发数量 | `208`  |
| `tag`  | 话题 | `高校毕业季设巨型花束打卡点`  |
| `@用户`  | @用户| `@北京科技大学`  |
| `time`  | 发布时间 | `2024/6/22 19:15:19`  |

## 二、数据清洗
### 1.分词和去除停用词:
```
import pandas as pd
import jieba #jieba是常用的中文文本处理工具，主要用于中文分词
```
#### 如果没有jieba，可以通过pip安装
```
pip install jieba
```
安装后相应库后，即可使用分词与去除停用词进行数据清理
```
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
```
#### 停用词表还可以通过txt文件形式自定义，通常命名为'stopwords.txt'
![image](https://github.com/ClaireZUO-2000/Portfolio/assets/172008743/e8984763-9e74-44db-b63c-42db10a5544e)

## 三、数据分析可视化
### 1.情感分析可视化:
```
import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
```
#### 如果没有相应库，可以通过pip安装
```
pip install snownlp\matplotlib
```
#### df情感分析函数
```
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
```
#### 绘制可视化图像
```
# 绘制饼图
plt.figure(figsize=(8, 8))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])  #图像颜色在此处修改
plt.title('Sentiment Distribution') #图像标题在此处修改
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
```
##### 得出结论：人民日报近五日微博内容八成以上为积极情感倾向（正面宣传为主）
![image](https://github.com/ClaireZUO-2000/Portfolio/assets/172008743/818e11c9-ea10-48bc-bee4-e26264814a11)
### 2.最受欢迎内容:
#### 通过matplotlib可以直观展示近五日人们对什么内容感兴趣
```
#导入相应库
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
```
#### matplotlib生成中文图表时要记得设置字体，避免乱码
```
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
```
#### 结果展示：
![image](https://github.com/ClaireZUO-2000/Portfolio/assets/172008743/ec279766-5141-4747-9280-dfa70a6c174c)
#### 还可以生成词云
```
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
```
#### 结果展示：
![image](https://github.com/ClaireZUO-2000/Portfolio/assets/172008743/6028ca5f-6bf2-4a38-85dd-bd60da722f47)
## 四、总结
以上可视化结果可以验证，近五日人民日报发布微博内容以正面内容为主。人们主要关注话题为高考、毕业季以及台岛问题等
