from utils.db_api.create_tables import Database


class LessonsDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_to_free_lessons(self, category_id):
        row_id = await self.db.execute(
            """
            INSERT INTO free_lessons (category_id)
            VALUES ($1)            
            RETURNING id
            """,
            category_id,
            fetchval=True
        )

        if row_id:
            return row_id

        return await self.db.execute(
            "SELECT id FROM free_lessons WHERE category_id = $1",
            category_id,
            fetchval=True
        )

    async def add_to_free_lessons_files(self, lesson_number, lesson_id, file_id, file_type, caption):
        sql = """
            INSERT INTO free_lessons_files (lesson_number, lesson_id, file_id, file_type, caption) VALUES ($1, $2, $3, $4, $5)
            """
        await self.db.execute(sql, lesson_number, lesson_id, file_id, file_type, caption, execute=True)

    async def get_free_lessons_by_category(self):
        sql = """
            SELECT DISTINCT
                c.id,
                c.name
            FROM categories c
            JOIN free_lessons f
                ON f.category_id = c.id
            JOIN free_lessons_files ff
                ON ff.lesson_id = f.id
            ORDER BY c.name
        """
        return await self.db.execute(sql, fetch=True)

    async def get_lessons_categories(self):
        sql = """
            SELECT DISTINCT id, name FROM categories ORDER BY name
        """
        return await self.db.execute(sql, fetch=True)


    async def get_paid_lessons_by_category(self):
        sql = """
            SELECT DISTINCT
                c.id,
                c.name
            FROM categories c
            JOIN paid_lessons f
                ON f.category_id = c.id
            JOIN paid_lessons_files ff
                ON ff.lesson_id = f.id
            ORDER BY c.name
        """
        return await self.db.execute(sql, fetch=True)

    async def get_lessons_by_category_id(self, category_id):
        sql = """
            SELECT
                ROW_NUMBER() OVER (ORDER BY f.created_at) AS row_number,
                f.id        AS file_row_id,
                f.lesson_number,
                f.lesson_id,
                f.file_id,
                f.file_type,
                f.caption,
                f.created_at
            FROM (
                SELECT DISTINCT ON (f.lesson_number)
                    f.*
                FROM free_lessons_files f
                JOIN free_lessons l ON l.id = f.lesson_id
                WHERE l.category_id = $1
                ORDER BY f.lesson_number, f.created_at
            ) f
            ORDER BY f.created_at 
            """
        return await self.db.execute(sql, category_id, fetch=True)

    async def get_lessons_paid_by_category_id(self, category_id):
        sql = """
            SELECT
                ROW_NUMBER() OVER (ORDER BY f.created_at) AS row_number,
                f.id        AS file_row_id,
                f.lesson_number,
                f.lesson_id,
                f.file_id,
                f.file_type,
                f.caption,
                f.created_at
            FROM (
                SELECT DISTINCT ON (f.lesson_id)
                    f.*
                FROM paid_lessons_files f
                JOIN paid_lessons l ON l.id = f.lesson_id
                WHERE l.category_id = $1
                ORDER BY f.lesson_id, f.created_at
            ) f
            ORDER BY f.created_at 
            """
        return await self.db.execute(sql, category_id, fetch=True)

    async def get_lesson_free(self):
        sql = """
            SELECT id, position, type, file_id, caption FROM lessons WHERE paid = FALSE
            """
        return await self.db.execute(sql, fetch=True)

    async def get_lesson_by_lesson_id(self, lesson_id):
        sql = """
            SELECT file_type, file_id, caption FROM free_lessons_files WHERE lesson_id = $1
            """
        return await self.db.execute(sql, lesson_id, fetch=True)

    async def get_paid_lesson(self, lesson_id):
        sql = """
            SELECT file_type, file_id, caption FROM paid_lessons_files WHERE lesson_id = $1
            """
        return await self.db.execute(sql, lesson_id, fetch=True)

    async def get_lesson_category_id_by_lesson_id(self, lesson_id):
        sql = """
            SELECT category_id FROM free_lessons WHERE id = $1
            """
        return await self.db.execute(sql, lesson_id, fetchval=True)

    async def get_paid_categories(self, lesson_id):
        sql = """
            SELECT category_id FROM paid_lessons WHERE id = $1
            """
        return await self.db.execute(sql, lesson_id, fetchval=True)
