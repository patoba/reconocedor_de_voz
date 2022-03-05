import os
import librosa.display
import json

def build_manifest(data_dir, transcripts_path, manifest_path, wav_path):
    with open(transcripts_path, 'r') as fin:
        with open(manifest_path, 'w') as fout:
            for line in fin:
                transcript = line[: line.find('(')-1].lower()
                transcript = transcript.replace('<s>', '').replace('</s>', '')
                transcript = transcript.strip()
                file_id = line[line.find('(')+1 : -2]  
                audio_path = os.path.join(
                    data_dir, wav_path,
                    file_id[file_id.find('-')+1 : file_id.rfind('-')],
                    file_id + '.wav')

                duration = librosa.core.get_duration(filename=audio_path)

                metadata = {
                    "audio_filepath": audio_path,
                    "duration": duration,
                    "text": transcript
                }
                json.dump(metadata, fout)
                fout.write('\n')

if __name__ == '__main__':
    data_dir = "/mnt/working/ASR/data/"
    transcripts_path = data_dir +  "transcripts.txt"
    manifest_path = data_dir + "manifest.txt"
    wav_path = "archivos_wav/"