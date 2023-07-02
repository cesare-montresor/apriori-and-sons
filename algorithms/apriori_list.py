from algorithms.utils import issubset
from itertools import product


def test():
    min_support = 0.7
    dataset_dir = "../data/"
    result_dir = "../result/apriori_list/"
    dataset_name = "mushroom"

    data_path = dataset_dir + dataset_name + ".txt"
    result_path = result_dir + dataset_name + "/"

    sc = pyspark.SparkContext(appName="Apriori")

    transactions = load(sc, data_path)
    lines = transactions.collect()
    frequentSets = apriori_list(lines, min_support)
    print("apriori list num:", len(frequentSets))
    print("apriori list result:", frequentSets)
    #save(frequentSets, result_path)

    sc.stop()


def apriori_list(transactions: list | tuple, min_support: float) -> tuple:
    # load data

    lineCount = len(transactions)
    min_frequency = int(min_support * lineCount)
    print(f"Min Freq: {min_frequency} ({min_support} * {lineCount})")

    # count items
    itemFlat = []
    for line in transactions: itemFlat.extend(line)
    itemUnique = set(itemFlat)
    itemFlat = tuple(itemFlat)

    # filter min frequency
    itemSupport = filterMinFrequency(itemFlat, min_frequency)
    frequentSets = list(map(lambda item: ((item[0],), item[1]), itemSupport))

    aprioriStatus(itemSupport, frequentSets, min_frequency, lineCount, 1)

    itemSupport = tuple(map(lambda item: item[0], itemSupport))

    set_length = 2
    while not len(itemSupport) == 0:
        # extend the set
        extendedSets = product(itemSupport, itemUnique)
        extendedSets = map(flatMergeCartesian, extendedSets)  # ( ('3','1'),'4') -> ('1','3','4')
        extendedSets = tuple(filter(lambda item: len(item) == set_length, extendedSets))  # from flatMergeCartesian: ( ('4','3'), '3') -> ('3','4')
        extendedSets = tuple(set(extendedSets))

        # filter valid sets against transactions
        existingSets = product(extendedSets, transactions)
        existingSets = tuple(filter(lambda item: set(item[0]).issubset(item[1]), existingSets))  # not all sets exist as transaction
        existingSets = tuple(map(lambda item: item[0], existingSets))

        # count occurrences
        itemSupport = filterMinFrequency(existingSets, min_frequency)
        frequentSets.extend(itemSupport)

        aprioriStatus(itemSupport, frequentSets, min_frequency, lineCount, set_length)

        itemSupport = tuple(map(lambda item: item[0], itemSupport))
        set_length += 1

    return tuple(frequentSets)


def aprioriStatus(itemSupport, frequentSets, min_frequency, lineCount, set_length) -> None:
    if len(itemSupport) == 0: return
    max_freq = max(itemSupport, key=lambda item: item[1])[1]
    min_freq = min(itemSupport, key=lambda item: item[1])[1]

    gap_size = ((max_freq - min_freq) / (lineCount - min_frequency))
    print(
        f"Set length: {set_length} ({len(itemSupport)} items) - Set Freq: {min_frequency} < {min_freq}:{max_freq} ({int(gap_size * 100)}%) < {lineCount} - Total sets: {len(frequentSets)}")


def filterMinFrequency(items, min_frequency) -> tuple:
    setCount = {}
    for item in items:
        if item not in setCount: setCount[item] = 0
        setCount[item] += 1

    setCount = tuple(map(lambda idx: (idx, setCount[idx]), setCount))
    return tuple(filter(lambda item: item[1] > min_frequency, setCount))


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
