import itertools

from dataset import Dataset




def main():
    filepath = 'data/T10I4D100K_sample.txt'
    ds = Dataset(filepath)
    data = ds.get_data()


class Apriori:
    def __init__(self, dataset,  support):
        self.dataset = dataset
        self.support = support
        self.data = self.dataset.get_data()

        self.frequentSets = {}

    def getFrequentSets(self, numItems=1):
        itemsSets = {}
        if numItems <= 0: numItems = 1
        if numItems in self.frequentSets: return self.frequentSets[numItems]
        if numItems == 1:
            return self.getFrequentItems()
        elif numItems == 2:
            base = self.getFrequentSets(1)
            keys = base.keys()
            keys.sort()
            keys_larger = []
            frequentSets = {}
            for i, keyA in enumerate(keys):
                for keyB in keys[i:]:
                    keys_larger.append([keyA, keyB])


            return self.getFrequentItems()
        else:
            base = self.getFrequentSets(numItems - 1)
            keys = base.keys()
            key_bases = set([key[0:numItems] for key in keys])
            key_groupby = {key_base:filter(lambda key: numItems>=len(key) and key[0:numItems] == key_base, keys) for key_base in key_bases}

            for key_base, key_list in key_groupby:
                key_larger = [*key_base]
                for key in key_list:
                    additions = filter(lambda part: part not in key_larger, key)
                    key_larger.extend(additions)



        self.frequentSets[numItems] = itemsSets

    def getFrequentItems(self):
        if 1 in self.frequentSets: return self.frequentSets[1]

        frequentSets = {}
        # aggregate
        for row in self.data: # get one row
            for item in row: # get one element of the row
                key = self.buildKey(item)
                if item not in frequentSets: frequentSets[key] = []
                frequentSets[key].append(row)
        # filter
        numItems = len(self.data)
        self.frequentSets[1] = dict(filter(lambda itm: len(itm) / numItems >= self.support, frequentSets))
        return self.frequentSets[1]

    def buildKey(self, items):
        if not isinstance(items, (list,tuple)): items = [items]
        items.sort()
        #key = "_".join(items)
        return items






if __name__ == '__main__': main()