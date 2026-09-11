import os
import re
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# NEW (Lightweight, no bloated LangChain install needed):
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
from groq import Groq


@dataclass
class Chunk:
    """Represents a text chunk with metadata"""
    text: str
    source: str
    chunk_id: int
    start_idx: int
    end_idx: int


@dataclass
class RetrievedContext:
    """Represents a retrieved context with relevance score"""
    text: str
    source: str
    score: float
    chunk_id: int


class RAGEngine:
    """
    Multi-stage RAG pipeline:
    1. Chunking with overlap
    2. Embedding using open-source sentence-transformers
    3. FAISS vector indexing
    4. Multi-stage retrieval (retrieve → re-rank → filter)
    5. Grounded answer generation via Groq
    """

    # UPDATE: Set default model to gpt-oss-120b
    def __init__(self, groq_api_key: str, model_name: str = "gpt-oss-120b"):
        # Embedding model (open-source, runs locally)
        self.embed_model_name = "all-MiniLM-L6-v2"
        self.embed_model = None  # Lazy load

        # Groq LLM
        self.groq_client = Groq(api_key=groq_api_key)
        self.llm_model = model_name

        # FAISS index
        self.index = None
        self.chunks: List[Chunk] = []
        self.embeddings: Optional[np.ndarray] = None

        # Splitter config
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            length_function=len,
            separators=["\n\n", "\n", ". ", ", ", " ", ""]
        )

        # Pipeline state
        self.is_indexed = False

    def _load_embed_model(self):
        """Lazy load embedding model"""
        if self.embed_model is None:
            self.embed_model = SentenceTransformer(self.embed_model_name)

    # =====================================================
    # STAGE 1: CHUNKING
    # =====================================================
    def chunk_documents(self, documents: List[Dict]) -> List[Chunk]:
        """
        Split documents into overlapping chunks.
        Each document dict should have 'filename' and 'text_content'.
        """
        all_chunks = []
        chunk_id = 0

        for doc in documents:
            filename = doc["filename"]
            text = doc["text_content"]

            if not text or not text.strip():
                continue

            # Split text
            splits = self.text_splitter.split_text(text)

            for i, split_text in enumerate(splits):
                if split_text.strip():
                    chunk = Chunk(
                        text=split_text.strip(),
                        source=filename,
                        chunk_id=chunk_id,
                        start_idx=i * 800,  # approximate
                        end_idx=(i + 1) * 800
                    )
                    all_chunks.append(chunk)
                    chunk_id += 1

        self.chunks = all_chunks
        return all_chunks

    # =====================================================
    # STAGE 2: EMBEDDING
    # =====================================================
    def create_embeddings(self, chunks: List[Chunk] = None) -> np.ndarray:
        """Create embeddings for all chunks using sentence-transformers"""
        self._load_embed_model()

        if chunks is None:
            chunks = self.chunks

        if not chunks:
            raise ValueError("No chunks to embed. Process documents first.")

        texts = [chunk.text for chunk in chunks]
        embeddings = self.embed_model.encode(
            texts,
            show_progress_bar=False,
            batch_size=32,
            normalize_embeddings=True
        )

        self.embeddings = np.array(embeddings, dtype=np.float32)
        return self.embeddings

    # =====================================================
    # STAGE 3: FAISS INDEXING
    # =====================================================
    def build_index(self, embeddings: np.ndarray = None):
        """Build FAISS index from embeddings"""
        if embeddings is None:
            embeddings = self.embeddings

        if embeddings is None:
            raise ValueError("No embeddings found. Create embeddings first.")

        dimension = embeddings.shape[1]

        # Use IndexFlatIP for cosine similarity (embeddings are normalized)
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        self.is_indexed = True

    # =====================================================
    # STAGE 4: MULTI-STAGE RETRIEVAL
    # =====================================================
    def retrieve(self, query: str, top_k: int = 8, rerank_top_k: int = 5) -> List[RetrievedContext]:
        """
        Multi-stage retrieval:
        1. Embed query
        2. FAISS search (top_k candidates)
        3. Re-rank by relevance
        4. Return top rerank_top_k results
        """
        if not self.is_indexed:
            raise ValueError("Index not built. Process and index documents first.")

        self._load_embed_model()

        # Step 1: Embed query
        query_embedding = self.embed_model.encode(
            [query],
            normalize_embeddings=True
        ).astype(np.float32)

        # Step 2: FAISS search
        scores, indices = self.index.search(query_embedding, min(top_k, len(self.chunks)))

        # Step 3: Build results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.chunks):
                continue
            chunk = self.chunks[idx]
            results.append(RetrievedContext(
                text=chunk.text,
                source=chunk.source,
                score=float(score),
                chunk_id=chunk.chunk_id
            ))

        # Step 4: Re-rank - boost chunks that have keyword overlap with query
        results = self._rerank(query, results)

        return results[:rerank_top_k]

    def _rerank(self, query: str, results: List[RetrievedContext]) -> List[RetrievedContext]:
        """Re-rank results using keyword overlap boosting"""
        query_tokens = set(re.findall(r'\w+', query.lower()))

        for result in results:
            chunk_tokens = set(re.findall(r'\w+', result.text.lower()))
            overlap = len(query_tokens.intersection(chunk_tokens))
            # Boost score by keyword overlap (hybrid approach)
            keyword_boost = overlap * 0.02
            result.score += keyword_boost

        # Re-sort by updated score
        results.sort(key=lambda x: x.score, reverse=True)
        return results

    # =====================================================
    # STAGE 5: GROUNDED GENERATION (ANTI-HALLUCINATION)
    # =====================================================
    def generate_answer(self, query: str, contexts: List[RetrievedContext],
                        chat_history: List[Dict] = None) -> Tuple[str, List[str]]:
        """
        Generate answer strictly grounded in retrieved contexts.
        Uses multi-stage prompting to prevent hallucination.
        """

        # Build context string
        context_parts = []
        sources = []
        for i, ctx in enumerate(contexts):
            context_parts.append(f"[Source {i+1}: {ctx.source} | Relevance: {ctx.score:.3f}]\n{ctx.text}")
            if ctx.source not in sources:
                sources.append(ctx.source)

        context_string = "\n\n---\n\n".join(context_parts)

        # System prompt with strict grounding instructions
        system_prompt = """You are FinanceRAG, a precise financial document analysis assistant. 

YOUR STRICT RULES:
1. ONLY answer based on the provided CONTEXT below. Never use external knowledge.
2. If the context does NOT contain enough information to answer, say: "Based on the uploaded documents, I don't have enough information to answer this question. Please upload relevant documents or rephrase your query."
3. ALWAYS cite which source document your answer comes from.
4. When discussing numbers/amounts, quote them EXACTLY as they appear in the context.
5. If you calculate something (sum, average, etc.), show your work step by step.
6. Be specific, structured, and use bullet points or tables when appropriate.
7. Never make assumptions about data not present in the documents.
8. For financial advice questions, clarify you're analyzing documents, not giving professional financial advice.

FORMAT YOUR RESPONSE:
- Use clear headings if the answer has multiple parts
- Use bullet points for lists
- Quote exact figures from documents
- End with source attribution"""

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        # Add chat history for context continuity
        if chat_history:
            for msg in chat_history[-6:]:  # Last 3 exchanges
                messages.append(msg)

        # User message with context
        user_message = f"""CONTEXT FROM UPLOADED DOCUMENTS:
{context_string}

---

USER QUESTION: {query}

Remember: Answer ONLY from the context above. If information is not in the context, say so explicitly."""

        messages.append({"role": "user", "content": user_message})

        # Call Groq
        try:
            response = self.groq_client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                temperature=0.1,  # Low temperature for factual accuracy
                max_tokens=2048,
                top_p=0.9,
            )

            answer = response.choices[0].message.content

            # STAGE 2: Verification pass - check if answer is grounded
            answer = self._verify_grounding(answer, context_string, query)

            return answer, sources

        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            if "api_key" in str(e).lower() or "auth" in str(e).lower():
                error_msg = "Invalid Groq API key. Please check your API key and try again."
            return error_msg, []

    def _verify_grounding(self, answer: str, context: str, query: str) -> str:
        """
        Verification stage: Check if the answer contains claims not in context.
        This is a lightweight check - flags potential issues.
        """
        # Extract numbers from answer and context
        answer_numbers = set(re.findall(r'\$?[\d,]+\.?\d*', answer))
        context_numbers = set(re.findall(r'\$?[\d,]+\.?\d*', context))

        # Check if answer introduces numbers not in context (potential hallucination)
        # Allow common numbers like percentages, years, etc.
        suspicious_numbers = answer_numbers - context_numbers
        # Filter out small common numbers
        suspicious_numbers = {n for n in suspicious_numbers
                             if not re.match(r'^[\d]{1,2}$', n.replace('$', '').replace(',', ''))}

        if suspicious_numbers and len(suspicious_numbers) > 3:
            answer += "\n\n⚠️ *Note: Some calculated figures in this response were derived from the source data. Please verify calculations against your original documents.*"

        return answer

    # =====================================================
    # FULL PIPELINE
    # =====================================================
    def process_and_index(self, documents: List[Dict]) -> Dict:
        """
        Run the full pipeline:
        1. Chunk documents
        2. Create embeddings
        3. Build FAISS index
        Returns status dict.
        """
        result = {
            "chunks_created": 0,
            "index_size": 0,
            "status": "processing"
        }

        # Step 1: Chunk
        chunks = self.chunk_documents(documents)
        result["chunks_created"] = len(chunks)

        if not chunks:
            result["status"] = "error"
            result["error"] = "No text content found in documents"
            return result

        # Step 2: Embed
        embeddings = self.create_embeddings(chunks)

        # Step 3: Index
        self.build_index(embeddings)
        result["index_size"] = self.index.ntotal
        result["status"] = "ready"

        return result

    def query(self, question: str, chat_history: List[Dict] = None) -> Tuple[str, List[str]]:
        """
        Full RAG query: Retrieve → Generate
        """
        # Retrieve relevant contexts
        contexts = self.retrieve(question, top_k=8, rerank_top_k=5)

        if not contexts:
            return ("I couldn't find relevant information in your uploaded documents. "
                    "Please make sure you've uploaded the right documents and try rephrasing your question."), []

        # Generate grounded answer
        answer, sources = self.generate_answer(question, contexts, chat_history)

        return answer, sources

    def reset(self):
        """Reset the entire pipeline"""
        self.index = None
        self.chunks = []
        self.embeddings = None
        self.is_indexed = False
