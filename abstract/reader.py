from abc import abstractmethod,ABC
import os
class Reader(ABC):
    def __init__ (self,data_folder : str):
        self.data_folder = data_folder
    @abstractmethod
    def get_list_of_files(self,type_file : str):
        pass

class ReaderOS(Reader):
    def __init__(self, data_folder: str):
        super().__init__(data_folder)

    def get_list_of_files(self,type_file : str):
        files = os.listdir(self.data_folder)
        for file in files:
            full_path = os.path.join(self.data_folder,file)
            if(os.path.isfile(full_path) and file.lower().endswith(type_file)):
                yield full_path