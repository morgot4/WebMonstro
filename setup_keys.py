# import pandas as pd
# import sqlalchemy
# from sqlalchemy import create_engine, text
# import time
# import os


# # Настройки подключения
# username = "gen_user"
# password = "wuosy4z8t4"
# host = "109.68.213.209"
# port = "5432"
# database = "default_db"
# table_name = "keys" 

# # Создаем подключение
# conn_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
# engine = create_engine(conn_string)

# # Названия колонок в таблице
# col1_name = "text"  # замените на имя первой колонки в вашей таблице
# col2_name = "frequency"  # замените на имя второй колонки в вашей таблице
# fraction = 1 / 7

# # Параметры загрузки
# filepath = 'C:\\Users\\Administrator\\Downloads\\keywords225.tsv'  # путь к вашему TSV файлу
# chunksize = 50000 # размер чанка (можно уменьшить при проблемах с памятью)

# file_size = os.path.getsize(filepath)
# estimated_total_rows = file_size / 100  # очень грубая оценка: предполагаем ~100 байт на строку
# max_rows_to_process = int(estimated_total_rows * fraction)

# # Функция для прямой вставки через SQL
# def insert_chunk(conn, df, table):
#     # Создаем временную таблицу в памяти
#     temp_table = f"temp_{table}"
#     df.to_sql(temp_table, conn, if_exists='replace', index=False)
    
#     # Вставляем данные из временной таблицы в целевую таблицу
    
#     conn.execute(text(f"""
#     INSERT INTO {table} ({col1_name}, {col2_name})
#     SELECT "0", "1" FROM {temp_table}
#     ON CONFLICT DO NOTHING
#     """))
#     conn.execute(text(f"DROP TABLE {temp_table}"))

# # Основной процесс загрузки
# total_rows = 0
# start_time = time.time()

# try:
#     with engine.connect() as conn:
#         # Создаем таблицу, если она не существует
#         conn.execute(text(f"""
#         CREATE TABLE IF NOT EXISTS {table_name} (
#             {col1_name} TEXT,
#             {col2_name} BIGINT
#         )
#         """))
        
#         # Читаем и загружаем данные чанками
#         for i, chunk in enumerate(pd.read_csv(filepath, sep='\t', header=None, 
#                                              chunksize=chunksize, quoting=3, 
#                                              dtype={0: str, 1: 'Int64'})):
#             # Очищаем данные
#             chunk = chunk.fillna('')
#             chunk[1] = pd.to_numeric(chunk[1], errors='coerce').fillna(0).astype('Int64')
            
#             # Выводим первый чанк для отладки
#             if i == 0:
#                 print("Первые 5 строк из файла:")
#                 print(chunk.head())
            
#             # Вставляем данные
#             insert_chunk(conn, chunk, table_name)
            
#             # Обновляем счетчик и выводим статус
#             total_rows += len(chunk)
#             elapsed = time.time() - start_time
#             print(f"Загружено {total_rows:,} строк за {elapsed:.1f} секунд. "
#                   f"Скорость: {total_rows/elapsed:.1f} строк/сек")
#             conn.commit()
#             # Останавливаемся, когда достигнем заданной доли данных
#             if total_rows >= max_rows_to_process:
#                 #print(f"Достигнут лимит в {fraction:.0%} от оценочного объема данных")
#                 break
            
# except Exception as e:
#     print(f"Ошибка: {e}")
#     import traceback
#     traceback.print_exc()
# finally:
#     pass
#     print(f"Всего загружено {total_rows:,} строк за {time.time() - start_time:.1f} секунд")
#     print(f"Приблизительно {total_rows / estimated_total_rows:.1%} от общего объема файла")



import time
import pandas as pd
from clickhouse_driver import Client
from tqdm import tqdm
import os

def load_to_clickhouse(file_path, host, user, password, 
                      batch_size=50000, max_retries=3, fraction=1 / 7):
    """Загрузка части файла в ClickHouse"""
    
    # Подключение к ClickHouse
    client = Client(
        host=host,
        port=9440,
        user=user,
        password=password,
        secure=True
    )
    
    # Подсчет общего количества строк
    total_lines = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
    max_rows = int(total_lines * fraction)
    
    print(f"Всего строк: {total_lines:,}")
    print(f"Загружаем {max_rows:,} строк ({fraction*100:.1f}%)")
    
    # Инициализация таймера и счетчиков
    start_time = time.time()
    last_log_time = start_time
    rows_loaded = 0
    
    try:
        # Прогресс-бар
        with tqdm(total=max_rows, unit='rows', desc='Загрузка') as progress:
            for chunk in pd.read_csv(
                file_path,
                sep='\t',
                header=None,
                names=['text', 'frequency'],
                dtype={'text': str, 'frequency': 'Int64'},
                chunksize=batch_size,
                encoding='utf-8'
            ):
                # Очистка данных
                chunk = chunk.dropna(subset=['text'])
                chunk['text'] = chunk['text'].str.strip()
                chunk['frequency'] = pd.to_numeric(
                    chunk['frequency'], errors='coerce'
                ).fillna(0).astype('int64')
                
                # Обрезаем чанк если достигли лимита
                remaining = max_rows - rows_loaded
                if remaining <= 0:
                    break
                if len(chunk) > remaining:
                    chunk = chunk.iloc[:remaining]
                
                # Вставка с повторами при ошибках
                for attempt in range(max_retries):
                    try:
                        client.execute(
                            "INSERT INTO keywords (text, frequency) VALUES",
                            chunk.to_dict('records')
                        )
                        break
                    except Exception as e:
                        if attempt == max_retries - 1:
                            raise
                        time.sleep(2 ** attempt)
                
                # Обновление прогресса
                rows_loaded += len(chunk)
                progress.update(len(chunk))
                
                # Логирование каждые N строк
                current_time = time.time()
                if current_time - last_log_time > 30:  # Каждые 30 секунд
                    elapsed = current_time - start_time
                    speed = rows_loaded / elapsed if elapsed > 0 else 0
                    print(
                        f"\nЗагружено: {rows_loaded:,}/{max_rows:,} "
                        f"({rows_loaded/max_rows:.1%}) | "
                        f"Скорость: {speed:.0f} строк/сек"
                    )
                    last_log_time = current_time
    
    finally:
        client.disconnect()
        total_time = time.time() - start_time
        print(
            f"\nИтог: {rows_loaded:,} строк за {total_time:.1f} сек "
            f"({rows_loaded/total_time:.0f} строк/сек)"
        )

# Пример использования
load_to_clickhouse(
    file_path='C:\\Users\\Fedor\\Desktop\\keywords225\\keywords225.tsv',
    host='gm0pw0r5n1.westus3.azure.clickhouse.cloud',
    user='default',
    password='V_YqSv9ERe3Ac',
    fraction=1/7
)


