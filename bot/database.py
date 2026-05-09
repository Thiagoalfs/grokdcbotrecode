import aiomysql
import os

class Database:
    def __init__(self):
        self.pool = None

    async def setup(self):
        """Inicializa o pool de conexões com o MySQL usando variáveis de ambiente."""
        try:
            host = os.getenv("DB_HOST")
            print(f"DEBUG: Tentando conectar ao host: {host}")
            
            self.pool = await aiomysql.create_pool(
                host=host,
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                db=os.getenv("DB_NAME"),
                autocommit=True, # Salva alterações automaticamente
                cursorclass=aiomysql.DictCursor, # Retorna resultados como dicionários (ex: row['nome'])
                minsize=1,
                maxsize=5, # Limita o pool para não exceder o limite do servidor (5 conexões)
                pool_recycle=300 # Recicla conexões a cada 5 minutos para evitar o timeout da Clever Cloud
            )
            print("✅ Conexão com o banco de dados MySQL estabelecida!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco de dados: {e}")
            raise e

    async def create_tables(self):
        """Cria a tabela de configurações caso não exista."""
        await self.execute("""
            CREATE TABLE IF NOT EXISTS botsettings (
                guild_id BIGINT PRIMARY KEY,
                serverprefix VARCHAR(5) DEFAULT '.',
                language VARCHAR(5) DEFAULT 'EN'
            )
        """)

        # Tabela de League of Legends (Global)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS leagueconfig (
                user_id BIGINT PRIMARY KEY,
                riot_id VARCHAR(100) NOT NULL
            )
        """)

    async def execute(self, query, params=None):
        """Executa comandos como INSERT, UPDATE, DELETE."""
        for attempt in range(2):
            try:
                async with self.pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(query, params or ())
                        return cur.rowcount
            except aiomysql.OperationalError as e:
                # Erros 2006 (Gone away) ou 2013 (Lost connection)
                if attempt == 0 and e.args[0] in (2006, 2013):
                    continue
                raise e

    async def fetch(self, query, params=None):
        """Busca múltiplos registros (SELECT)."""
        for attempt in range(2):
            try:
                async with self.pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(query, params or ())
                        return await cur.fetchall()
            except aiomysql.OperationalError as e:
                if attempt == 0 and e.args[0] in (2006, 2013):
                    continue
                raise e

    async def fetch_one(self, query, params=None):
        """Busca um único registro."""
        for attempt in range(2):
            try:
                async with self.pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(query, params or ())
                        return await cur.fetchone()
            except aiomysql.OperationalError as e:
                if attempt == 0 and e.args[0] in (2006, 2013):
                    continue
                raise e