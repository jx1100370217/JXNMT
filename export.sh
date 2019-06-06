#bin=../tensor2tensor/bin
#python t2t-trainer --registry_help

PROBLEM=translate_enzh_sub50k
MODEL=transformer
HPARAMS=transformer_big
HOME=`pwd`
DATA_DIR=$HOME/data
TRAIN_DIR=$HOME/model/$PROBLEM/$HPARAMS/avg

t2t-exporter \
  --data_dir=$DATA_DIR \
  --problem=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$TRAIN_DIR \
  --t2t_usr_dir=user_dir
