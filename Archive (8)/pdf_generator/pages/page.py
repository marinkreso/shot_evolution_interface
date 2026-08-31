from abc import ABC, abstractmethod


# TODO Move all page to subclass page
class Page(ABC):
    def __init__(self, document, data, variant=None) -> None:
        self.document = document
        self.data = data
        self.variant = variant

    @property
    @abstractmethod
    def execution_cost(self):
        pass
