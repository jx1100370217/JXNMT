# 训练模型
t2t-trainer --data_dir=data \
	--problem=translate_enzh_sub50k \
	--model=transformer \
	--hparams_set=transformer_big \
	--output_dir=model/translate_enzh_sub50k/transformer_big \
	--train_steps=5000000 \
	--worker_gpu=2 \
	--t2t_usr_dir=user_dir
