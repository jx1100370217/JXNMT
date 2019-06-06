mosesdecoder/scripts/recaser/train-truecaser.perl --model en-truecase.mdl --corpus data/en.tok.all

mosesdecoder/scripts/recaser/truecase.perl --model en-truecase.mdl < data/en.tok.all > data/en.tc.all
