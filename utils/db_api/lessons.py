from utils.db_api.create_tables import Database


class LessonsDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_category(self, category_name: str) -> int:
        category_id = await self.db.fetchval(
            """
            INSERT INTO categories (name)
            VALUES ($1)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
            """,
            category_name
        )

        if category_id:
            return category_id

        return await self.db.fetchval(
            "SELECT id FROM categories WHERE name = $1",
            category_name
        )

    async def add_subcategory(self, category_id: int, subcategory_name: str) -> int:
        sql = """
            INSERT INTO subcategories (category_id, name)
            VALUES ($1, $2)
            ON CONFLICT (category_id, name)
            DO UPDATE SET name = EXCLUDED.name
            RETURNING id
        """
        return await self.db.fetchval(sql, category_id, subcategory_name)

    async def add_lessons(self, subcategory_id):
        sql = """
            INSERT INTO lessons (subcategory_id) VALUES ($1) RETURNING id    
            """
        return await self.db.fetchval(sql, subcategory_id)

    async def add_lesson_files(self, lesson_number, lesson_id, file_id, file_type, caption):
        sql = """
            INSERT INTO lesson_files (lesson_number, lesson_id, file_id, file_type, caption) VALUES ($1, $2, $3, $4, $5)
            """
        await self.db.execute(sql, lesson_number, lesson_id, file_id, file_type, caption)

    async def get_free_categories(self):
        sql = """
            SELECT DISTINCT
                c.id,
                c.name
            FROM categories c
            JOIN subcategories s ON s.category_id = c.id
            JOIN lessons l ON l.subcategory_id = s.id
            WHERE l.is_paid = FALSE
            ORDER BY c.name
        """
        return await self.db.fetch(sql)


    async def get_lessons_categories(self):
        sql = """
            SELECT DISTINCT id, name FROM categories ORDER BY id
        """
        return await self.db.fetch(sql)

    async def set_category_name(self, name, category_id):
        sql = """
            UPDATE categories SET name = $1 WHERE id = $2
            """
        await self.db.execute(sql, name, category_id)

    async def get_free_lessons(self, subcategory_id: int):
        sql = """
            SELECT 
                lf.id AS lesson_id,
                lf.lesson_number,
                lf.caption,
                lf.lesson_id AS ls_id
            FROM lessons l
            JOIN lesson_files lf ON lf.lesson_id = l.id
            WHERE l.subcategory_id = $1
              AND l.is_paid = FALSE
            ORDER BY lf.lesson_number, lf.id
        """
        return await self.db.fetch(sql, subcategory_id)

    async def get_subcategories(self, category_id):
        sql = """
            SELECT DISTINCT ON (name) name, id FROM subcategories WHERE category_id = $1
            """
        return await self.db.fetch(sql, category_id)

    async def get_related_subcategories(self, subcategory_id: int):
        sql = """
            SELECT
                id,
                category_id,
                name                
            FROM subcategories
            WHERE category_id = (
                SELECT category_id
                FROM subcategories
                WHERE id = $1
            )
            ORDER BY name
        """
        return await self.db.fetch(sql, subcategory_id)

    async def get_lesson_by_lesson_id(self, lesson_id):
        sql = """
            SELECT l.subcategory_id, lf.file_type, file_id, caption FROM lesson_files lf 
            JOIN lessons l ON lf.lesson_id = l.id            
            WHERE lf.id = $1
            """
        return await self.db.fetch(sql, lesson_id)

    async def lesson_file_exists(
            self,
            lesson_file_id: int,
            subcategory_id: int
    ) -> bool:
        sql = """
            SELECT EXISTS (
                SELECT 1
                FROM lesson_files lf
                JOIN lessons l ON l.id = lf.lesson_id
                WHERE lf.id = $1
                  AND l.subcategory_id = $2
            )
        """
        return await self.db.fetchval(sql, lesson_file_id, subcategory_id)

    async def check_category(self, category_id: int) -> bool:
        sql = """
            SELECT EXISTS (SELECT 1 FROM categories WHERE id = $1) 
            """
        return await self.db.fetchval(sql, category_id)

    async def check_subcategory(self, category_id: int, subcategory_id: int) -> bool:
        sql = """
            SELECT EXISTS (SELECT 1 FROM subcategories WHERE category_id = $1 AND id = $2) 
            """
        return await self.db.fetchval(sql, category_id, subcategory_id)

    async def set_free_lesson(self, file_id, file_type, caption, lesson_number, lesson_id):
        sql = """
            UPDATE lesson_files SET file_id = $1, file_type = $2, caption = $3, lesson_number = $4 WHERE id = $5
            """
        await self.db.execute(sql, file_id, file_type, caption, lesson_number, lesson_id)

    async def set_subcategory_name(self, subcategory_name, subcategory_id):
        sql = """
            UPDATE subcategories SET name = $1 WHERE id = $2
            """
        await self.db.execute(sql, subcategory_name, subcategory_id)

    async def delete_category(self, category_id):
        sql = """
            DELETE FROM categories WHERE id = $1
            """
        await self.db.execute(sql, category_id)

    async def delete_subcategory(self, subcategory_id):
        sql = """
            DELETE FROM subcategories WHERE id = $1
            """
        await self.db.execute(sql, subcategory_id)

    async def delete_lesson(self, lesson_id):
        sql = """
            DELETE FROM lessons WHERE id = $1
            """
        await self.db.execute(sql, lesson_id)
