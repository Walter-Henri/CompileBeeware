#!/usr/bin/env python3
"""
Script de teste para verificar as funcionalidades do TVApp
"""

import asyncio
import os
import sys
sys.path.insert(0, 'src')

from tvapp.stream_manager import StreamManager
from tvapp.config import DEFAULT_LIVE_URLS

async def test_stream_manager():
    """Testa o StreamManager"""
    print("=== Teste do StreamManager ===")
    
    manager = StreamManager()
    
    # Teste de conexão com o banco
    print("Testando conexão com o banco...")
    client = await manager.get_db_client()
    if client:
        print("✓ Conexão com o banco estabelecida com sucesso!")
        await client.close()
    else:
        print("✗ Falha na conexão com o banco")
        return False
    
    # Teste de extração de stream com streamlink
    print("\nTestando extração de stream com streamlink...")
    test_url = "https://www.youtube.com/@SBT/live"
    m3u8_url = manager.extract_m3u8_with_streamlink(test_url)
    if m3u8_url:
        print(f"✓ Stream extraído com sucesso: {m3u8_url[:50]}...")
    else:
        print("✗ Falha na extração do stream com streamlink")
    
    # Teste de extração com ytdlp (se disponível)
    ytdlp_path = "ytdlp"
    if os.path.exists(ytdlp_path):
        print("\nTestando extração de stream com ytdlp...")
        m3u8_url_ytdlp = manager.extract_m3u8_with_ytdlp(test_url, ytdlp_path)
        if m3u8_url_ytdlp:
            print(f"✓ Stream extraído com ytdlp: {m3u8_url_ytdlp[:50]}...")
        else:
            print("✗ Falha na extração do stream com ytdlp")
    else:
        print("\n⚠ ytdlp não encontrado, pulando teste")
    
    return True

async def test_database_operations():
    """Testa operações do banco de dados"""
    print("\n=== Teste de Operações do Banco ===")
    
    manager = StreamManager()
    
    # Teste de atualização de links
    print("Testando atualização de links...")
    test_lives = [
        {"name": "test_live", "url": "https://www.youtube.com/@SBT/live"}
    ]
    
    success = await manager.update_live_links(test_lives)
    if success:
        print("✓ Links atualizados com sucesso!")
    else:
        print("✗ Falha na atualização de links")
        return False
    
    # Teste de busca de link
    print("Testando busca de link...")
    link = await manager.get_live_link("test_live")
    if link:
        print(f"✓ Link encontrado: {link[:50]}...")
    else:
        print("✗ Link não encontrado")
    
    return True

def test_config():
    """Testa as configurações"""
    print("\n=== Teste de Configurações ===")
    
    from tvapp.config import DATABASE_URL, DATABASE_AUTH_TOKEN, DEFAULT_LIVE_URLS
    
    if DATABASE_URL:
        print("✓ DATABASE_URL configurada")
    else:
        print("✗ DATABASE_URL não configurada")
        return False
    
    if DATABASE_AUTH_TOKEN:
        print("✓ DATABASE_AUTH_TOKEN configurada")
    else:
        print("✗ DATABASE_AUTH_TOKEN não configurada")
        return False
    
    if DEFAULT_LIVE_URLS:
        print(f"✓ {len(DEFAULT_LIVE_URLS)} lives configuradas")
        for live in DEFAULT_LIVE_URLS:
            print(f"  - {live['name']}: {live['url']}")
    else:
        print("✗ Nenhuma live configurada")
        return False
    
    return True

async def main():
    """Função principal de teste"""
    print("TVApp - Teste de Funcionalidades\n")
    
    # Teste de configurações
    config_ok = test_config()
    
    if not config_ok:
        print("\n❌ Falha nos testes de configuração")
        return
    
    # Teste do StreamManager
    stream_ok = await test_stream_manager()
    
    if not stream_ok:
        print("\n❌ Falha nos testes do StreamManager")
        return
    
    # Teste de operações do banco
    db_ok = await test_database_operations()
    
    if not db_ok:
        print("\n❌ Falha nos testes do banco de dados")
        return
    
    print("\n✅ Todos os testes passaram com sucesso!")
    print("\nO TVApp está pronto para uso!")

if __name__ == "__main__":
    asyncio.run(main())

