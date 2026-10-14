import requests
import time
import datetime

# 🔑 Credenciais do seu Supabase
SUPABASE_URL = "https://sonjvqvaithtpzrqbolf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvbmp2cXZhaXRodHB6cnFib2xmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE3MzI0NzQsImV4cCI6MjEwNzMwODQ3NH0.U30fYDFbG418bDzY7ampcy30ZiVun7DBr4T7FjKchPg"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

payload = {
    "id": int(time.time() * 1000),
    "nome_operador": "Analista SOC",
    "data_nascimento": "Automático",
    "termo_pesquisado": "ransomware zero-day mitigation",
    "data_hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

response = requests.post(f"{SUPABASE_URL}/rest/v1/historico_pesquisas", headers=headers, json=payload)

if response.status_code in [200, 201]:
    print("Registo inserido com sucesso!")
else:
    print(f"Erro ao inserir: {response.text}")
