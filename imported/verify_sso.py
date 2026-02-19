#!/usr/bin/env python3
"""
Verificação rápida da rota /sso (Pacelkin).
Correr a partir da pasta imported/ com o venv ativo:
  python verify_sso.py
"""
import sys

def main():
    print("1. A importar app.main...")
    try:
        from app.main import app, CLOSERSPACE_SSO_SECRET
    except Exception as e:
        print("   ERRO na importação:", e)
        print("   Instala dependências: pip install -r requirements.txt")
        return 1

    print("   OK")
    print("2. CLOSERSPACE_PACELKIN_SSO_SECRET está definido?", bool(CLOSERSPACE_SSO_SECRET))

    print("3. A testar GET /sso (sem token)...")
    from fastapi.testclient import TestClient
    client = TestClient(app)
    r = client.get("/sso")
    if r.status_code != 400:
        print("   ERRO: esperado 400, obtido", r.status_code, r.json())
        return 1
    print("   OK -> 400 Missing token")

    print("4. A testar GET /sso?token=invalid...")
    r2 = client.get("/sso", params={"token": "invalid"})
    if r2.status_code != 401:
        print("   ERRO: esperado 401, obtido", r2.status_code, r2.json())
        return 1
    print("   OK -> 401 Invalid JWT")

    print("\nTudo OK. A rota /sso está a responder como esperado.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
