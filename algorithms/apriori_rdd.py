from algorithms.utils import *


def test():
    min_support = 0.7
    dataset_dir = "../data/"
    result_dir = "../result/apriori_rdd/"
    dataset_name = "mushroom"

    data_path = dataset_dir + dataset_name + ".txt"
    result_path = result_dir + dataset_name + "/"

    sc = pyspark.SparkContext(appName="Apriori")

    transactions = load(sc, data_path)
    frequentSets = apriori_rdd(transactions, min_support)
    print("apriori rdd num:", frequentSets.count())
    print("apriori rdd result:", frequentSets)
    save(frequentSets, result_path)

    sc.stop()


def apriori_rdd(transactions: pyspark.RDD | list, min_support: float) -> pyspark.RDD:
    # load data
    print(type(transactions))

    lineCount = transactions.count()
    min_frequency = int(min_support * lineCount)
    print(f"Min Freq: {min_frequency} ({min_support} * {lineCount})")

    # count items
    itemFlat = transactions.flatMap(lambda line: line)
    itemUnique = itemFlat.distinct()

    # filter min frequency
    itemSupport = filterMinFrequency(itemFlat, min_frequency)
    frequentSets = itemSupport.map(lambda item: ((item[0],), item[1]))

    print("Base support items:", frequentSets)
    #
    aprioriStatus(itemSupport, frequentSets, min_frequency, lineCount, 1)

    itemSupport = itemSupport.map(lambda item: item[0])

    set_length = 2
    while not itemSupport.isEmpty():
        # extend the set
        extendedSets = itemSupport.cartesian(itemUnique)
        extendedSets = extendedSets.map(flatMergeCartesian)  # ( ('3','1'),'4') -> ('1','3','4')
        extendedSets = extendedSets.filter(lambda item: len(item) == set_length)  # from flatMergeCartesian: ( ('4','3'), '3') -> ('3','4')
        extendedSets = extendedSets.distinct()

        # filter valid sets against transactions
        existingSets = extendedSets.cartesian(transactions)  # -> (extendedSets, transactions)
        existingSets = existingSets.filter(lambda item: issubset(*item))  # not all sets exist as transaction
        existingSets = existingSets.map(lambda item: item[0])  #

        # count occurrences
        itemSupport = filterMinFrequency(existingSets, min_frequency)
        frequentSets = frequentSets.union(itemSupport)

        aprioriStatus(itemSupport, frequentSets, min_frequency, lineCount, set_length)

        itemSupport = itemSupport.map(lambda item: item[0])
        set_length += 1

    return frequentSets





def aprioriStatus(itemSupport, frequentSets, min_frequency, lineCount, set_length) -> None:
    if itemSupport.isEmpty(): return
    max_freq = itemSupport.max(key=lambda item: item[1])[1]
    min_freq = itemSupport.min(key=lambda item: item[1])[1]

    gap_size = ((max_freq - min_freq) / (lineCount - min_frequency))
    print(
        f"Set length: {set_length} ({itemSupport.count()} items) - Set Freq: {min_frequency} < {min_freq}:{max_freq} ({int(gap_size * 100)}%) < {lineCount} - Total sets: {frequentSets.count()}")


def filterMinFrequency(itemsRdd, min_frequency) -> pyspark.RDD:
    setCount = itemsRdd.map(lambda item: (item, 1))
    setCount = setCount.reduceByKey(lambda x, y: x + y)
    return setCount.filter(lambda item: item[1] > min_frequency)


def flatMergeCartesian(extendedItemset) -> tuple:
    itemset, new_item = extendedItemset
    if isinstance(itemset, list):
        itemset = tuple(itemset)
    if not isinstance(itemset, tuple):
        itemset = (itemset,)
    if new_item in itemset: return itemset

    itemset = list(itemset)
    itemset.append(new_item)
    itemset.sort()

    return tuple(itemset)


if __name__ == '__main__':
    test()
