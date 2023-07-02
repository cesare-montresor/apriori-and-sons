#! /bin/bash

cd /home/cesare/Projects/apriori-and-sons || exit 
mkdir -p /home/cesare/Projects/apriori-and-sons/result/logs || exit 


python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_spark-mushroom-0700-integers apriori_spark 0.7 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark-mushroom-0700-native-no /home/cesare/Projects/apriori-and-sons/result/index_integers.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark-mushroom-0700-integers_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_spark-mushroom-0700-integers apriori_spark 0.7 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark-mushroom-0700-native-no /home/cesare/Projects/apriori-and-sons/result/index_integers.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark-mushroom-0700-integers_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_spark-mushroom-0700-integers apriori_spark 0.7 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark-mushroom-0700-native-no /home/cesare/Projects/apriori-and-sons/result/index_integers.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark-mushroom-0700-integers_logs.txt || true

python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_erode-mushroom-0300-integers pcy_erode 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/pcy_erode-mushroom-0300-native-no /home/cesare/Projects/apriori-and-sons/result/index_integers.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/pcy_erode-mushroom-0300-integers_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_erode-mushroom-0300-integers pcy_erode 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/pcy_erode-mushroom-0300-native-no /home/cesare/Projects/apriori-and-sons/result/index_integers.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/pcy_erode-mushroom-0300-integers_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_erode-mushroom-0300-integers pcy_erode 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/pcy_erode-mushroom-0300-native-no /home/cesare/Projects/apriori-and-sons/result/index_integers.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/pcy_erode-mushroom-0300-integers_logs.txt || true

python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_python-mushroom-0500-integers apriori_python 0.5 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark-mushroom-0500-native-no /home/cesare/Projects/apriori-and-sons/result/index_integers.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark-mushroom-0500-integers_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_python-mushroom-0500-integers apriori_python 0.5 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark-mushroom-0500-native-no /home/cesare/Projects/apriori-and-sons/result/index_integers.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark-mushroom-0500-integers_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_python-mushroom-0500-integers apriori_python 0.5 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark-mushroom-0500-native-no /home/cesare/Projects/apriori-and-sons/result/index_integers.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark-mushroom-0500-integers_logs.txt || true
