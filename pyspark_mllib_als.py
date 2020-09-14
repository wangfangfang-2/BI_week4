# coding=utf-8
# 使用pyspark-ALS进行矩阵分解
from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS
import os
os.environ['PYSPARK_PYTHON']='/usr/local/bin/python3'
print("使用Spark-ALS算法") 
sc = SparkContext('local', 'MovieRec')
# 读取数据，需要第一行不是列名
rawUserData = temp = sc.textFile('./ratings_small_without_header.csv')
print(rawUserData.count())
print(rawUserData.first())
"""100004                                                                          
1,31,2.5,1260759144
[['1', '31', '2.5'], ['1', '1029', '3.0'], ['1', '1061', '3.0'], ['1', '1129', '2.0'], ['1', '1172', '4.0']]"""
rawRatings = rawUserData.map(lambda line: line.split(",")[:3])
print(rawRatings.take(5))
training_RDD = rawRatings.map(lambda x: (x[0], x[1], x[2]))

# 模型训练
rank = 3
model = ALS.train(training_RDD, rank, seed=5, iterations=10, lambda_=0.1)
# 针对user_id = 100的用户进行Top-N推荐
print(model.recommendProducts(100, 5))

"""[Rating(user=100, product=67504, rating=5.61383724956478), Rating(user=100, product=83359, 
rating=5.61383724956478), Rating(user=100, product=83411, rating=5.61383724956478), 
Rating(user=100, product=83318, rating=5.61383724956478), Rating(user=100, product=3216, 
rating=5.40984140528023)]"""