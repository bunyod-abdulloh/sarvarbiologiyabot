from aiogram import Dispatcher

from loader import dp
from .is_subscribed_middleware import SubscriptionMiddleware
from .media_group import AlbumMiddleware

from .throttling import ThrottlingMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(AlbumMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SubscriptionMiddleware())

