from math import ceil
import os
from time import time, sleep

def escribir_archivo(file_name, text):
    with open(file_name, 'a') as f:
        f.write(text + '\n')

def escribir(text, file_name):
    print(text)
    escribir_archivo(file_name, text)

def procesar_archivos(archivos_uris, borrar_data):
    for f in archivos_uris:
        ffmep = f'ffmpeg -i "{f}" -ar 16000 {output_dir}/$(basename "{f}" .mp3).wav'
        if os.system(ffmep) != 0:
            return False
        if borrar_data:
            borrar = f'rm -f "{f}"'
            os.system(borrar)
    return True

def procesar_batches(archivos, archivo_log, archivo_log_correctos,
                    batch_size = 100, ignorar_batches = {},
                    borrar_data = True):
    tiempo_inicial = time()
    total_de_archivos = len(archivos)  # 528502
    n_iteraciones = int(ceil(total_de_archivos / batch_size))
    batch_correctos = []
    for i in range(n_iteraciones):
        if i in ignorar_batches:
            s = time() - tiempo_inicial
            escribir(f"batch {i} skipeado - {s} seg", archivo_log)
        else:
            sub_archivos = archivos[i * batch_size:(i + 1) * batch_size]
            s = time() - tiempo_inicial
            if procesar_archivos(sub_archivos, borrar_data):
                escribir(f"batch {i} exitoso - {s} seg", archivo_log)
                batch_correctos.append(i)
                escribir(str(i), archivo_log_correctos)
            else:
                escribir(f"batch {i} fallido - {s} seg", archivo_log)
    escribir("batches correctos:", archivo_log)
    escribir(batch_correctos, archivo_log)
    exactitud = (len(batch_correctos) + len(ignorar_batches)) / total_de_archivos
    escribir("exactitud:", exactitud * 100, "%", archivo_log)

def crear_archivo(ubicacion):
    file = open(ubicacion, "w+")
    file.close()

def obtener_archivos_de_ubicacion(ubicacion):
    return [os.path.abspath(os.path.join(ubicacion, p)) for p in os.listdir(ubicacion)]

if __name__ == '__main__':
    file_name = "cv-corpus-8.0-2022-01-19-es.tar.gz"
    output_dir = f"{file_name[:-10]}/es/clips_wav"
    input_dir = f"{file_name[:-10]}/es/clips"
    log_folder = "log/"

    # descomprimir
    if not os.path.exists(input_dir):
        print("descomprimiendo")
        tar = f"tar -xvf {file_name}"
        os.system(tar)

    # crear carpeta salida
    if not os.path.exists(output_dir):
        print("creando carpeta salida")
        create_dir = f"mkdir {output_dir}"
        os.system(create_dir)

    # crear carpeta log
    if not os.path.exists(log_folder):
        print("creando carpeta log")
        create_dir = f"mkdir {log_folder}"
        os.system(create_dir)

    intento = max(0, len(obtener_archivos_de_ubicacion(log_folder)) - 1)
    file_write_name =  f"{log_folder}registro_{str(intento)}.txt" 
    file_write_name_files_correct = f"{log_folder}/completos.txt"

    # crear historico
    crear_archivo(file_write_name)

    # crear archivo de registros correctos
    if not os.path.exists(file_write_name_files_correct):
        print("creando archivo con batches correctos")
        crear_archivo(file_write_name_files_correct)

    sleep(5)

    # obtener batches completos
    batches_completos = open(file_write_name_files_correct, "r").readlines()
    batches_completos = [int(batch.replace("/n", "")) for batch in batches_completos]

    files = obtener_archivos_de_ubicacion(input_dir) 
    procesar_batches(files, file_write_name, file_write_name_files_correct,
                     ignorar_batches = batches_completos, borrar_data = False)