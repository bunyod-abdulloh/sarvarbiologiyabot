from utils.db_api.create_tables import Database


class PaidLessonsDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_to_categories(self, category_name: str) -> int:
        row_id = await self.db.execute(
            """
            INSERT INTO categories (name)
            VALUES ($1)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
            """,
            category_name,
            fetchval=True
        )

        if row_id:
            return row_id

        return await self.db.execute(
            "SELECT id FROM categories WHERE name = $1",
            category_name,
            fetchval=True
        )

    async def add_to_paid_lessons(self, category_id):
        row_id = await self.db.execute(
            """
            INSERT INTO paid_lessons (category_id)
            VALUES ($1)            
            RETURNING id
            """,
            category_id,
            fetchval=True
        )

        if row_id:
            return row_id

        return await self.db.execute(
            "SELECT id FROM paid_lessons WHERE category_id = $1",
            category_id,
            fetchval=True
        )

    async def add_to_pd_lessons_files(self, lesson_id, file_id, file_type, caption):
        sql = """
            INSERT INTO paid_lessons_files (lesson_id, file_id, file_type, caption) VALUES ($1, $2, $3, $4)
            """
        await self.db.execute(sql, lesson_id, file_id, file_type, caption, execute=True)



    async def count_users_pd(self):
        sql = """
            SELECT COUNT(id) FROM paid_lessons
            """
        return await self.db.execute(sql, fetchval=True)

    async def delete_from_pd(self, telegram_id):
        sql = """
            DELETE FROM paid_lessons WHERE telegram_id = $1
            """
        await self.db.execute(sql, telegram_id, execute=True)

    async def check_paid_user(self, telegram_id):
        sql = """
            SELECT EXISTS (SELECT 1 FROM paid_lessons WHERE telegram_id = $1)
            """
        return await self.db.execute(sql, telegram_id, fetchval=True)
