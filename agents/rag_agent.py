from pathlib import Path
import re


class RAGAgent:
    """
    Lightweight Retrieval-Augmented Generation agent.

    Retrieves relevant drone failure knowledge from
    local knowledge files using keyword-based similarity.

    This version is optimized for low-memory cloud deployment.
    """

    def __init__(self):

        self.knowledge_dir = Path("knowledge")
        self.documents = self._load_documents()

        print(
            f"RAG knowledge base loaded: {len(self.documents)} documents"
        )

    # =====================================================
    # LOAD KNOWLEDGE
    # =====================================================

    def _load_documents(self):

        documents = []

        if not self.knowledge_dir.exists():

            print("WARNING: knowledge folder not found.")

            return documents

        for file_path in self.knowledge_dir.glob("*.txt"):

            try:

                text = file_path.read_text(
                    encoding="utf-8"
                )

                if text.strip():

                    documents.append({
                        "content": text,
                        "source": file_path.name
                    })

            except Exception as error:

                print(
                    f"Could not read {file_path}: {error}"
                )

        return documents

    # =====================================================
    # TEXT PROCESSING
    # =====================================================

    def _keywords(self, text):

        words = re.findall(
            r"[a-zA-Z0-9]+",
            text.lower()
        )

        stop_words = {
            "the",
            "is",
            "a",
            "an",
            "and",
            "or",
            "of",
            "to",
            "in",
            "for",
            "with",
            "on",
            "may",
            "be",
            "can",
            "this",
            "that"
        }

        return {
            word
            for word in words
            if word not in stop_words
            and len(word) > 2
        }

    # =====================================================
    # RETRIEVE KNOWLEDGE
    # =====================================================

    def retrieve(self, query):

        """
        Retrieve the most relevant drone failure
        procedures from the knowledge base.
        """

        # Convert dictionary diagnosis to text

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

        query = str(query)

        if not self.documents:

            return []

        query_words = self._keywords(query)

        scored_documents = []

        for document in self.documents:

            document_words = self._keywords(
                document["content"]
            )

            # Count matching keywords

            matching_words = (
                query_words &
                document_words
            )

            score = len(matching_words)

            scored_documents.append(
                (
                    score,
                    document
                )
            )

        # Highest relevance first

        scored_documents.sort(
            key=lambda item: item[0],
            reverse=True
        )

        # Return top 3 relevant documents

        results = []

        for score, document in scored_documents[:3]:

            if score > 0:

                results.append({
                    "content": document["content"],
                    "source": document["source"],
                    "relevance_score": score
                })

        return results

    # =====================================================
    # SEARCH ALIAS
    # =====================================================

    def search(self, query):

        return self.retrieve(query)

    # =====================================================
    # QUERY ALIAS
    # =====================================================

    def query(self, query):

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

    results = rag.retrieve(test_query)

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
            print(f"Result {index}")

            print(
                "Source:",
                result["source"]
            )

            print(
                "Relevance:",
                result["relevance_score"]
            )

            print(
                result["content"]
            )

    else:

        print("No knowledge retrieved.")

    print()
    print("=" * 60)