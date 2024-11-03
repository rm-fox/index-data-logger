
import pandas as pd
from enum import Enum
from logger_secrets import DB_PASSWORD, DB_HOST
from sqlalchemy import create_engine
import pymysql

class Indices:
    def __init__(self, name, time, price):
        self.index_name = name
        self.index_name_db = f'{self.index_name}_db'
        self.db_host = DB_HOST
        self.db_port = 3306
        self.db_user = 'admin'
        self.db_password = DB_PASSWORD
        self.db_database = 'cloudpriceloggingdb'

        self.save = self.save_index_to_db(time, price)

    def save_index_to_db(self, epoch_nano, price):
        self.create_db()
        engine = create_engine(f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}")
        df = pd.DataFrame({
            'epoch_nanos': [epoch_nano],  # wrap in a list
            'price': [price]               # wrap in a list
        })
        df.to_sql(self.index_name_db, con=engine, if_exists='append', index=False)

    def create_db(self):
        connection = pymysql.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            database=self.db_database
        )
        mycur = connection.cursor()
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{self.index_name_db}` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `epoch_nanos` INT,
            `price` FLOAT,
            PRIMARY KEY (`id`)
        ) ENGINE=INNODB;
        """
        mycur.execute(create_table_query)
        connection.commit()