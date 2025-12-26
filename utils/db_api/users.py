from utils.db_api.create_tables import Database


class UsersDB:
    def __init__(self, db: Database):
        self.db = db
        
    async def add_user(self, telegram_id):
        sql = "INSERT INTO users (telegram_id) VALUES ($1) ON CONFLICT (telegram_id) DO NOTHING"
        await self.db.execute(sql, telegram_id)

    async def select_all_users(self):
        sql = "SELECT telegram_id FROM users "
        return await self.db.fetch(sql)

    async def select_users_offset(self, offset: int = 0, limit: int = 1000):
        sql = "SELECT telegram_id FROM users ORDER BY id LIMIT $1 OFFSET $2"
        return await self.db.fetch(sql, limit, offset)

    async def count_users(self):
        sql = "SELECT COUNT(id) FROM users"
        return await self.db.fetchval(sql)

    async def delete_user(self, telegram_id):
        sql = "DELETE FROM users WHERE telegram_id = $1"
        return await self.db.execute(sql, telegram_id)
