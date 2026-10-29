from abc import ABC, abstractmethod
import ollama
class Embed(ABC):
    def __init__(self,model : str):
        self.model = model

    @abstractmethod
    def embedding(self,text : str|list[str]):
        pass

class EmbedOllama(Embed):
    def __init__(self, model):
        super().__init__(model)

    def embedding(self, text : str|list[str]):
        response = ollama.embed(
            model=self.model,
            input=text
        )
        return response["embeddings"]