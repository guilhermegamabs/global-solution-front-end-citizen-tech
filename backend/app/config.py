import os

from dotenv import load_dotenv

load_dotenv()


def obterChaveGemini():
    return os.getenv("GEMINIAPIKEY", "")


def obterModeloGemini():
    return os.getenv("GEMINIMODEL", "gemini-2.5-flash")


def obterOrigensPermitidas():
    bruto = os.getenv("ALLOWEDORIGINS", "http://localhost:8501")
    return [origem.strip() for origem in bruto.split(",") if origem.strip()]


def obterTempoLimite():
    return float(os.getenv("REQUESTTIMEOUT", "30"))
