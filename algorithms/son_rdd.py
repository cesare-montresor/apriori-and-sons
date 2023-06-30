from algorithms.utils import *
from algorithms.apriori_list import apriori_list


def test():
    min_support = 0.7
    dataset_dir = "../data/"
    result_dir = "../result/son_rdd/"
    dataset_name = "mushroom"

    data_path = dataset_dir + dataset_name + ".txt"
    result_path = result_dir + dataset_name + "/"

    sc = pyspark.SparkContext(appName="Son")

    transactions = load(sc, data_path)
    frequentSets = son_rdd(transactions, min_support)
    print("son rdd num:", frequentSets.count())
    print("son rdd result:", frequentSets)
    save(frequentSets, result_path)
    sc.stop()


def son_rdd(transactions: pyspark.RDD, min_support: float, num_partitions: int | None = None) -> pyspark.RDD:
    sc = transactions.ctx
    num_partitions = sc.defaultParallelism if num_partitions is None else num_partitions

    # computer params
    lineCount = transactions.count()
    candidate_frequency = int(min_support * (lineCount / num_partitions))
    min_frequency = int(min_support * lineCount)
    print(f"Chunk Freq: {candidate_frequency} = ({lineCount} / {num_partitions}) * {min_support} ")
    print(f"Min Freq: {min_frequency} = {lineCount} * {min_support}")

    # partition dataset rdd
    partitionSets = transactions.repartition(num_partitions)

    # find candidates
    candidateSets = partitionSets.mapPartitions(lambda part: apriori_list(list(part), min_support))
    candidateSets = candidateSets.map(lambda item: item[0])
    candidateSets = candidateSets.distinct()
    candidateSets = candidateSets.coalesce(1)
    candidateSets = candidateSets.distinct()
    #print(candidateSets)

    # test candidates
    testingSets = partitionSets.cartesian(candidateSets) # preserve partitioning
    testingSets = testingSets.mapPartitions( candidatesForPartition)
    testingSets = testingSets.reduceByKey(lambda x, y: x + y)
    testingSets = testingSets.filter(lambda item: item[1] > candidate_frequency)

    frequentSets = testingSets.coalesce(1)
    frequentSets = frequentSets.reduceByKey(lambda x, y: x + y)
    frequentSets = frequentSets.filter(lambda item: item[1] > min_frequency)

    return frequentSets

def candidatesForPartition(partition):
    countSubsets = lambda transaction, candidate: (candidate, 1) if issubset(candidate, transaction) else None
    res = map(lambda item:countSubsets(item[0], item[1]), partition)
    res = filter(lambda item: item is not None, res)
    return tuple(res)

if __name__ == '__main__':
    test()
