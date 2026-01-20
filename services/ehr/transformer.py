from abc import ABC


class TransformerMap(ABC):
    def __init__(self):
        raise NotImplementedError


class Transformer(ABC):
    def __init__(self):
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError
