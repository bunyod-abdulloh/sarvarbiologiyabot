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
            ORDER BY c.id
        """
        return await self.db.execute(sql, fetch=True)

    async def get_lessons_categories(self):
        sql = """
            SELECT DISTINCT id, name FROM categories ORDER BY name
        """
        return await self.db.execute(sql, fetch=True)

    async def get_categories(self):
        sql = """
            SELECT id, name FROM categories ORDER BY id ASC
            """
        return await self.db.execute(sql, fetch=True)

    async def set_category_name(self, name, category_id):
        sql = """
            UPDATE categories SET name = $1 WHERE id = $2
            """
        await self.db.execute(sql, name, category_id, execute=True)


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
            ORDER BY c.id
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

    async def check_free_lesson(self, lesson_id):
        sql = """
            SELECT EXISTS (SELECT 1 FROM free_lessons_files ff WHERE ff.id = $1)
            """
        return await self.db.execute(sql, lesson_id, fetchval=True)

    async def check_paid_lesson_category_exists(self, paid_file_id: int, category_id: int) -> bool:
        sql = """
            SELECT EXISTS (
                SELECT 1
                FROM paid_lessons_files plf
                JOIN paid_lessons pl ON pl.id = plf.lesson_id
                JOIN categories c ON c.id = pl.category_id
                WHERE plf.id = $1 AND c.id = $2 
            )
        """
        return await self.db.execute(sql, paid_file_id, category_id, fetchval=True)

    async def check_free_lesson_category_exists(self, paid_file_id: int, category_id: int) -> bool:
        sql = """
            SELECT EXISTS (
                SELECT 1
                FROM free_lessons_files flf
                JOIN free_lessons fl ON fl.id = flf.lesson_id
                JOIN categories c ON c.id = fl.category_id
                WHERE flf.id = $1 AND c.id = $2 
            )
        """
        return await self.db.execute(sql, paid_file_id, category_id, fetchval=True)

    async def set_free_lesson(self, file_id, file_type, caption, lesson_number, lesson_id):
        sql = """
            UPDATE free_lessons_files SET file_id = $1, file_type = $2, caption = $3, lesson_number = $4 WHERE id = $5
            """
        await self.db.execute(sql, file_id, file_type, caption, lesson_number, lesson_id, execute=True)

    async def set_paid_lesson(self, file_id, file_type, caption, lesson_number, lesson_id):
        sql = """
            UPDATE paid_lessons_files SET file_id = $1, file_type = $2, caption = $3, lesson_number = $4 WHERE id = $5
            """
        await self.db.execute(sql, file_id, file_type, caption, lesson_number, lesson_id, execute=True)

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

    async def delete_category(self, category_id):
        sql = """
            DELETE FROM categories WHERE id = $1
            """
        await self.db.execute(sql, category_id, execute=True)

    async def delete_lesson_free(self, lesson_id):
        sql = """
            DELETE FROM free_lessons_files WHERE id = $1
            """
        await self.db.execute(sql, lesson_id, execute=True)

    async def delete_lesson_paid(self, lesson_id):
        sql = """
            DELETE FROM paid_lessons_files WHERE id = $1
            """
        await self.db.execute(sql, lesson_id, execute=True)
