from abc import ABC, abstractmethod


class GuiInterface(ABC):
    @abstractmethod
    def get_pages(self):
        pass

    @abstractmethod
    def start_test(self):
        pass

    @abstractmethod
    def cancel_test(self):
        pass

    @abstractmethod
    def stop_test(self):
        pass
    