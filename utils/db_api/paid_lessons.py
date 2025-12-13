from utils.db_api.create_tables import Database


class PaidLessonsDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_to_pd(self, telegram_id):
        sql = """
            INSERT INTO paid_lessons (telegram_id) VALUES ($1)
            """
        await self.db.execute(sql, telegram_id)

    async def count_users_pd(self):
        sql = """
            SELECT COUNT(id) FROM paid_lessons
            """
        return self.db.execute(sql, fetchval=True)

    async def delete_from_pd(self, telegram_id):
        sql = """
            DELETE FROM paid_lessons WHERE telegram_id = $1
            """
        await self.db.execute(sql, telegram_id, execute=True)
