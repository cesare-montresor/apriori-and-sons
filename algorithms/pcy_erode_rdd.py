from algorithms.utils import *
from itertools import combinations

def test():
    min_support = 0.4
    dataset_dir = "../data/"
    result_dir = "../result/pcy_rdd/"
    dataset_name = "mushroom"

    data_path = dataset_dir + dataset_name + ".txt"
    result_path = result_dir + dataset_name + "/"

    sc = pyspark.SparkContext(appName="PCY")

    transactions = load(sc, data_path)
    frequentSets = pcy_erode_rdd(transactions, min_support)
    print("pcy rdd num:", frequentSets.count())
    print("pcy rdd result:", frequentSets)
    save(frequentSets, result_path)
    sc.stop()


def pcy_erode_rdd(transactions: pyspark.RDD, min_support: float, num_partitions: int | None = None) -> pyspark.RDD:
    sc = transactions.ctx
    num_partitions = sc.defaultParallelism if num_partitions is None else num_partitions

    # computer params
    lineCount = transactions.count()
    min_frequency = int(min_support * lineCount)
    print(f"Min Freq: {min_frequency} = {lineCount} * {min_support}")

    # partition dataset rdd

    itemFlat = transactions.flatMap(lambda line: line)

    # count items
    setCount = itemFlat.map(lambda item: (item, 1))
    setCount = setCount.reduceByKey(lambda x, y: x + y)
    frequentSets = setCount.filter(lambda item: item[1] > min_frequency)
    print(frequentSets.count())

    validationSet = frequentSets.map(lambda item: item[0]).collect()
    supportSet = [(item,) for item in validationSet]
    candidateSize = 2

    while len(validationSet)>0:
        print(f"candidateSize:", candidateSize)
        print(f"supportSets:", validationSet)
        print("transactions size", transactions.count() )
        transactions = reduceTransactions(transactions, validationSet, candidateSize)

        pairsCount = transactions.flatMap(lambda transaction: findPairs(transaction, candidateSize))
        pairsCount = pairsCount.reduceByKey(lambda x, y: x + y)
        pairsCount = pairsCount.filter(lambda item: item[1] > min_frequency)

        frequentSets = frequentSets.union(pairsCount)
        print("pairsCount:", pairsCount.count())
        validationSet = pairsCount.flatMap(lambda item:item[0]).distinct().collect()

        candidateSize += 1

    print("transactions size", transactions.count())

    return frequentSets
def reduceTransactions(transactions: pyspark.RDD, validationSet: list | tuple, candidateSize:int)->pyspark.RDD:
    reducedSet = transactions.map(lambda transaction: filterTransactionItems(transaction, validationSet, candidateSize))
    reducedSet = reducedSet.filter(lambda transaction: transaction is not None)
    return reducedSet

def filterTransactionItems(transaction:list|tuple, validationSet, candidateSize:int) -> tuple|None:
    if len(transaction) < candidateSize: return None
    validItems = set(filter(lambda item: item in validationSet, transaction))
    if len(validItems) < candidateSize: return None
    return tuple(sorted(validItems))


def findPairs(transaction:list|tuple, candidateSize:int) -> tuple:
    pairs = combinations(transaction, candidateSize)
    return tuple((pair, 1) for pair in pairs)

def filterMinFrequency(itemsRdd:pyspark.RDD, min_frequency:float) -> pyspark.RDD:
    setCount = itemsRdd.map(lambda item: (item, 1))
    setCount = setCount.reduceByKey(lambda x, y: x + y)
    return setCount.filter(lambda item: item[1] > min_frequency)

def patitionToBucket(partition, min_support):
    return []


def candidatesForPartition(partition) -> tuple:
    countSubsets = lambda transaction, candidate: (candidate, 1) if issubset(candidate, transaction) else None
    res = map(lambda item:countSubsets(item[0], item[1]), partition)
    res = filter(lambda item: item is not None, res)
    return tuple(res)

def pcyStatus(itemSupport, frequentSets, min_frequency, lineCount, set_length) -> None:
    if itemSupport.isEmpty(): return
    max_freq = itemSupport.max(key=lambda item: item[1])[1]
    min_freq = itemSupport.min(key=lambda item: item[1])[1]

    gap_size = ((max_freq - min_freq) / (lineCount - min_frequency))
    print(
        f"Set length: {set_length} ({itemSupport.count()} items) - Set Freq: {min_frequency} < {min_freq}:{max_freq} ({int(gap_size * 100)}%) < {lineCount} - Total sets: {frequentSets.count()}")


if __name__ == '__main__':
    test()
