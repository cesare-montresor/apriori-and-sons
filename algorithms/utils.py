import os.path
import pyspark
import shutil
import signal
import time


class TimeoutException(Exception): pass

def _didTimeout(signal, frame):
    raise TimeoutException()

def issubset(a,b):
    return set(a).issubset(b)

def print(*args):
    args = map(lambda x: x.collect() if isinstance(x, pyspark.RDD) else x, args)
    __builtins__['print'](*args)

def load(sc, data_path, sep=' ') -> pyspark.RDD:
    itemSets = sc.textFile(data_path)
    return itemSets.map(lambda line: line.strip().split(sep))

def save(data, output_path):
    if os.path.exists(output_path): shutil.rmtree(output_path)
    if isinstance(data, pyspark.RDD):
        write = data.coalesce(1).saveAsTextFile
        write(output_path)
    else:
        os.makedirs(output_path, exist_ok=True)
        with open(output_path+'/results.txt', "w") as f:
            content = "\n".join([str(line) for line in data])
            f.write(content)



def runTask(task_name:str, algorithm, data_path:str, min_support:float, result_path:str=None, maxTimeout:int=-1, lineTimeout:float=-1):
    print("=" * 80)
    print(" " * ((80-len(task_name))//2) + task_name)
    print("=" * 80)


    # load data
    sc = pyspark.SparkContext(appName=task_name)
    transactions = load(sc, data_path)
    if lineTimeout>0:
        total_timeout = int(lineTimeout * transactions.count())
        maxTimeout = total_timeout if maxTimeout < 0 else min(maxTimeout, total_timeout)

    frequentSets = None
    num_sets = 0
    total_time = 0

    # profile task
    try:
        start_time = time.time()
        if maxTimeout > 0: signal.alarm(maxTimeout)
        frequentSets = algorithm(transactions, min_support)
        if isinstance(frequentSets, pyspark.RDD):
            num_sets = frequentSets.count()
        else:
            num_sets = len(frequentSets)
        if maxTimeout > 0: signal.alarm(0)
        total_time = time.time() - start_time

        status = 'success'
    except TimeoutException:
        print(f'TIMEOUT:{task_name}')
        status = 'timeout'
    except Exception as e:
        status = 'error'
        print(f'ERROR:{task_name}:',e)

    # save and return results
    if result_path is not None and frequentSets is not None:
        try: save(frequentSets, result_path)
        except Exception as e:
            print(f"WARNING:{task_name}: failed to save results: {result_path}",e)

    sc.stop()
    print("------------- RESULTS -------------")
    print(task_name)
    print(status)
    print(num_sets)
    print(total_time)


    return status, num_sets, total_time

signal.signal(signal.SIGALRM, _didTimeout)