"""
Script de teste para verificar configuração e acesso ao disco Z:
"""
import os
import json

def test_config():
    print("🔍 Testando configuração...")
    
    # Verificar se arquivo de configuração existe
    if os.path.exists('advanced_config.json'):
        print("✅ advanced_config.json encontrado")
        with open('advanced_config.json', 'r') as f:
            config = json.load(f)
            print(f"📋 Configuração: {config}")
            
        # Testar caminho configurado
        path = config.get('path', '')
        print(f"🔍 Caminho configurado: {path}")
        
        if path:
            if os.path.exists(path):
                print(f"✅ Caminho existe: {path}")
                
                # Listar alguns arquivos
                try:
                    files = os.listdir(path)
                    print(f"📁 Arquivos na pasta: {len(files)}")
                    for i, file in enumerate(files[:10]):  # Primeiros 10 arquivos
                        print(f"  {i+1}. {file}")
                    if len(files) > 10:
                        print(f"  ... e mais {len(files) - 10} arquivos")
                except Exception as e:
                    print(f"❌ Erro ao listar arquivos: {e}")
            else:
                print(f"❌ Caminho não existe: {path}")
        else:
            print("❌ Nenhum caminho configurado")
    else:
        print("❌ advanced_config.json não encontrado")
        
    # Testar disco Z: diretamente
    print("\n🔍 Testando disco Z: diretamente...")
    z_path = "Z:\\"
    
    if os.path.exists(z_path):
        print(f"✅ Disco Z: existe: {z_path}")
        try:
            files = os.listdir(z_path)
            print(f"📁 Arquivos no disco Z: {len(files)}")
            for i, file in enumerate(files[:10]):
                print(f"  {i+1}. {file}")
            if len(files) > 10:
                print(f"  ... e mais {len(files) - 10} arquivos")
        except Exception as e:
            print(f"❌ Erro ao listar disco Z: {e}")
    else:
        print(f"❌ Disco Z: não existe: {z_path}")
        
    # Verificar permissões
    print("\n🔐 Verificando permissões...")
    try:
        test_path = "Z:\\"
        if os.path.exists(test_path):
            test_file = os.path.join(test_path, "test_permission.txt")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("✅ Permissões de escrita OK")
        else:
            print("⚠️ Não é possível testar permissões - caminho não existe")
    except Exception as e:
        print(f"❌ Erro de permissão: {e}")

if __name__ == "__main__":
    test_config()
