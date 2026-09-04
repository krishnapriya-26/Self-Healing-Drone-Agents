from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class RAGAgent:
    """
    Retrieval-Augmented Generation agent for the
    Self-Healing Multi-Agent Drone Operations Platform.

    The agent:
    1. Reads drone failure knowledge from the knowledge folder.
    2. Converts the knowledge into embeddings.
    3. Stores the embeddings in a FAISS vector database.
    4. Searches the knowledge base using a drone diagnosis.
    """

    def __init__(self):

        # -------------------------------------------------
        # Knowledge directory
        # -------------------------------------------------

        self.knowledge_dir = Path("knowledge")

        # -------------------------------------------------
        # Load embedding model
        # -------------------------------------------------

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # -------------------------------------------------
        # Load knowledge documents
        # -------------------------------------------------

        self.documents = self._load_documents()

        # -------------------------------------------------
        # Create vector database
        # -------------------------------------------------

        if self.documents:

            self.vectorstore = FAISS.from_documents(
                self.documents,
                self.embeddings
            )

        else:

            self.vectorstore = None


    # =====================================================
    # LOAD KNOWLEDGE
    # =====================================================

    def _load_documents(self):

        documents = []

        # Check whether knowledge folder exists

        if not self.knowledge_dir.exists():

            print(
                "WARNING: knowledge folder not found."
            )

            return documents


        # Read all .txt files

        for file_path in self.knowledge_dir.glob("*.txt"):

            try:

                text = file_path.read_text(
                    encoding="utf-8"
                )

                if text.strip():

                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": file_path.name
                            }
                        )
                    )

            except Exception as error:

                print(
                    f"Could not read {file_path}: {error}"
                )


        return documents


    # =====================================================
    # RETRIEVE KNOWLEDGE
    # =====================================================

    def retrieve(self, query):

        """
        Retrieve the most relevant drone failure
        procedures from the knowledge base.

        query can be either:
            - a string
            - a dictionary containing diagnosis/severity
        """

        # -------------------------------------------------
        # IMPORTANT FIX
        # -------------------------------------------------
        # HuggingFace embeddings require TEXT.
        # Our diagnosis agent may return a dictionary.
        # Convert the dictionary into a readable string.
        # -------------------------------------------------

        if isinstance(query, dict):

            diagnosis = query.get(
                "diagnosis",
                ""
            )

            severity = query.get(
                "severity",
                ""
            )

            query = (
                f"Drone diagnosis: {diagnosis}. "
                f"Severity: {severity}."
            )


        # Make sure query is always a string

        query = str(query)


        # -------------------------------------------------
        # No vector database
        # -------------------------------------------------

        if self.vectorstore is None:

            return []


        # -------------------------------------------------
        # Perform similarity search
        # -------------------------------------------------

        try:

            results = self.vectorstore.similarity_search(
                query,
                k=3
            )

        except Exception as error:

            print(
                f"RAG search error: {error}"
            )

            return []


        # -------------------------------------------------
        # Return useful text instead of raw objects
        # -------------------------------------------------

        knowledge = []

        for document in results:

            knowledge.append({

                "content":
                    document.page_content,

                "source":
                    document.metadata.get(
                        "source",
                        "unknown"
                    )

            })


        return knowledge


    # =====================================================
    # SEARCH ALIAS
    # =====================================================

    def search(self, query):

        """
        Alternative method name for compatibility
        with the workflow.
        """

        return self.retrieve(query)


    # =====================================================
    # QUERY ALIAS
    # =====================================================

    def query(self, query):

        """
        Alternative query method.
        """

        return self.retrieve(query)


# =========================================================
# TEST RAG AGENT DIRECTLY
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("        DRONE RAG AGENT TEST")
    print("=" * 60)

    rag = RAGAgent()

    test_query = {
        "diagnosis": "GPS failure",
        "severity": "HIGH"
    }

    results = rag.retrieve(
        test_query
    )

    print()
    print("Query:")
    print(test_query)

    print()
    print("Retrieved Knowledge:")
    print("-" * 60)

    if results:

        for index, result in enumerate(
            results,
            start=1
        ):

            print()
            print(
                f"Result {index}"
            )

            print(
                "Source:",
                result["source"]
            )

            print(
                result["content"]
            )

    else:

        print(
            "No knowledge retrieved."
        )

    print()
    print("=" * 60)