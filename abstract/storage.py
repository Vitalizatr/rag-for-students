from abc import ABC,abstractmethod
from abstract.embeder import Embed
from structure.chunk import Chunk

class Storage(ABC):
    def __init__(self, client, embeder : Embed, name_table : str):
        self.client = client
        self.embeder = embeder
        self.name_table = name_table

    @abstractmethod
    def storage_data(self,data : list[Chunk]):
        pass

    @abstractmethod
    def delete_data(self):
        pass

    @abstractmethod
    def get_data_by_ids(self,ids):
        pass

    @abstractmethod
    def get_data_by_text(self,text):
        pass


class StorageChroma(Storage):
    def __init__(self, client : chromadb.PersistentClient, embeder : Embed, name_table : str):
        super().__init__(client,embeder, name_table) 
        self.collection = client.get_or_create_collection(name=name_table)

    
    def storage_data(self,data : list[Chunk]):
        documents = [chunk.text for chunk in data ]
        ids = [f"{chunk.source.name}:{chunk.page}.{chunk.index}" for chunk in data]
        metadatas = [{"pages" : chunk.source.pages,
                     "full_path" : chunk.source.full_path,
                     "sha256_hash" : chunk.source.sha256_hash,
                     "updated_at_sec" : chunk.source.updated_at_sec
                     } for chunk in data ]
        embeddings = self.embeder.embeding(documents)
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
                     


    def delete_data(self):
        self.client.delete_collection(name=self.name_table)
        self.collection = self.client.get_or_create_collection(name=self.name_table)


    def get_data_by_ids(self,ids):
        result = self.collection.get(ids=ids)
        return result

    def get_data_by_text(self,text):
        query_vector = self.embeder.embeding(text)
        result = self.collection.query(
            query_embeddings=query_vector,
            n_results=1
        )
        return result