from dataclasses import dataclass
import pickle as pkl

class History:
    def __init__(self, size: int, history: list[str] = []):
        self.size = size
        self.history = history

    def append(self, cmd: str):
        self.size += 1
        self.history.append(cmd)
    
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
        with open(filename, "rb") as file:
            return pkl.load(file)

if __name__=='__main__':
    test = History(4, ['ok', "salut", "op", "ii"])
    test.save("test.pkl")

    test2 = History.load("test.pkl")