systemctl start docker
docker pull tensorflow/serving:1.12.0-gpu
docker run --runtime=nvidia -p 8501:8500 --mount type=bind,source=/home/data/dosmono/ai/dosmono-nmt/model/translate_enzh_sub50k/transformer_big/avg/export,target=/models/my_model -e MODEL_NAME=my_model -t tensorflow/serving:1.12.0-gpu &
