from pymongo import MongoClient

# Configura la URL de conexión a MongoDB
MONGO_URI = "mongodb://localhost:27017/Actas_Arintia"

# Crea una instancia del cliente de MongoDB
client = MongoClient(MONGO_URI)

# Selecciona la base de datos
db = client.get_database()
