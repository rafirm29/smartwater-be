import motor.motor_asyncio
from pymongo.collection import Collection
from models.user import User

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client['smartwater-db']
collection: Collection[User] = db['user']
