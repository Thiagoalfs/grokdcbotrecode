import time
from variables import groq_client

ultimo_uso = 0
cooldown = 10

async def perguntar_groq(pergunta, option):
    global ultimo_uso
    agora = time.time()
    tempo_restante = cooldown - (agora - ultimo_uso)
    if agora - ultimo_uso < cooldown:
        return f"calma aí fi, se mandar mta coisa a api n deixa. **tempo restante: _{round(tempo_restante)}_ segundos**"
    
    ultimo_uso = agora

    if option == "imagem":
        try:
            resposta = groq_client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": pergunta}},
                        {"type": "text", "text": "Explique essa imagem em forma de resumo. caso for de algum jogo, fale o jogo que ela é; caso seja uma série, fale de qual série é e por aí vai."}
                    ]
                }]
            )
            return resposta.choices[0].message.content
        except Exception as e:
            erro = str(e).lower()
            if "rate_limit" in erro or "quota" in erro or "tokens" in erro or "429" in erro:
                return f"erro: {e}"

    else:
        MODELOS = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
        messages = [
            {"role": "system", "content": "Imagine que você é um usuário de discord. responda as perguntas de forma simples, resumida e rápida, mas garantindo o entendimento da resposta"},
            {"role": "user", "content": pergunta}
        ]
        for modelo in MODELOS:
            try:
                resposta = groq_client.chat.completions.create(
                    messages=messages,
                    model=modelo
                )
                return resposta.choices[0].message.content
            except Exception as e:
                erro = str(e).lower()
                if "rate_limit" in erro or "quota" in erro or "tokens" in erro or "429" in erro:
                    continue
                else:
                    return f"erro: {e}"

        return "todos os modelos tão no limite, tenta mais tarde fi"