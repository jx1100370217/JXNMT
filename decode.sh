# 模型解码
t2t-decoder --t2t_usr_dir=user_dir \
	--data_dir=data \
	--problem=translate_enzh_sub50k \
	--model=transformer \
	--hparams_set=transformer_big \
	--output_dir=model/translate_enzh_sub50k/transformer_big \
	--decode_beam_size=32 \
	--decode_from_file=data/test.en \
	--decode_to_file=result
