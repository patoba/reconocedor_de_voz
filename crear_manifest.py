import os
import librosa.display
import json
import sys

def build_manifest(data_dir, transcripts_path, manifest_path, wav_path):
    with open(transcripts_path, 'r') as fin:
        next(fin)
        with open(manifest_path, 'w') as fout:
            for linea in fin:
                separacion = linea.split("\t")
                
                file_nombre = separacion[1].replace(".mp3", "")  

                transcript = separacion[2]

                audio_path = os.path.join(
                    data_dir, wav_path,
                    file_nombre + '.wav')
                
                duracion = librosa.core.get_duration(filename=audio_path)

                metadata = {
                    "audio_filepath": audio_path,
                    "duration": duracion,
                    "text": transcript
                }

                json.dump(metadata, fout)
                fout.write('\n')

if __name__ == '__main__':
    name = str(sys.argv[1])

    checkpoints_folder = "checkpoints/"

    data_dir = "./data/"
    transcripts_folder = data_dir + "transcripts/"
    manifest_folder = data_dir + "manifests/"

    if not os.path.exists(transcripts_folder):
        print(f"creando carpeta {transcripts_folder}")
        create_dir = f"mkdir {transcripts_folder}"
        os.system(create_dir)

    if not os.path.exists(manifest_folder):
        print(f"creando carpeta {manifest_folder}")
        create_dir = f"mkdir {manifest_folder}"
        os.system(create_dir)

    if not os.path.exists(checkpoints_folder):
        print("creando carpeta manifest")
        create_dir = f"mkdir {checkpoints_folder}"
        os.system(create_dir)

    transcripts_path = transcripts_folder + name
    manifest_path = manifest_folder + name.replace(".tsv", ".json")
    wav_path = "clips_wav/"

    build_manifest(data_dir, transcripts_path, manifest_path, wav_path)