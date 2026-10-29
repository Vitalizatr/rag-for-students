
### Math RAG System

A local RAG (Retrieval-Augmented Generation) system built in Python, engineered for high-precision search and question-answering over mathematical text documents. The system optimizes raw user queries, retrieves relevant contexts (including complex formulas, vector definitions, and coordinate spaces) from a vector database, and generates accurate responses using a local LLM. 

### Architecture Features

* **Query Optimization:** Translates raw or ambiguous user questions into a single paragraph of structured technical context before performing the vector database search to improve retrieval quality.
* **Mathematical Chunking:** Specifically handles mathematical texts, preserving the structural integrity of definitions, vector coordinates, formulas, and pseudo-graphics.
* **Neighboring Context Retrieval:** To prevent losing vital mathematical context, the system automatically parses the retrieved chunk's ID format (file_name:id) and fetches adjacent chunks — one chunk **before** (id-1) and one **after** (id+1). This ensures that formulas are never separated from their variable definitions or theorem premises.
* **Fully Local Stack:** Complete data privacy and offline capability using a local vector database and local model inference.
* **Ollama Orchestration:** Powered by the RagUseCase class to manage the query lifecycle and handle final response generation via the deepseek-r1:14b model.

### System Workflow

The entire lifecycle of a request is orchestrated by the RagUseCase class: 

1. Receives the raw user query.
2. Rewrites and optimizes the query into a dense technical block for the vector search.
3. Performs a vector lookup to find the top matching mathematical chunks.
4. Extracts the chunk IDs and pulls adjacent blocks (id-1, id+1) to rebuild a continuous context window.
5. Formulates an enriched, strictly factual System Instruction (using UTF-8 encoding).
6. Streams the final tokens from the local Ollama instance running DeepSeek-R1.

### Requirements

* Python 3.10+
* A running local Ollama instance with the deepseek-r1:14b model pulled
* Project dependencies (see requirements.txt)

### Quick Start

1. **Clone the repository:** 


2. **Install dependencies:** 

bash

pip install -r requirements.txt

3. **Ingest Documents:**
Place your mathematical PDFs or documents into the data/ directory and run the ingestion script to populate the vector store: 


4. **Run the Application:** 

bash

python main.py


### Code Example

python

from rag_module import RagUseCase

# Initialize the RAG use case with your local model
rag = RagUseCase(model_name="deepseek-r1:14b")

# Execute a query
query = "What is a unit vector?"
response = rag.execute(query)

print("System Response:")
print(response)


### Prompt Configuration

The system utilizes strict system guidelines optimized for mathematical logic. The model is explicitly restricted from hallucinating facts, forcing it to rely solely on the injected sliding window context to describe definitions like unit vectors, zero vectors, or coordinate transforms.
