import os
import math
from pathlib import Path
import sys
import itertools

class Sizer():
    def __init__(self, *args, **kwargs) -> None:
        args, kwargs = args, kwargs
        self.TOTAL_SIZE = 0
        self.TOTAL_DIRS = 0
        self.TOTAL_SUBDIRS = 0
        self.TOTAL_FILES = 0
        self.FILE_PATH = Path.cwd()

    def loading_bar(self, current, total):

        percent = (current * 100) // total

        width = 30

        sys.stdout.write("\r[")

        for i in range(width):
            
            if i < percent * width // 100:
                sys.stdout.write("#")
            else:
                sys.stdout.write(" ")

        sys.stdout.write(f"] {percent}%")
        sys.stdout.flush()

    def spinner(self, message):

        for c in itertools.cycle("|/-\\"):
            sys.stdout.write(f"\r{message}... {c}")
            sys.stdout.flush()
            yield
        
    def list_dir(self, path):

        counter = 0


        print(f"RAIZ: {path}")
        print()

        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isdir(full_path):
                counter+=1

        self.TOTAL_DIRS = counter
    
    def format_size(self, bytes_size: int, base: int = 1024) -> str:
       
        if bytes_size <= 0:
            return "0B"

        sizes = "B", "KB", "MB", "GB", "TB", "PB"

        sizes_idex = int(math.log(bytes_size, base))

        power = base ** sizes_idex
       
        final_size = bytes_size / power
        
        abrev = sizes[sizes_idex]
        return f'{final_size:.2f} {abrev}'
    
    def count_files(self, path):

        spin = self.spinner("CONTANDO")
        counter = 0

        print("CONTANDO ARQUIVOS...")
        print()

        for _, _, files in os.walk(path):
            next(spin)
            counter+=len(files)

        print("\n")
        print("CONTAGEM CONCLUIDA!")
        print()

        return counter

    def list_subdir(self, path, file_name):

        total_files = self.count_files(path)
        processed_size = 0
        subdir_counter = 0
        file_counter = 0


        with open(os.path.join(self.FILE_PATH, file_name), "w", encoding="UTF-8", errors="replace") as _file_:

            print("ESCANEANDO ESTRUTURA...")
            print()

            spin = self.spinner("ESCANEANDO")

            for i in os.walk(path):
                next(spin)

            print("\rESCANEAMENTO CONCLUIDO!")
            print()
                
            print()
            print("CALCULANDO TAMANHO TOTAL DO DIRETORIO...")
            print()

            for root, dirs, files in os.walk(path):
                _file_.write(f"RAIZ: {root}\n")

                for dir_ in dirs:
                    _file_.write(f"    DIRETORIO: {dir_}\n")
                    subdir_counter+=1

                for file_ in files:
                    full_path = os.path.join(root, file_)

                    try:
                        size = os.path.getsize(full_path)
                    except (FileNotFoundError, PermissionError, OSError):
                        continue

                    self.TOTAL_SIZE += size
                    processed_size+=1

                    self.loading_bar(processed_size, total_files)

                    _file_.write(f"      ARQUIVO: {file_} TAMANHO: {self.format_size(size)}\n")
                    file_counter+=1

        self.TOTAL_SUBDIRS = subdir_counter
        self.TOTAL_FILES = file_counter

        print()

        print("\n")

        print(f"TOTAL DE DIRETORIOS: {self.TOTAL_DIRS}")
        print(f"TOTAL DE SUB DIRETORIOS: {self.TOTAL_SUBDIRS}")
        print(f"TOTAL DE ARQUIVOS: {self.TOTAL_FILES}")

        print()
        print(f"TAMANHO TOTAL DO DIRETORIO {path}: {self.format_size(self.TOTAL_SIZE)}")
        print()

        return self.TOTAL_SIZE


                    

if __name__ == "__main__":

    try:

        print()
        dirs = int(input("ENTRE COM O NUMERO DE DIRETORIOS QUE IRA ESCANEAR: "))
        print()

        total = 0

        for i in range(1, (dirs + 1)):
            print("----------------------------------------\n")
            path = input(f"ENTRE COM O CAMINHO DO DIRETORIO {i}: ")
            print()

            path_name = os.path.basename(path)

            if not os.path.isdir(path):
                raise NotADirectoryError

            main = Sizer()
            main.list_dir(path)
            total+=main.list_subdir(path, f"report_{path_name}.txt")
        print()

        print("----------------------------------------\n")

        print(f"TAMANHO TOTAL DOS DIRETORIOS ESCANEADOS: {Sizer().format_size(total)}")

    except ValueError:
        print("ENTRE COM NUMERO VALIDO!")
    except NotADirectoryError:
        print("ENTRE COM UM DIRETORIO VALIDO!")