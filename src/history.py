import pickle as pkl

class History:
    def __init__(self, size: int = 0, history: list[str] = []):
        self.size = size
        self.history = history

    def append(self, cmd: str):
        self.size += 1
        self.history.append(cmd)

    def __len__(self):
        return len(self.history)

    def __getstate__(self):
        """
        Override the default behaviour for loading pickle file.
        """
        return {'size': self.size, 'history': self.history}

    def save(self, filename: str):
        assert filename.endswith('.pkl'), "The filename provided should end with 'pkl'."
        with open(filename, "wb") as file:
            pkl.dump(self, file)

    @staticmethod
    def load(filename: str):
        global hist
        try:
            with open(filename, "rb") as file:
                tmp = pkl.load(file)
            hist.size = tmp.size
            hist.history = tmp.history
        except FileNotFoundError:
            pass

hist = History()

def history(cmd: str):
    global hist
    if len(hist) == 0:
        return
    else:
        for i, h in enumerate(hist.history):
            print(i, h)

if __name__=='__main__':
    test = History(4, ['ok', "salut", "op", "ii"])
    test.save("test.pkl")

    test2 = History.load("test.pkl")