mv data/en.tc.all data/data.en
mv data/zh.jieba.all data/data.zh

#rm -rf data/en.*
#rm -rf data/zh.all

mosesdecoder/scripts/training/clean-corpus-n.perl data/data zh en data/clean 1 100
