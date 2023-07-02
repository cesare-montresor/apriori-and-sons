#! /bin/bash

cd /home/cesare/Projects/apriori-and-sons || exit 
mkdir -p /home/cesare/Projects/apriori-and-sons/result/logs || exit


# mushroom
#python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_spark_mushroom_0300 apriori_spark 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark_mushroom_0300 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark_mushroom_0300_logs.txt || true
#python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_mushroom_0300 apriori_spark 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark_mushroom_0300 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark_mushroom_0300_logs.txt || true

# retail
python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_retail_0500 pcy 0.5 /home/cesare/Projects/apriori-and-sons/data/benchmark/retail.txt /home/cesare/Projects/apriori-and-sons/result/pcy_retail_0500 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/pcy_retail_0500_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_retail_0300 pcy 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/retail.txt /home/cesare/Projects/apriori-and-sons/result/pcy_retail_0300 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/pcy_retail_0300_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_retail_0100 pcy 0.1 /home/cesare/Projects/apriori-and-sons/data/benchmark/retail.txt /home/cesare/Projects/apriori-and-sons/result/pcy_retail_0300 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/pcy_retail_0100_logs.txt || true

python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_spark_retail_0500 apriori_spark 0.5 /home/cesare/Projects/apriori-and-sons/data/benchmark/retail.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark_retail_0500 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark_retail_0500_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_spark_retail_0300 apriori_spark 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/retail.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark_retail_0300 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark_retail_0300_logs.txt || true

python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_python_retail_0500 apriori_python 0.5 /home/cesare/Projects/apriori-and-sons/data/benchmark/retail.txt /home/cesare/Projects/apriori-and-sons/result/apriori_python_retail_0500 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_python_retail_0500_logs.txt || true
python /home/cesare/Projects/apriori-and-sons/main.py runtask apriori_python_retail_0300 apriori_python 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/retail.txt /home/cesare/Projects/apriori-and-sons/result/apriori_python_retail_0300 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_python_retail_0300_logs.txt || true

python /home/cesare/Projects/apriori-and-sons/main.py runtask pcy_mushroom_0300 apriori_spark 0.3 /home/cesare/Projects/apriori-and-sons/data/benchmark/mushroom.txt /home/cesare/Projects/apriori-and-sons/result/apriori_spark_mushroom_0300 /home/cesare/Projects/apriori-and-sons/result/index_recovery.csv 2>&1 | tee /home/cesare/Projects/apriori-and-sons/result/logs/apriori_spark_mushroom_0300_logs.txt || true
