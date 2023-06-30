import os
import re
from algorithms.utils import *
from algorithms import *
import sys

session_id = int(time.time())

# config benckmark
base_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = f'{base_path}/data/benchmark/'
result_path = f'{base_path}/result/'
logs_path = f'{base_path}/result/logs/'
tasks_path = f"{result_path}tasks_{session_id}.sh"
index_path = f"{result_path}index_{session_id}.csv"

maxTimeout = 5 * 60 # max timeout, 5 minutes, for low support values
lineTimeout = 0.1 # scale overall timeout with the size of the dataset

supports = [0.5, 0.3] # [0.7, 0.5, 0.3]
algos = [
    {"algorithm_name": "son_apriori", "algorithm": son_rdd},
    {"algorithm_name": "pcy", "algorithm": pcy_rdd},
    {"algorithm_name": "pcy_erode", "algorithm": pcy_erode_rdd},
    {"algorithm_name": "apriori_python", "algorithm": lambda ts, min_sup: apriori_list(ts.collect(), min_sup)},
    {"algorithm_name": "apriori_spark", "algorithm": apriori_rdd},
]



def main():
    command = sys.argv.pop(0)
    args = sys.argv if len(sys.argv) > 0 else ['tasklist']
    print(sys.argv)

    os.makedirs(logs_path, exist_ok=True)
    os.makedirs(result_path, exist_ok=True)


    action = args.pop(0)
    if action == 'all':
        createTaskList()
        os.execl("/bin/bash", tasks_path,"&")
    if action == 'tasklist':
        createTaskList()
    elif action == 'runtask':
        if len(args)!=6: print("Usage:\n main.py task_name algo_name min_support data_path result_path index_path")
        runTaskCli(*args)

# run
def createTaskList():
    all_files = os.listdir(dataset_path)
    datasets = list(filter(lambda filename: str(filename).endswith('.txt'), all_files))
    datasets = list(map(lambda filename: os.path.splitext(filename)[0], datasets))

    tasks = []
    for algo in algos:
        for dataset in datasets:
            for min_support in supports:
                sup_slug = int(min_support * 100)
                task_name = f'{algo["algorithm_name"]}_{dataset}_{sup_slug}'
                task = {
                    'task_name': task_name,
                    'dataset': dataset,
                    'data_path': f'{dataset_path}{dataset}.txt',
                    'result_path': f'{result_path}{task_name}/',
                    'min_support': min_support,
                    **algo
                }
                tasks.append(task)
    writeTasks(tasks_path, tasks)


def runTaskCli(name, algorithm_name, min_support, data_path, output_path, index_fullpath):
    algorithm = list(filter(lambda a: a["algorithm_name"] == algorithm_name, algos))
    if len(algorithm) != 1:
        print(f"ERROR: algorithm {algorithm_name} NOT FOUND")
        return False
    algorithm = algorithm[0]['algorithm']

    params = {
        'task_name': name,
        'algorithm': algorithm,
        'data_path': data_path,
        'min_support': float(min_support),
        'result_path': output_path,
        'maxTimeout': -1,
        'lineTimeout': -1
    }
    print("TASK:", name)
    outcome, num_sets, total_time = runTask(**params)
    print("TASK:", outcome, num_sets, total_time)
    result = (name, algorithm_name, data_path, min_support, output_path, outcome, num_sets, total_time)
    writeResult(index_fullpath, result)
    return True

def writeResult(index_path, results):
    line = map(lambda part: f'"{part}"', results)
    line = ";".join(line)+"\n"
    with open(index_path,'a') as f: f.write(line)


def writeTasks(tasks_path, tasks, writeLogs=True):
    cmd = os.path.abspath(__file__)
    tasks_path = os.path.abspath(tasks_path)
    idx_path = os.path.abspath(index_path)
    log_path = os.path.abspath(logs_path)

    lines = [
        "#! /bin/bash\n\n",
        f"cd {base_path} || exit \n"
        f"mkdir -p {log_path} || exit \n"
    ]
    for task in tasks:
        name = task['task_name']
        algo = task['algorithm_name']
        min_support = task['min_support']
        data_path = os.path.abspath(task['data_path'])
        output_path = os.path.abspath(task['result_path'])

        logs_file = f'{log_path}/{name}_logs.txt'
        logs_cli = f"2>&1 | tee {logs_file}" if writeLogs else ''

        line = f"python {cmd} runtask {name} {algo} {min_support} {data_path} {output_path} {idx_path} {logs_cli} || true\n"
        lines.append(line)
    with open(tasks_path,'w') as f: f.writelines(lines)



if __name__ == '__main__': main()



"""


def runTasks(tasks):
    results = []
    last_algo_dataset = None
    last_min_support = 0.0
    for task in tasks:
        min_support = task['min_support']
        algo_dataset = task['algorithm_slug'] + task['data_path']
        if last_algo_dataset == algo_dataset and last_min_support < min_support:
            results.append(('skip-timeout', 0, 0))
            continue

        params = {
            'task_name': task['task_name'],
            'algorithm': task['algorithm'],
            'data_path': task['data_path'],
            'min_support': task['min_support'],
            'result_path': task['result_path'],
            'maxTimeout': maxTimeout,
            'lineTimeout': lineTimeout
        }
        print("TASK:", task['task_name'])
        outcome, num_sets, total_time = runTask(**params)
        print(task['task_name'], outcome, num_sets, total_time)

        # skip future timeouts ( same algo/data but higher support )
        last_algo_dataset = algo_dataset if outcome == 'timeout' else None
        last_min_support = task['min_support']
        result = (task['task_name'], task['algorithm_name'], task['min_support'], task['data_path'], task['result_path'], outcome, num_sets, total_time)
        writeResult(index_path, result)
        results.append(result)

"""