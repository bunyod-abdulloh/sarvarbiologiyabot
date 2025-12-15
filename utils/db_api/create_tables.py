from typing import Union

import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args, fetch=False, fetchval=False, fetchrow=False, execute=False):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)  # *args bilan argumentlar yuboriladi
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)  # To'g'ri uzatilgan argumentlar
        return result

    async def create_tables(self):
        queries = [
            """
                CREATE TABLE IF NOT EXISTS paid_lessons (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT NOT NULL,                    
                    created_at TIMESTAMP DEFAULT NOW()                                
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT NOT NULL UNIQUE                                                    
            );
            """,
            """
                CREATE TABLE IF NOT EXISTS admins (
                    id SERIAL PRIMARY KEY,
                    status BOOLEAN DEFAULT FALSE                                
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS lessons (
                    id SERIAL PRIMARY KEY,                    
                    paid BOOLEAN DEFAULT FALSE,
                    position INTEGER NULL,
                    type VARCHAR(255) NULL,
                    file_id VARCHAR(300) NULL,
                    caption VARCHAR(4000) NULL
                );
                
                CREATE SEQUENCE lessons_position_seq START 1;
            """
        ]
        for query in queries:
            await self.execute(query, execute=True)

    async def create_tables(self):
        queries = [
            """
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS paid_lessons (
                    id SERIAL PRIMARY KEY,
                    category_id INTEGER NOT NULL REFERENCES categories(id),                    
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS paid_lessons_files (
                    id SERIAL PRIMARY KEY,
                    lesson_id INTEGER NOT NULL REFERENCES paid_lessons(id) ON DELETE CASCADE,
                    file_id TEXT NOT NULL,
                    file_type VARCHAR(20) NOT NULL,
                    caption TEXT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS paid_users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT NOT NULL UNIQUE,                    
                    created_at TIMESTAMP DEFAULT NOW()                                
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT NOT NULL UNIQUE                                                    
            );
            """,
            """
                CREATE TABLE IF NOT EXISTS admins (
                    id SERIAL PRIMARY KEY,
                    status BOOLEAN DEFAULT FALSE                                
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS free_lessons (
                    id SERIAL PRIMARY KEY,
                    category_id INTEGER NOT NULL REFERENCES categories(id),                    
                    created_at TIMESTAMP DEFAULT NOW()
                );            
            """,
            """
                CREATE TABLE IF NOT EXISTS free_lessons_files (
                    id SERIAL PRIMARY KEY,
                    lesson_id INTEGER NOT NULL REFERENCES free_lessons(id) ON DELETE CASCADE,
                    file_id TEXT NOT NULL,
                    file_type VARCHAR(20) NOT NULL,
                    caption TEXT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """
        ]

        for query in queries:
            await self.execute(query, execute=True)
