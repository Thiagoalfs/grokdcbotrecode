from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

botToken = os.getenv("TOKEN")
groq_client = Groq(api_key=os.getenv("GROQ_API"))
gif_atual = 0