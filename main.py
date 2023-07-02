import math
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
stats_path = f"{result_path}dataset_stats.csv"

maxTimeout = 5 * 60 # max timeout, 5 minutes, for low support values
lineTimeout = 0.1 # scale overall timeout with the size of the dataset

algos = [
    {"algorithm_name": "son_apriori", "algorithm": son_rdd},
    {"algorithm_name": "pcy", "algorithm": pcy_rdd},
    {"algorithm_name": "pcy_erode", "algorithm": pcy_erode_rdd},
    {"algorithm_name": "apriori_python", "algorithm": lambda ts, min_sup: apriori_list(ts.collect(), min_sup)},
    {"algorithm_name": "apriori_spark", "algorithm": apriori_rdd},
]

datasets = [
    {"name":"mushroom", "supports":[0.7, 0.5, 0.3]},
    {"name":"retail", "supports":[0.05, 0.005]}, # [0.1, 0.05, 0.005]
    {"name":"50K10", "supports":[0.06, 0.03, 0.01]},
    {"name":"25K40", "supports":[0.01, 0.001]}, #[0.1, 0.01, 0.001]
    {"name":"100K10", "supports":[0.06, 0.03, 0.01]},
    {"name":"100K40", "supports":[0.2, 0.1, 0.05]},
]

csv_div = ','

def main():
    command = sys.argv.pop(0)
    args = sys.argv if len(sys.argv) > 0 else ['tasklist']
    # print(sys.argv)

    os.makedirs(logs_path, exist_ok=True)
    os.makedirs(result_path, exist_ok=True)


    action = args.pop(0)
    if action == 'all':
        createTaskList()
        os.execl("/bin/bash", tasks_path,"&")
    elif action == 'tasklist':
        createTaskList()
    elif action == 'runtask':
        if len(args) != 6: print("Usage:\n main.py runtask <task_name> <algo_name> <min_support> <data_path> <result_path> <index_path>")
        runTaskCli(*args)
    elif action == 'datastats':
        dataStats(dataset_path, stats_path)
    else:
        print("Usage:\npython main.py [all|tasklist|runtask|datastats|help] (Default: tasklist)")


def dataStats(data_path, output_path):

    lines = ["Name, Path, Size, Num lines, Num items, min_freq, max_freq, avg_freq, min_items, max_items, avg_items, hist_x_freq_txt, hist_y_freq_txt, hist_x_items_txt, hist_y_items_txt"]
    for dataset in datasets:
        name = dataset['name']
        path = dataset_path+name+".txt"
        print(name, path)

        # ================================================================ COUNT ================================================================
        filesize = os.path.getsize(path)
        num_lines = 0
        unique_items = {}
        lines_lengths = {}
        with open(path, 'r') as fp:
            for row_num, row in enumerate(fp):
                items = row.strip().split(' ')
                item_cnt = len(items)
                if item_cnt not in lines_lengths: lines_lengths[item_cnt] = 0
                lines_lengths[item_cnt] += 1
                for item in items:
                    if item not in unique_items: unique_items[item] = 0
                    unique_items[item] += 1
                num_lines += 1

        num_unique_items = len(unique_items)

        # ================================================================ FREQUENCY ================================================================
        hist_freq_size = 20

        max_freq = max(unique_items.values())
        min_freq = min(unique_items.values())
        avg_freq = sum(unique_items.values()) / len(unique_items)

        hist_freq_width = (max_freq // hist_freq_size) + 1

        stats_freq = [0] * hist_freq_size
        for item_freq in unique_items.values():
            idx = item_freq // hist_freq_width
            stats_freq[idx] += 1

        hist_x_freq_txt = "|".join([str(int(item * hist_freq_width)) for item in range(hist_freq_size)])
        hist_y_freq_txt = "|".join([str(item) for item in stats_freq])

        # ================================================================ TRANSACTION ================================================================
        hist_items_size = 20

        max_items = max(lines_lengths.keys())
        min_items = min(lines_lengths.keys())
        avg_items = sum([length * cnt for length, cnt in lines_lengths.items()]) / num_lines

        hist_items_width = ( max_items // hist_items_size) + 1
        stats_items = [0] * hist_items_size
        for item_count, num_occurences in lines_lengths.items():
            idx = item_count // hist_items_width
            stats_items[idx] += num_occurences

        hist_x_items_txt = "|".join([str(int(line * hist_items_width)) for line in range(hist_items_size)])
        hist_y_items_txt = "|".join([str(item) for item in stats_items])


        # ================================================================ WRITE ================================================================

        line = (name, path, filesize, num_lines, num_unique_items, min_freq, max_freq, avg_freq, min_items, max_items, avg_items, hist_x_freq_txt, hist_y_freq_txt, hist_x_items_txt, hist_y_items_txt)
        line = csv_div.join([str(item) for item in line])
        lines.append(line)
    content = '\n'.join(lines)
    with open(stats_path, 'w') as f: f.write(content)


# run
def createTaskList():

    tasks = []
    for algo in algos:
        for dataset in datasets:
            dataset_name = dataset['name']
            supports = dataset['supports']
            for min_support in supports:
                sup_slug = str(int(min_support * 1000)).rjust(4, '0')
                task_name = f'{algo["algorithm_name"]}-{dataset_name}-{sup_slug}'
                task = {
                    'task_name': task_name,
                    'dataset': dataset_name,
                    'data_path': f'{dataset_path}{dataset_name}.txt',
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
    dataset_name = os.path.splitext(data_path.split("/")[-1])[0]
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
    sys.stdout.flush()
    result = (name, algorithm_name, dataset_name, data_path, min_support, output_path, outcome, num_sets, total_time)
    writeResult(index_fullpath, result)
    return True

def writeResult(index_path, results):
    line = map(lambda part: f'"{part}"', results)
    line = csv_div.join(line)+"\n"
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