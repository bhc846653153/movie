# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# class TutorialPipeline(object):
#     def process_item(self, item, spider):
#         return item

class MysqlPipeline(object):
    """
    同步操作
    """

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect('localhost', 'root', '123456', 'IMDB',charset='utf8')  # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()

    def __init_mysqlDB(self):
        self.cursor.execute("show tables;")
        #无表则创建
        if "imdb2" not in [_[0] for _ in self.cursor.fetchall()]:
            self.cursor.execute('''
            CREATE TABLE `imdb2` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `title` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
              `year` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
              `director` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
              `actor` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
              `type` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
              `area` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
              `score` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=1678 DEFAULT CHARSET=utf8;
            ''')
            self.conn.commit()
            #有表则清空
        else:
            self.cursor.execute('truncate table imdb2')
            self.conn.commit()


    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
        insert into imdb2(title,year,director,actor,type,area,score) VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['title'], item['year'], item['director'], item['actor'], item['type'], item['area'], item['score'],
                                         ))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
