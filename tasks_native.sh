#! /bin/bash

cd /home/cesare/Projects/apriori-and-sons || exit 
mkdir -p /home/cesare/Projects/apriori-and-sons/result/logs || exit 

# TEST: no significat difference
#python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_spark-mushroom-0700-native-no apriori_spark 0.7 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark-mushroom-0700-native-no /home/cesare/Projects/apriori-and-sons/result/index_native.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark-mushroom-0700-native-no_logs.txt || true
#export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native
#python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_spark-mushroom-0700-native-yes apriori_spark 0.7 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark-mushroom-0700-native-yes /home/cesare/Projects/apriori-and-sons/result/index_native.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark-mushroom-0700-native-yes_logs.txt || true


python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_erode-mushroom-0300-native-no pcy_erode 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/pcy_erode-mushroom-0300-native-no /home/cesare/Projects/apriori-and-sons/result/index_native.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/pcy_erode-mushroom-0300-native-no_logs.txt || true
#export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native
#python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_erode-mushroom-0300-native-yes pcy_erode 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/pcy_erode-mushroom-0300-native-yes /home/cesare/Projects/apriori-and-sons/result/index_native.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/pcy_erode-mushroom-0300-native-yes_logs.txt || true
