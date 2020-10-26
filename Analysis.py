import pandas as pd
from sqlalchemy import create_engine
import jieba
from collections import Counter
import numpy as np

#读取MySQL数据库
engine = create_engine("mysql+pymysql://root:123456@localhost/imdb?charset=utf8mb4")
con = engine.connect()
data = pd.read_sql_table("imdb2",con)
print(data)

print(len(data))
data.drop(columns="id",inplace=False)
data.drop_duplicates(inplace=True)
data.replace(to_replace=r'^\s*$', value=np.nan, regex=True, inplace=True)
data = data.dropna(axis=0, how='any')
data = data[~data['area'].str.contains('语')]
data = data[~data['area'].str.contains('\d{4}-\d{2}-\d{2}')]
data.dropna(inplace=True)
print(len(data))

print(data.columns)#查看列表头

#电影评分
#评分前五十的电影
higth_score=data.sort_values("score",ascending=False).head(200)
higth_score['key']='higth_score'
#分组计算
result = higth_score.groupby('score')
tool_result = []
for i in result:
    field = i[0]
    num = len(i[1])
    tool_result.append((field, num))
#保存数据
scoreDF = pd.DataFrame.from_records(tool_result,columns=['score','num'])
print(scoreDF)
scoreDF.to_sql('score',con,index=False,if_exists='replace')
#存到数据库
hight_resul=higth_score
print(hight_resul)
hight_resul.to_sql('paiming',con,if_exists='replace')

#电影地区
result = data.drop_duplicates('title').groupby('area')
place_result = []
for i in result:
    field = i[0]
    num = len(i[1])
    place_result.append((field, num))
#
areaDF = pd.DataFrame.from_records(place_result,columns=['area','num'])
# print(areaDF)
areaDF.to_sql('area',con,index=False,if_exists='replace')

#电影类型
#提取电影类型
type_cout = '/'.join(list(data['type']))
#对电影类型进行分词
# split_type = jieba.cut(type_cout,cut_all=False)
# split_type = [i for i in split_type if i !=None and i !=',' and i !='/' and len(i)>1]
split_type = type_cout.split('/')
#电影类型词频统计
count_type = Counter(split_type)
type_result = sorted(list(count_type.items()),key=lambda x:x[1],reverse=True)
#保存数据
work_type = pd.DataFrame.from_records(type_result,columns=['type','num'])
# print(work_type)
work_type.to_sql("type",con,if_exists='replace')

#主演和导演
#提取主演和导演
content = ','.join(list(data['actor']))#主演
pairs = ','.join(list(data['director']))#导演
#对主演进行分词
# split_content = jieba.cut(content,cut_all=False)
# split_content = [i for i in split_content if i !=None and i !=',' and i !='/' and len(i)>1]
split_content = content.split(',')
#对导演进行分词
# split_pairs = jieba.cut(pairs,cut_all=False)
# split_pairs = [i for i in split_pairs if i !=None and i !=',' and i !='/' and len(i)>1]
split_pairs = pairs.split(',')
#词频统计
count_content = Counter(split_content)
count_pairs = Counter(split_pairs)
count_content_result = sorted(list(count_content.items()),key=lambda x:x[1],reverse=True)
count_pairs_result = sorted(list(count_pairs.items()),key=lambda x:x[1],reverse=True)
#保存数据
work_count1 = pd.DataFrame.from_records(count_content_result,columns=['name','num'])
work_count2 = pd.DataFrame.from_records(count_pairs_result,columns=['name','num'])
#整合
work_count = work_count1.append(work_count2)
#保存
work_count.to_sql('word_cloud',con,if_exists='replace')






