import motor.motor_asyncio
from pymongo.collection import Collection
from models.user import User
from models.pool import Pool

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client['smartwater-db']
collection_user: Collection[User] = db['user']
collection_pool: Collection[Pool] = db['pool']
