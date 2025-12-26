from loader import dp
from .is_subscribed_middleware import SubscriptionMiddleware

from .throttling import ThrottlingMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SubscriptionMiddleware())

