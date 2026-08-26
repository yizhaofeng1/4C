import pymysql
import os
from pymysql.constants import CLIENT
conn=None
try:
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="ShanHaiJin",
        local_infile=True,
        client_flag=CLIENT.LOCAL_FILES,
        charset='utf8mb4'
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'shanhaijin.csv')

    # 转换路径分隔符为Linux风格
    file_path = file_path.replace('\\', '/')

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV文件不存在：{file_path}")

    with conn.cursor() as cur:
        SQL = f"""
        LOAD DATA LOCAL INFILE '{file_path}'
        INTO TABLE shj
        FIELDS TERMINATED BY ',' 
        ENCLOSED BY '"'
        LINES TERMINATED BY '\\n'
        IGNORE 1 ROWS;
        """
        cur.execute(SQL)
        conn.commit()
        print(f"成功导入 {cur.rowcount} 行数据")

except Exception as e:
    print(f"错误发生：{str(e)}")
finally:
    if conn.open and conn:
        conn.close()