import motor.motor_asyncio
from pymongo.collection import Collection
from models.user import User
from models.pool import Pool
from models.history import History

from config.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(
    f'mongodb+srv://{settings.MONGODB_ADMIN}:{settings.MONGODB_PASSWORD}@smartwater-cluster.s5r9b9h.mongodb.net')
db = client['smartwater-db']
collection_user: Collection[User] = db['user']
collection_pool: Collection[Pool] = db['pool']
collection_history: Collection[History] = db['history']
