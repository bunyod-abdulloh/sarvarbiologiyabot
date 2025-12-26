from utils.db_api.create_tables import Database


class AdminsDB:
    def __init__(self, db: Database):
        self.db = db
        
    async def add_send_status(self):
        sql = "INSERT INTO send_table (status) VALUES (FALSE)"
        await self.db.execute(sql)

    async def update_status_true(self):
        sql = "UPDATE send_table SET status = TRUE"
        await self.db.execute(sql)

    async def update_status_false(self):
        sql = "UPDATE send_table SET status = FALSE"
        await self.db.execute(sql)

    async def get_send_status(self):
        sql = "SELECT status FROM send_table"
        return await self.db.fetchval(sql)
