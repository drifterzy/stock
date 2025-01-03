import pymysql

conn = pymysql.connect(
    host="localhost",
    port=3306,
    database="stock",
    user="root",
    password="123456"
)
print("Connection successful!")
conn.close()
