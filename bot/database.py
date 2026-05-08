import aiomysql
import os

class Database:
    def __init__(self):
        self.pool = None

    async def setup(self):
        """Inicializa o pool de conexões com o MySQL usando variáveis de ambiente."""
        self.pool = await aiomysql.create_pool(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            db=os.getenv("DB_NAME"),
            autocommit=True, # Salva alterações automaticamente
            cursorclass=aiomysql.DictCursor # Retorna resultados como dicionários (ex: row['nome'])
        )
        print("✅ Conexão com o banco de dados MySQL estabelecida!")

    async def create_tables(self):
        """Cria a tabela de configurações caso não exista."""
        await self.execute("""
            CREATE TABLE IF NOT EXISTS botsettings (
                guild_id BIGINT PRIMARY KEY,
                serverprefix VARCHAR(5) DEFAULT '.'
            )
        """)

    async def execute(self, query, params=None):
        """Executa comandos como INSERT, UPDATE, DELETE."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or ())
                return cur.rowcount

    async def fetch(self, query, params=None):
        """Busca múltiplos registros (SELECT)."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or ())
                return await cur.fetchall()

    async def fetch_one(self, query, params=None):
        """Busca um único registro."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or ())
                return await cur.fetchone()