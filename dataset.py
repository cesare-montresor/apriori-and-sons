class Dataset():

    def __init__(self, path, batch_size=None):
        self.path = path
        self.file = None
        self.is_open = False
        self.batch_size = batch_size

    def openFile(self):
        try:
            self.file = open(self.path, "r")
            return True
        except:
            return False


    def get_data(self):
        if not self.openFile(): return False
        self.is_open = True

        if self.batch_size is None:
            lines = self.file.readlines()
            data = [line.split(" ") for line in lines]
            return data

