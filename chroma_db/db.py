import chromadb
import uuid


class ChromaDbManager:
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(path="./chroma_db/db")
            self.collection = self.client.get_or_create_collection(
                name="chroma_collection")
        except Exception as e:
            print("Error:", e)

    def delete_all_data(self):
        results = self.collection.get()
        all_ids = results["ids"]

        if all_ids:
            self.collection.delete(ids=all_ids)
            print(
                f"Eliminados {len(all_ids)} elementos de la colección ")
        else:
            print(f"La colección ya está vacía.")

    def insert_data(self, array_data):
        try:
            for doc in array_data:
                self.collection.add(
                    documents=[doc["doc_content"]],
                    metadatas=[{"doc_name": doc["doc_name"]}],
                    ids=[str(uuid.uuid4())]
                )
        except Exception as e:
            print("Error:", e)

    def search_documents(self, document_name, document_section, full_text):
        try:
            finall_data = []
            # Si el usuario escribe el nombre del documento y la sección.
            if (document_name != False and document_section != False):
                results = self.collection.query(
                    query_texts=document_section,
                    where={"doc_name": str(document_name)},
                    n_results=20
                )
            # Si el usuario escribe solamente el nombre del documento
            elif document_name != False and document_section == False:
                results = self.collection.query(
                    query_texts=full_text,
                    where={"doc_name": document_name},
                    n_results=20
                )
            # Si el usuario escribe solamente la sección de los documentos
            elif document_name == False and document_section != False:
                results = self.collection.query(
                    query_texts=document_section,
                    n_results=20
                )
            # Si el ususrio no especifica la busqueda, se hace una búsqueda general
            else:
                results = self.collection.query(
                    query_texts=full_text, n_results=20)

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
