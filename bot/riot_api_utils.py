import aiohttp
import os

async def fetch_riot_api(url):
    """Faz requisições assíncronas para a Riot API usando a chave de ambiente."""
    api_key = os.getenv("RIOT_API_KEY")
    if not api_key:
        print("❌ RIOT_API_KEY não encontrada no .env")
        return None

    headers = {"X-Riot-Token": api_key}
    # Timeout curto para evitar que o bot trave se a Riot demorar
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            
            print(f"⚠️ Erro na Riot API: {resp.status} - URL: {url}")
            return None