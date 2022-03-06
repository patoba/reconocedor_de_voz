from ruamel.yaml import YAML
import pytorch_lightning as pl
import nemo.collections.asr as nemo_asr
from omegaconf import DictConfig
from copy import deepcopy

data_dir = "./data/"
config_path = data_dir + 'quartznet_15x5.yaml'
manifests = data_dir + "manifests/"
train_manifest = manifests + "train.json"
test_manifest = manifests + "test.json"

yaml = YAML(typ='safe')
with open(config_path) as f:
    params = yaml.load(f)

new_opt = deepcopy(params['model']['optim'])
new_opt['lr'] = 0.001

params['model']['train_ds']['manifest_filepath'] = train_manifest
params['model']['validation_ds']['manifest_filepath'] = test_manifest

quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5Base-En")

quartznet.change_vocabulary(
    new_vocabulary=
    [
        ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'", "!"
    ] +
    [
        'á', 'é', 'í', 'ñ', 'ó', 'ú', 'ü', '¿', '¡'
    ]
)

quartznet.setup_optimization(optim_config=DictConfig(new_opt))

quartznet.setup_training_data(train_data_config=params['model']['train_ds'])

quartznet.setup_validation_data(val_data_config=params['model']['validation_ds'])

trainer = pl.Trainer(gpus=1, max_epochs=10, # 50 epocas min
                     default_root_dir = "./checkpoints"
                     )

trainer.fit(quartznet)

trainer.save_checkpoint("./checkpoints/ultimo.ckpt")
