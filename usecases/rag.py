import pymupdf
from abstract.reader import ReaderOS,Reader
from abstract.chunker import ChunkerStr,Chunker
from structure.source import Source
from abstract.storage import StorageChroma,Storage
from abstract.embedder import EmbedOllama,Embed
import chromadb

client = chromadb.PersistentClient(path="storage/chromadb")
embedder = EmbedOllama(model = "nomic-embed-text")
storage = StorageChroma(client,embedder,"math")

data_folder = "./data"

        
class RagUseCase():
    def __init__(self,client,embedder : Embed,storage : Storage,reader : Reader):
        self.client = client
        self.embedder = embedder
        self.storage = storage
        self.reader = reader

    @classmethod
    def from_basic(cls,path,model,table_name,data_folder):
        client = chromadb.PersistentClient(path=path)
        embedder = EmbedOllama(model=model)
        storage = StorageChroma(client=client, embedder=embedder, table_name=table_name)
        reader = ReaderOS(data_folder)
        return cls(
            client=client,
            embedder=embedder,
            storage=storage,
            reader=reader
        )
    
    def update_data(self,format,chunk_size):
        
        chunks = []
        for file in self.reader.get_list_of_files(format):
            with pymupdf.open(file) as doc:
                text = []
                for page in doc:
                    text.append(page.get_text())
            
                source = Source.create_from_pdf(file,text)
                chunker = ChunkerStr(source,chunk_size)
                chunks.extend(chunker.divade_chinks(text))

        self.storage.storage_data(chunks)

    def search(self,text):
        return self.storage.get_data_by_text(text)

    def delete_data(self):
        self.storage.delete_data()

    def search_by_ids(self,ids):
        return self.storage.get_data_by_ids(ids);

    def advanse_search_by_index(self,prompt):
        response = self.search(prompt)
        
        response_id = response["ids"][0][0]

        file_name, chunk_id = response_id.split(":")
        chunk_id = int(chunk_id)

        ids = [f"{file_name}:{i}" for i in (chunk_id - 1, chunk_id, chunk_id + 1)]
        return self.search_by_ids(ids)
        