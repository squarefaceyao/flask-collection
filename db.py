from pymysql import connect
from pymysql.cursors import DictCursor # 为了返回字典形式
from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
import pandas

# 类和对象
# 对象是类的实例
# 类是抽象的
# 对象是具像的

class DB(object):
    def __init__(self):  # 创建对象同时要执行的代码
        self.conn = connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset='utf8'
        )
        self.cursor=self.conn.cursor(DictCursor)  # 这个可以让他返回字典的形式

    def __del__(self):  # 释放对象同时要执行的代码
        self.cursor.close()
        self.conn.close()


    def get_signal_values(self):
        # sql = 'select * from rf1_2 limit 3 '
        # sql = "SELECT table_name,create_time FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='test123'"
        sql = "SELECT table_name,create_time,table_rows FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{}'".format(MYSQL_DATABASE)
        self.cursor.execute(sql)
        data = []
        for temp in self.cursor.fetchall():
            data.append(temp)
            # pprint(temp)
        return data

    def chaxun(self,sql):
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def download(self,path,table_name):
        # path 是放文件得路径
        sql = 'select * from ' + table_name
        data = pandas.DataFrame(self.chaxun(sql=sql))
        #把id设置成行索引
        data_1 = data.set_index("id",drop=True)
        #写写入数据数据
        filename= path+'/mysql_{}.csv'.format(table_name)
        pandas.DataFrame.to_csv(data_1,filename,encoding="utf_8_sig")
        print("写入成功")



    def write(self,table_name,ad1,ad2,ad3,ad4,ad5,ad6,ad7,ad8):
        self.cursor.execute("insert into %s(create_time,ad1,ad2,ad3,ad4,ad5,ad6,ad7,ad8) value(now(),'%s','%s','%s','%s','%s','%s','%s','%s')" %(table_name,ad1,ad2,ad3,ad4,ad5,ad6,ad7,ad8))
        self.conn.commit()
        # print("ad成功写入{}表".format(table_name))

    def create(self,table_name):
        # 根据table名字创建table
        sql = """CREATE TABLE `%s` (
                          `id` int(11) NOT NULL AUTO_INCREMENT,
                          `create_time` datetime DEFAULT NULL,
                          `ad1` float(10,5) DEFAULT NULL,
                          `ad2` float(10,5) DEFAULT NULL,
                          `ad3` float(10,5) DEFAULT NULL,
                          `ad4` float(10,5) DEFAULT NULL,
                          `ad5` float(10,5) DEFAULT NULL,
                          `ad6` float(10,5) DEFAULT NULL,
                          `ad7` float(10,5) DEFAULT NULL,
                          `ad8` float(10,5) DEFAULT NULL,
                          PRIMARY KEY (`id`) USING BTREE,
                          KEY `ht_create_time_index` (`create_time`) USING BTREE
                        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='ad表';
        """ % (table_name)
        # 简单判断下，存在表需要删除
        # self.delete()
        # print('存在表，已删除{}'.format(self.table))
        try:
            self.cursor.execute(sql)
        except:
            print("不用创建啦，存在该{}表！！！,将往该表写入ad值，如需创建请更换表名，操作将继续进行...............".format(table_name))
        else:
            print('创建{}成功'.format(table_name))

if __name__ == '__main__':
    db=DB()
    db.create('sssssss')






