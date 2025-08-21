import os
print("Teste iniciado")

# Verificar se Z: existe
z_path = "Z:\\"
print(f"Verificando {z_path}")

if os.path.exists(z_path):
    print("Z: existe!")
    try:
        files = os.listdir(z_path)
        print(f"Arquivos encontrados: {len(files)}")
        for i, file in enumerate(files[:5]):
            print(f"  {file}")
    except Exception as e:
        print(f"Erro: {e}")
else:
    print("Z: não existe")

print("Teste concluído")
