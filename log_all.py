import gpuhunt
import pandas as pd
from enum import Enum
from logger_secrets import DB_PASSWORD, DB_HOST
from sqlalchemy import create_engine

class LogAllPrices:
    def __init__(self, time):
        self.query_time = time
        self.data = self.query_gpuhunt()

    def query_gpuhunt(self):
        items = gpuhunt.query()
        data = [
            {'instance_name': item.instance_name,
            'datetime': self.query_time,
            'location': item.location,
            'price': item.price,
            'cpu': item.cpu,
            'memory': item.memory,
            'gpu_count': item.gpu_count,
            'gpu_name': item.gpu_name,
            'gpu_memory': item.gpu_memory,
            'spot': item.spot,
            'disk_size': item.disk_size,
            'provider': item.provider,
            'gpu_vendor': item.gpu_vendor.name if isinstance(item.gpu_vendor, Enum) else item.gpu_vendor
            }
            for item in items
        ]

        return pd.DataFrame(data)

    def save_logging_to_db(self):
        host = DB_HOST
        port = 3306
        user = 'admin'
        password = DB_PASSWORD
        database = 'cloudpriceloggingdb'

        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
        self.data.to_sql('all_cloud_logging', con=engine, if_exists='append', index=False)

    def generate_gpu_index_price(self, gpu_name, gpu_count, cpu_min, cpu_max, memory_min, memory_max, removed_instances, cpu_divisor, cpu_weighting, memory_divisor, memory_weighting):
        df = self.data
        options = df[(df.gpu_name == gpu_name) & (df.gpu_count == gpu_count) & (df.cpu >= cpu_min ) & (df.cpu <= cpu_max) & (df.memory >= memory_min) & (df.cpu <= memory_max) & (~df['instance_name'].str.contains(removed_instances, case=False))]
        
        min_price_indices = options.groupby('provider')['price'].idxmin()
        df_min_price_per_provider = options.loc[min_price_indices]
        df_min_price_per_provider['cpu_adjustment'] = 1-(((df_min_price_per_provider['cpu']/cpu_divisor)-1)*cpu_weighting)
        df_min_price_per_provider['memory_adjustment'] = 1-(((df_min_price_per_provider['memory']/memory_divisor)-1)*memory_weighting)
        df_min_price_per_provider['adjusted_price'] = df_min_price_per_provider['price'] * df_min_price_per_provider['cpu_adjustment'] * df_min_price_per_provider['memory_adjustment']
        return df_min_price_per_provider.adjusted_price.mean()
