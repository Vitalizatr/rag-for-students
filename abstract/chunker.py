from abc import abstractmethod, ABC
from structure.source import Source
from structure.chunk import Chunk

    
class Chunker(ABC):
    def __init__(self, source : Source,chunk_size : int):
        self.source = source
        self.chunk_size = chunk_size
    @abstractmethod
    def divade_chinks(self, text : list[str]):
        pass

class ChunkerStr(Chunker):
    def __init__(self, source : Source,chunk_size : int):
        super().__init__(source,chunk_size)
    def divade_chinks(self,text : list[str]):
        count = 0
        cur_words = []
        index = 0
        for i,page in enumerate(text):
            words = page.split()
            for word in words:
                count += len(word) +1
                cur_words.append(word)
                if count >= self.chunk_size :
                    text_chunk = " ".join(cur_words)
                    yield Chunk(i+1,index,text_chunk,self.source)
                    count = 0
                    cur_words = []
                    index+=1
        if cur_words:
            text_chunk = " ".join(cur_words)
            yield Chunk(i,index,text_chunk,self.source)