from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.admins import AdminsDB
from utils.db_api.create_tables import Database
from utils.db_api.lessons import LessonsDB
from utils.db_api.paid_lessons import PaidLessonsDB
from utils.db_api.users import UsersDB

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# storage = RedisStorage2(
#     host='localhost',
#     port=6379,
#     db=5,
#     state_ttl=3600,
#     data_ttl=3600,
#     password=REDIS_PASS
# )
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
udb = UsersDB(db)
admdb = AdminsDB(db)
pdb = PaidLessonsDB(db)
lesdb = LessonsDB(db)
