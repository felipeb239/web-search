import os
import json

print("🚀 Teste Rápido - Sistema de Busca")
print("=" * 40)

# Testar configuração
if os.path.exists('advanced_config.json'):
    with open('advanced_config.json', 'r') as f:
        config = json.load(f)
    print(f"✅ Configuração carregada: {config['path']}")
    
    # Testar caminho
    path = config['path']
    if os.path.exists(path):
        print(f"✅ Caminho existe: {path}")
        files = os.listdir(path)
        print(f"📁 Arquivos encontrados: {len(files)}")
    else:
        print(f"❌ Caminho não existe: {path}")
else:
    print("❌ Arquivo de configuração não encontrado")

print("\n🎯 Teste concluído!")
