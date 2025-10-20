#!/usr/bin/env python3
"""
Build FAISS Vector Database from Knowledge Base
Uses lightweight multilingual embedding model
"""

import json
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss

class VectorDBBuilder:
    def __init__(self, knowledge_base_path: str, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize vector DB builder

        Args:
            knowledge_base_path: Path to knowledge_base.json
            model_name: Sentence transformer model name (default: multilingual-MiniLM for KO/EN support)
        """
        self.kb_path = Path(knowledge_base_path)
        self.model_name = model_name
        self.model = None
        self.documents = []
        self.embeddings = None
        self.index = None

    def load_knowledge_base(self):
        """Load knowledge base documents"""
        print(f"Loading knowledge base from: {self.kb_path}")
        with open(self.kb_path, 'r', encoding='utf-8') as f:
            self.documents = json.load(f)
        print(f"  Loaded {len(self.documents)} documents")

    def load_embedding_model(self):
        """Load sentence transformer model"""
        print(f"\nLoading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print(f"  Model loaded successfully")
        print(f"  Embedding dimension: {self.model.get_sentence_embedding_dimension()}")

    def create_embeddings(self):
        """Create embeddings for all documents"""
        print("\nCreating embeddings for documents...")

        # Extract content from documents
        texts = [doc['content'] for doc in self.documents]

        # Generate embeddings
        self.embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization for cosine similarity
        )

        print(f"  Created embeddings: shape {self.embeddings.shape}")

    def build_faiss_index(self):
        """Build FAISS index for similarity search"""
        print("\nBuilding FAISS index...")

        dimension = self.embeddings.shape[1]

        # Use IndexFlatIP for inner product (cosine similarity with normalized vectors)
        self.index = faiss.IndexFlatIP(dimension)

        # Add embeddings to index
        self.index.add(self.embeddings.astype('float32'))

        print(f"  Index built with {self.index.ntotal} vectors")

    def save(self, output_dir: str):
        """Save vector DB to disk"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        index_file = output_path / "faiss_index.bin"
        faiss.write_index(self.index, str(index_file))
        print(f"\nFAISS index saved to: {index_file}")

        # Save documents metadata
        docs_file = output_path / "documents.pkl"
        with open(docs_file, 'wb') as f:
            pickle.dump(self.documents, f)
        print(f"Documents metadata saved to: {docs_file}")

        # Save config
        config = {
            "model_name": self.model_name,
            "num_documents": len(self.documents),
            "embedding_dim": self.embeddings.shape[1]
        }
        config_file = output_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Config saved to: {config_file}")

    def test_search(self, query: str, k: int = 3):
        """Test the vector DB with a sample query"""
        print(f"\n=== Testing Search ===")
        print(f"Query: {query}")

        # Encode query
        query_embedding = self.model.encode([query], normalize_embeddings=True)

        # Search
        distances, indices = self.index.search(query_embedding.astype('float32'), k)

        print(f"\nTop {k} results:")
        for i, (idx, score) in enumerate(zip(indices[0], distances[0])):
            doc = self.documents[idx]
            print(f"\n{i+1}. [Score: {score:.4f}] [{doc['metadata']['type']}]")
            print(f"   {doc['content'][:150]}...")

    def build_all(self, output_dir: str):
        """Build complete vector database"""
        self.load_knowledge_base()
        self.load_embedding_model()
        self.create_embeddings()
        self.build_faiss_index()
        self.save(output_dir)


def main():
    # Paths
    kb_path = "/home/i0179/Realitylab-site/ai_server/knowledge_base.json"
    output_dir = "/home/i0179/Realitylab-site/ai_server/vector_db"

    # Build vector database
    builder = VectorDBBuilder(kb_path)
    builder.build_all(output_dir)

    # Test with sample queries
    print("\n" + "="*50)
    builder.test_search("연구실 위치가 어디인가요?", k=3)
    builder.test_search("김희원 교수님 이메일", k=2)
    builder.test_search("CVPR 2025 paper", k=2)

    print("\n" + "="*50)
    print("Vector database build complete!")


if __name__ == "__main__":
    main()
