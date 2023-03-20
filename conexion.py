import pymysql

def conectar():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='barber_house')