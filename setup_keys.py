import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text
import time
import sys



# Настройки подключения


# Создаем подключение
conn_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(conn_string)

# Названия колонок в таблице
col1_name = "text"  # замените на имя первой колонки в вашей таблице
col2_name = "frequency"  # замените на имя второй колонки в вашей таблице

# Параметры загрузки
filepath = 'C:\\Users\\Administrator\\Downloads\\keywords225.tsv'  # путь к вашему TSV файлу
chunksize = 50000  # размер чанка (можно уменьшить при проблемах с памятью)

# Функция для прямой вставки через SQL
def insert_chunk(conn, df, table):
    # Создаем временную таблицу в памяти
    temp_table = f"temp_{table}"
    df.to_sql(temp_table, conn, if_exists='replace', index=False)
    
    # Вставляем данные из временной таблицы в целевую таблицу
    with conn.begin():
        conn.execute(text(f"""
        INSERT INTO {table} ({col1_name}, {col2_name})
        SELECT "0", "1" FROM {temp_table}
        ON CONFLICT DO NOTHING
        """))
        conn.execute(text(f"DROP TABLE {temp_table}"))

# Основной процесс загрузки
total_rows = 0
start_time = time.time()

try:
    with engine.connect() as conn:
        # Создаем таблицу, если она не существует
        conn.execute(text(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {col1_name} TEXT PRIMARY KEY,
            {col2_name} BIGINT
        )
        """))
        
        # Читаем и загружаем данные чанками
        for i, chunk in enumerate(pd.read_csv(filepath, sep='\t', header=None, 
                                             chunksize=chunksize, quoting=3, 
                                             dtype={0: str, 1: 'Int64'})):
            # Очищаем данные
            chunk = chunk.fillna('')  # Заменяем NaN на пустые строки
            chunk[1] = pd.to_numeric(chunk[1], errors='coerce').fillna(0).astype('Int64')
            
            # Выводим первый чанк для отладки
            if i == 0:
                print("Первые 5 строк из файла:")
                print(chunk.head())
            
            # Вставляем данные
            insert_chunk(conn, chunk, table_name)
            
            # Обновляем счетчик и выводим статус
            total_rows += len(chunk)
            elapsed = time.time() - start_time
            print(f"Загружено {total_rows:,} строк за {elapsed:.1f} секунд. "
                  f"Скорость: {total_rows/elapsed:.1f} строк/сек")
            
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()
finally:
    print(f"Всего загружено {total_rows:,} строк за {time.time() - start_time:.1f} секунд")