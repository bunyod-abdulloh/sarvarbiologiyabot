from utils.db_api.create_tables import Database


class LessonsDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_lesson(self, type_, file_id, caption):
        sql = """
            INSERT INTO lessons (type, file_id, caption) VALUES ($1, $2, $3)
            """
        await self.db.execute(sql, type_, file_id, caption, execute=True)

    async def get_free_lessons_by_category(self):
        sql = """
            SELECT DISTINCT ON (category_name)
                   category_name, category_id
            FROM lessons
            WHERE paid = FALSE
            ORDER BY category_name, category_id
            """
        return await self.db.execute(sql, fetch=True)

    async def get_lessons_by_category_id(self, category_id):
        sql = """
            SELECT id, position, type, file_id, caption FROM lessons WHERE category_id = $1 
            """
        return await self.db.execute(sql, category_id, fetch=True)

    async def get_lesson_free(self):
        sql = """
            SELECT id, position, type, file_id, caption FROM lessons WHERE paid = FALSE
            """
        return await self.db.execute(sql, fetch=True)

    async def get_lesson_by_position(self, position):
        sql = """
            SELECT id, position, type, file_id, caption FROM lessons WHERE position = $1
            """
        return await self.db.execute(sql, position, fetchrow=True)
