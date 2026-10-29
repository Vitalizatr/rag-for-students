from abc import ABC,abstractmethod
from abstract.embedder import Embed
from structure.chunk import Chunk
from chromadb import PersistentClient
class Storage(ABC):
    def __init__(self, client, embedder : Embed, table_name : str):
        self.client = client
        self.embedder = embedder
        self.table_name = table_name

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
    def __init__(self, client : PersistentClient, embedder : Embed, table_name : str):
        super().__init__(client,embedder, table_name) 
        self.collection = client.get_or_create_collection(name=table_name)
        
    
    def storage_data(self,data : list[Chunk]):
        documents = [chunk.text for chunk in data ]
        ids = [f"{chunk.source.name}:{chunk.index}" for chunk in data]
        metadatas = [{"pages" : chunk.source.pages,
                     "full_path" : chunk.source.full_path,
                     "sha256_hash" : chunk.source.sha256_hash,
                     "updated_at_sec" : chunk.source.updated_at_sec
                     } for chunk in data ]
        embeddings = self.embedder.embedding(documents)
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
                     


    def delete_data(self):
        self.client.delete_collection(name=self.table_name)
        self.collection = self.client.get_or_create_collection(name=self.table_name)


    def get_data_by_ids(self,ids):
        result = self.collection.get(ids=ids)
        return result

    def get_data_by_text(self,text):
        query_vector = self.embedder.embedding(text)
        result = self.collection.query(
            query_embeddings=query_vector,
            n_results=1
        )
        return result

