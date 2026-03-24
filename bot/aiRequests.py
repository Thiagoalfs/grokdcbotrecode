import time
from variables import groq_client, ultimo_uso_groq, cooldown_groq

async def perguntar_groq(pergunta, option):
    global ultimo_uso_groq
    agora = time.time()
    tempo_restante = cooldown_groq - (agora - ultimo_uso_groq)
    if agora - ultimo_uso_groq < cooldown_groq:
        return f"calma aí fi, se mandar mta coisa a api n deixa. **tempo restante: _{round(tempo_restante)}_ segundos**"
    
    ultimo_uso_groq = agora

    if option == "imagem":
        try:
            resposta = groq_client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": "Você é Gork, um bot de discord que fala de maneira coloquial e com algumas girias/expressões. Explique essa imagem em forma de resumo de no máximo 4 linhas. Procure o contexto e tente explicar trazendo informações de fora que fazem sentido com o prompt."},
                    {"role": "user","content": [{"type": "image_url", "image_url": {"url": pergunta}}]}
                ]
            )
            return resposta.choices[0].message.content
        except Exception as e:
            erro = str(e).lower()
            if "rate_limit" in erro or "quota" in erro or "tokens" in erro or "429" in erro:
                return f"erro: {e}"

    else:
        MODELOS = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
        messages = [
            {"role": "system", "content": "Você é grok, um bot de discord. responda as perguntas de forma simples, com algumas gírias/expressões, resumida e rápida, mas garantindo o entendimento da resposta. sem emojis nem nada"},
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