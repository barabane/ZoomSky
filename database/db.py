import os
from loguru import logger
from mysql.connector import connect, Error

class DataBase:
    def __init__(self) -> None:
        self.conn = connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            db=os.environ.get('DB_NAME'),
            port=os.environ.get('DB_PORT')
        )
        self.curr = self.conn.cursor()

        try:
            if self.conn.is_connected():
                self.curr.execute("""CREATE TABLE IF NOT EXISTS user (
                    id BIGINT PRIMARY KEY,
                    username VARCHAR(100),
                    reg_date DATE,
                    city_name VARCHAR(200),
                    coordinates TEXT              
                )""")
            logger.info('DB successfully connected!')
        except Error as e:
            logger.error(f'Error while connecting to MySQL: {e}')

    def update_user(self, user):
        user_exists = self.get_user(user['id'])
        
        if user_exists:
            self.curr.execute("UPDATE user SET id = %s, username = %s, city_name = %s,coordinates = %s", 
                        (user['id'], user['username'], user['city_name'], user['coordinates']))
            self.conn.commit()
            return
        
        self.curr.execute("INSERT INTO user (id,username,reg_date,city_name,coordinates) VALUES (%s,%s,%s,%s,%s)", 
                        (user['id'], user['username'], user['reg_date'], user['city_name'], user['coordinates']))
        self.conn.commit()
        
    def get_user(self, id: int):
        self.curr.execute(f"SELECT * FROM user WHERE id={id}")
        
        return self.curr.fetchone()
    
db = DataBase()