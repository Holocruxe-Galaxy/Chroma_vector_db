import chromadb


class ChromaDbManager:
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(path="./chroma_db/db")
            self.collection = self.client.get_or_create_collection(
                name="chroma_collection")
        except Exception as e:
            print("Error:", e)

    def insert_data(self, array_data):
        try:
            for index, doc in enumerate(array_data):
                self.collection.add(
                    documents=[doc["doc_content"]],
                    metadatas=[{"doc_name": doc["doc_name"]}],
                    ids=str(index+1),
                )

        except Exception as e:
            print("Error:", e)

    def search_documents(self, document_name, document_section, full_text):
        try:
            if (document_section != False):
                results = self.collection.query(
                    query_texts=document_section, n_results=20)
                finall_data = []
                for index, data in enumerate(results.get('documents')[0]):
                    data_formatted = {
                        'document_name': results['metadatas'][0][index]['doc_name'],
                        'document_content': data,
                        'distance': results['distances'][0][index]
                    }
                    finall_data.append(data_formatted)
                return finall_data
            else:
                results = self.collection.query(
                    query_texts=full_text, n_results=20)
                finall_data = []
                for index, data in enumerate(results.get('documents')[0]):
                    data_formatted = {
                        'document_name': results['metadatas'][0][index]['doc_name'],
                        'document_content': data,
                        'distance': results['distances'][0][index]
                    }
                    finall_data.append(data_formatted)
                return finall_data
        except Exception as e:
            print('Error:', e)
