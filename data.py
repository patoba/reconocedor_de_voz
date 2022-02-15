from math import ceil
import os
from time import time
import sys

intento = sys.argv[1]

file_name="cv-corpus-8.0-2022-01-19-es.tar.gz"
output_dir=f"{file_name[:-10]}/es/clips_wav"
input_dir=f"{file_name[:-10]}/es/clips"
file_write_name = "log/registro_" + str(intento)
file_write_name_files_correct = "log/completos_" + str(intento)

def escribir_archivo(file_name, text):
    with open(file_name, 'a') as f:
        f.write(text + '\n') 

def escribir(text, file_name = file_write_name):
    print(text)
    escribir_archivo(file_name, text)

def procesar_archivos(archivos_uris):
    for f in archivos_uris:
        ffmep = f'ffmpeg -i "{f}" -ar 16000 {output_dir}/$(basename "{f}" .mp3).wav'
        os.system(ffmep)
    return True

def procesar_batches(archivos, batch_size = 100, ignorar_batches = {}):
    tiempo_inicial = time()
    total_de_archivos = len(archivos)  # 528502
    n_iteraciones = int(ceil(total_de_archivos / batch_size))
    batch_correctos = []
    for i in range(n_iteraciones):
        if i in ignorar_batches:
            s = time() - tiempo_inicial
            escribir(f"batch {i} skipeado - {s} seg")
        else:
            sub_archivos = archivos[i * batch_size:(i + 1) * batch_size]
            s = time() - tiempo_inicial
            if procesar_archivos(sub_archivos):
                escribir(f"batch {i} exitoso - {s} seg")
                batch_correctos.append(i)
                escribir(str(i), file_write_name_files_correct)
            else:
                escribir(f"batch {i} fallido - {s} seg")
    escribir("batches correctos:")
    escribir(batch_correctos)
    exactitud = (len(batch_correctos) + len(ignorar_batches)) / total_de_archivos
    escribir("exactitud:", exactitud * 100, "%")
        
if __name__ == '__main__':
    esta_descomprimir = True
    esta_creada_carpeta = True
    esta_archivo = False

    if not esta_descomprimir:
        tar = f"tar -xvf {file_name}"
        os.system(tar)

    if not esta_creada_carpeta:
        create_dir = f"mkdir {output_dir}"
        os.system(create_dir)

    
    file = open(file_write_name, "w+")
    file.close()

    # files = os.listdir(input_dir)
    files = [os.path.abspath(os.path.join(input_dir, p)) for p in os.listdir(input_dir)]
    procesar_batches(files)
    





