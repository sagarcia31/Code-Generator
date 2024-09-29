import os
import shutil

def remove_generated_files_and_pycache(directory):
    # Lista de diretórios que queremos limpar
    directories_to_clean = [
        '__pycache__',
        'back_end/generated',
        'back_end/__pycache__',
        'front_end/src/components',
        'front_end/src/services',
        'front_end/src',
        'trained_models/bdd_model'
    ]
    
    # Extensões de arquivos gerados automaticamente
    generated_extensions = ['.py', '.js']

    # Remover arquivos gerados automaticamente e as pastas vazias
    for dir_path in directories_to_clean:
        if os.path.exists(dir_path):
            for root, dirs, files in os.walk(dir_path, topdown=False):
                for file in files:
                    if any(file.endswith(ext) for ext in generated_extensions):
                        file_path = os.path.join(root, file)
                        print(f'Removendo arquivo gerado: {file_path}')
                        os.remove(file_path)
                
                # Tentar remover a pasta se ela estiver vazia
                if os.path.exists(root) and not os.listdir(root):
                    print(f'Removendo diretório vazio: {root}')
                    os.rmdir(root)

    # Remover diretórios __pycache__
    for root, dirs, files in os.walk(directory, topdown=False):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            if os.path.exists(pycache_path):
                print(f'Removendo diretório __pycache__: {pycache_path}')
                shutil.rmtree(pycache_path)

        # Tentar remover pastas vazias após limpar __pycache__
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if os.path.exists(dir_path) and not os.listdir(dir_path):
                print(f'Removendo diretório vazio: {dir_path}')
                os.rmdir(dir_path)

if __name__ == "__main__":
    # Diretório raiz do seu projeto
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Executa a limpeza
    remove_generated_files_and_pycache(project_root)
    print('Limpeza concluída!')