# Reconocedor de Voz

## Data

El dataset usado para este proceso es el Common Voice de mozilla que puede ser descargado desde [aqui](https://commonvoice.mozilla.org/es/datasets). Pesa alrededor de 20 gb y es necesario descomprimirlo. Por defecto viene en mp3 hay que realizar una conversion a formato wav a una tasa de 16 kbps para que sea compatible con nemo. El peso total del dataset ya descomprimido teniendo tanto los wav como los mp3 es alrededor de 130 gb.

## Configuracion

### Ambiente

El ambiente es importante para poder realizar el entrenamiento correspondiente todas las dependencias necesarias de python (junto con su respectiva version) se encuentran en **requirements.txt**.

Se necesitan los paquetes de linux:

* libfuzzy-dev
* libsndfile1
* ffmpeg
* python3.7
* python3.7-venv
* libpython3.7-dev
* screen (opcional pero util)

Se necesitan los modulos de python:

* nemo
* pytorch_lightning
* ruamel.yaml
* torch

Para poder crear un ambiente de python con los modulos necesarios e instalar las dependencias de linux necesarias basta con correr el script **crear_ambiente.sh** mediante:

```bash
# ./crear_ambiente.sh
```

Este creara un ambiente de python 3.7 llamado *ASR* que permite trabajar correctamente.

### Conversion Audios

El script **crear_data.py** facilita permite descomprimir y realizar la conversion correspondiente del audio (funciona en linux unicamente).  Para correrlo es necesario tener el entorno de python activado, haber descardo el dataset de Common Voice, y mover el dataset a la misma ubicacion que el script. Se corre mediante la siguiente linea:

```bash
$ python crear_data.py
```

### Creacion de Manifest

Se necesita crear un manifest para cada conjunto de datos (train, test, validation). Para ello se necesita mover los archivos wav a la ubicacion: *ubicacion_repo/data/clips_wav*, y los transcripts (archivos *.tsv* de la carpeta descomprimida). Ya con eso se ejecuta el archivo *crear_manifest.py* para cada conjunto de datos en el entorno virtual de la siguiente forma:

```bash
$ python crear_manifest.py nombre_transcript
```

donde nombre_transcript vale "train.tsv", "test.tsv", "validated.tsv"

# Entrenamiento

Para entrenar es necesario tener en la carpeta data los siguiente:

* clips_wav (audios wav)
* transcripts (jsons de ubicaciones de archivos wav)
* quartznet_15x5.yaml (configuracion de parametros)

Para entrenar se realiza lo siguiente:

```bash
$ python entrenamiento.py
```

El entrenamiento actual son con 10 epocas, y se realiza sobre un modelo preentrenado de de reconocedor de voz en ingles.
