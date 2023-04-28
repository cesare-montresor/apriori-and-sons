from dataset import Dataset




def main():
    filepath = 'data/T10I4D100K_sample.txt'
    ds = Dataset(filepath)
    data = ds.get_data()


class Apriori:
    def __init__(self, dataset):
        self.dataset = dataset
        self.data = None
        self.itemsCount = {}
        self.frequentSets = {}

    def process(self, support, numItems):
        self.support = support
        self.data = self.dataset.get_data()
        self.countItems()
        self.filterFrequentItems()

    def computeFrequentSet(self, numItems):
        itemsSets = {}

        self.frequentSets[numItems] = itemsSets

    def filterFrequentItems(self):
        numItems = len(self.data)
        self.frequentSets[1] = filter(lambda itm: itm/numItems >= self.support, self.itemsCount)

    def countItems(self):
        for lines in self.data:
            for items in lines:
                for item in items:
                    if item not in self.itemsCount: self.itemsCount[item] = 0
                    self.itemsCount[item] += 1






if __name__ == '__main__': main()