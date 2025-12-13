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
                CREATE TABLE IF NOT EXISTS paid_users (
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
                category_name VARCHAR(255) NULL,
                category_id INTEGER NULL,
                position INTEGER,
                type VARCHAR(255),
                file_id VARCHAR(300),
                caption VARCHAR(4000)
            );
            """,

            # sequence
            """
            CREATE SEQUENCE IF NOT EXISTS lessons_position_seq START 1;
            """,

            # trigger function
            """
            CREATE OR REPLACE FUNCTION lessons_set_position()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.position IS NULL THEN
                    NEW.position := nextval('lessons_position_seq');
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """,

            # trigger
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_trigger WHERE tgname = 'trg_lessons_set_position'
                ) THEN
                    CREATE TRIGGER trg_lessons_set_position
                    BEFORE INSERT ON lessons
                    FOR EACH ROW
                    EXECUTE FUNCTION lessons_set_position();
                END IF;
            END;
            $$;
            """
        ]

        for query in queries:
            await self.execute(query, execute=True)
