from typing import Optional

import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Optional[Pool] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            min_size=1,
            max_size=10
        )

    # =======================
    # QUERY METHODS
    # =======================
    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    # =======================
    # CREATE TABLES
    # =======================
    async def create_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS subcategories (
            id SERIAL PRIMARY KEY,
            category_id INTEGER NOT NULL
                REFERENCES categories(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            UNIQUE (category_id, name)
        );

        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            is_paid BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS send_table (
            id SERIAL PRIMARY KEY,
            status BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS lessons (
            id SERIAL PRIMARY KEY,
            subcategory_id INTEGER NOT NULL
                REFERENCES subcategories(id) ON DELETE CASCADE,
            is_paid BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS lesson_files (
            id SERIAL PRIMARY KEY,
            lesson_id INTEGER NOT NULL
                REFERENCES lessons(id) ON DELETE CASCADE,
            lesson_number VARCHAR(50),
            file_id TEXT NOT NULL,
            file_type VARCHAR(20) NOT NULL,
            caption TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS paid_access (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL
                REFERENCES users(id) ON DELETE CASCADE,
            category_id INTEGER NOT NULL
                REFERENCES categories(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT NOW(),
            UNIQUE (user_id, category_id)
        );

        CREATE INDEX IF NOT EXISTS idx_subcategories_category_id
            ON subcategories(category_id);

        CREATE INDEX IF NOT EXISTS idx_lessons_subcategory_id
            ON lessons(subcategory_id);

        CREATE INDEX IF NOT EXISTS idx_lessons_is_paid
            ON lessons(is_paid);

        CREATE INDEX IF NOT EXISTS idx_paid_access_user
            ON paid_access(user_id);
        """

        async with self.pool.acquire() as conn:
            await conn.execute(sql)
