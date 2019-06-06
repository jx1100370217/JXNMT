# 将clean.zh（预处理后的中文语料）和clean.en(预处理后的英文语料)合并到clean.both并打乱顺序
paste data/clean.{zh,en} | shuf > data/clean.both

# 将clean.both切分为train,dev,test三部分
sed -n 1,5000p data/clean.both | cut -f 1 > data/test.zh
sed -n 1,5000p data/clean.both | cut -f 2 > data/test.en
sed -n 5001,10000p data/clean.both |cut -f 1 > data/dev.zh
sed -n 5001,10000p data/clean.both |cut -f 2 > data/dev.en
sed -n 10001,49276929p data/clean.both |cut -f 1 > data/train.zh
sed -n 10001,49276929p data/clean.both |cut -f 2 > data/train.en
