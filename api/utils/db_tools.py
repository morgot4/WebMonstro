


async def populate_random_seeds(self, total_entries_count):
        """
        Заполнение таблицы случайных сидов
        
        :param total_entries_count: Общее количество записей в основной таблице
        """
        async with self.async_session() as session:
            # Очистка существующих сидов
            await session.execute('TRUNCATE TABLE random_seeds')
            
            # Генерация случайных сидов
            seeds = [
                RandomSeed(id=i, random_seed=random.randint(1, 1000000)) 
                for i in range(1, total_entries_count + 1001)  # Добавляем запас
            ]
            
            session.add_all(seeds)
            await session.commit()