import asyncpg

async def get_db_connection():
    return await asyncpg.connect(
        user="nurenai",
        password="Biz1nurenWar*",
        database="nurenpostgres",
        host="nurenaistore.postgres.database.azure.com",
        port=5432
    )
