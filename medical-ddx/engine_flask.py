import os
import pickle
import hashlib
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpointEmbeddings, HuggingFaceEmbeddings
from dotenv import load_dotenv
import chromadb
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DATA_PATH = "./data"
COLLECTION_NAME = "medical_docs"
EMBEDDINGS_CACHE_FILE = "./embeddings_cache.pkl"

class RAG_Engine:
    def __init__(self):
        """Initialize the RAG Engine with embeddings, LLM, and vector database"""
        try:
            # Initialize embeddings model with fallback
            try:
                # Try API-based embeddings first (no local download)
                self.embedding_model = HuggingFaceEndpointEmbeddings(
                    model="sentence-transformers/all-MiniLM-L6-v2",
                    huggingfacehub_api_token=os.getenv("HF_TOKEN")
                )
                logger.info("HuggingFace API embedding model initialized successfully")
                self.use_api_embeddings = True
            except Exception as api_error:
                logger.warning(f"API embeddings failed: {api_error}")
                logger.info("Falling back to local embeddings...")
                # Fallback to local embeddings
                self.embedding_model = HuggingFaceEmbeddings(
                    model_name="all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
                logger.info("Local embedding model initialized successfully")
                self.use_api_embeddings = False
            
            # Initialize LLM with better context management
            self.llm = ChatGroq(
                model_name="llama3-8b-8192",  # Changed to model with larger context
                api_key=GROQ_API_KEY,
                temperature=0.1,
                max_tokens=1500  # Limit response length
            )
            logger.info("LLM initialized successfully")
            
            # Initialize ChromaDB and check if data already exists
            self.client = chromadb.Client()
            
            # Try to get existing collection first
            try:
                self.collection = self.client.get_collection(name=COLLECTION_NAME)
                existing_count = self.collection.count()
                if existing_count > 0:
                    logger.info(f"Found existing collection with {existing_count} documents - skipping data loading")
                else:
                    logger.info("Collection exists but is empty - loading data")
                    self.load_and_embed_data()
            except Exception as e:
                # Collection doesn't exist, create it and load data
                logger.info(f"Collection not found ({e}), creating new collection and loading data")
                try:
                    self.collection = self.client.create_collection(name=COLLECTION_NAME)
                    self.load_and_embed_data()
                except Exception as create_error:
                    logger.error(f"Failed to create collection: {create_error}")
                    # Try to delete and recreate if creation fails
                    try:
                        self.client.delete_collection(name=COLLECTION_NAME)
                    except:
                        pass
                    self.collection = self.client.create_collection(name=COLLECTION_NAME)
                    self.load_and_embed_data()
                
        except Exception as e:
            logger.error(f"Error initializing RAG Engine: {e}")
            raise

    def chunk_text(self, text, max_chunk_size=8000, overlap=500):
        """Split text into larger chunks to reduce total number of documents"""
        # For smaller texts, don't chunk at all
        if len(text) <= max_chunk_size:
            return [text]
            
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + max_chunk_size, text_length)
            
            # Try to break at natural boundaries
            if end < text_length:
                # Look for section breaks first (double newlines)
                last_section = text.rfind('\n\n', start, end)
                # Then sentence endings
                last_period = text.rfind('.', start, end)
                # Finally single newlines
                last_newline = text.rfind('\n', start, end)
                
                # Use the best boundary found
                if last_section > start + max_chunk_size * 0.6:
                    end = last_section + 2
                elif last_period > start + max_chunk_size * 0.7:
                    end = last_period + 1
                elif last_newline > start + max_chunk_size * 0.8:
                    end = last_newline + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = max(start + 1, end - overlap)
        
        return chunks

    def get_data_hash(self):
        """Generate a hash of all data files to check if they've changed"""
        hasher = hashlib.md5()
        if not os.path.exists(DATA_PATH):
            return None
        
        file_hashes = []
        for filename in sorted(os.listdir(DATA_PATH)):
            if filename.endswith(".txt"):
                file_path = os.path.join(DATA_PATH, filename)
                with open(file_path, 'rb') as f:
                    file_hashes.append(hashlib.md5(f.read()).hexdigest())
        
        hasher.update(''.join(file_hashes).encode())
        return hasher.hexdigest()

    def load_cached_embeddings(self):
        """Load cached embeddings if they exist and data hasn't changed"""
        if not os.path.exists(EMBEDDINGS_CACHE_FILE):
            return None
            
        try:
            with open(EMBEDDINGS_CACHE_FILE, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Check if data has changed
            current_hash = self.get_data_hash()
            if cache_data.get('data_hash') == current_hash:
                logger.info("Loading embeddings from cache...")
                return cache_data
            else:
                logger.info("Data files have changed, cache is invalid")
                return None
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
            return None

    def save_embeddings_cache(self, documents, ids, metadatas, embeddings):
        """Save embeddings to cache"""
        try:
            cache_data = {
                'data_hash': self.get_data_hash(),
                'documents': documents,
                'ids': ids,
                'metadatas': metadatas,
                'embeddings': embeddings
            }
            with open(EMBEDDINGS_CACHE_FILE, 'wb') as f:
                pickle.dump(cache_data, f)
            logger.info("Embeddings saved to cache")
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")

    def load_and_embed_data(self):
        """Load medical documents and embed them in the vector database"""
        try:
            # Try to load from cache first
            cached_data = self.load_cached_embeddings()
            if cached_data:
                logger.info(f"Using cached embeddings for {len(cached_data['documents'])} documents")
                self.collection.add(
                    embeddings=cached_data['embeddings'],
                    documents=cached_data['documents'],
                    ids=cached_data['ids'],
                    metadatas=cached_data['metadatas']
                )
                return

            logger.info("Loading and embedding medical data...")
            documents = []
            ids = []
            metadatas = []
            
            if not os.path.exists(DATA_PATH):
                logger.error(f"Data path {DATA_PATH} does not exist")
                return
            
            doc_counter = 0
            for filename in os.listdir(DATA_PATH):
                if filename.endswith(".txt"):
                    file_path = os.path.join(DATA_PATH, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            if content.strip():  # Only add non-empty files
                                # Extract disease name from filename
                                disease_name = filename.replace('.txt', '').replace('_', ' ').title()
                                
                                # Chunk the document to avoid context length issues
                                chunks = self.chunk_text(content)
                                
                                for chunk_idx, chunk in enumerate(chunks):
                                    documents.append(chunk)
                                    ids.append(f"doc_{doc_counter}_chunk_{chunk_idx}")
                                    metadatas.append({
                                        'filename': filename,
                                        'disease': disease_name,
                                        'doc_type': 'medical_guide',
                                        'chunk_index': chunk_idx,
                                        'total_chunks': len(chunks)
                                    })
                                    doc_counter += 1
                                
                                logger.info(f"Processed {filename}: {len(chunks)} chunks")
                                
                    except Exception as e:
                        logger.warning(f"Error reading file {filename}: {e}")
                        continue
            
            if not documents:
                logger.warning("No documents found to embed")
                return
            
            # Generate embeddings and add to collection in batches optimized for the embedding type
            embedding_type = "API" if self.use_api_embeddings else "Local"
            logger.info(f"Generating embeddings for {len(documents)} document chunks using {embedding_type} embeddings...")
            
            # Set batch sizes based on embedding type - optimized for speed
            if self.use_api_embeddings:
                batch_size = 50  # Much larger batch size for API calls
                add_batch_size = 200  # Larger batch size for adding to ChromaDB
            else:
                batch_size = 100  # Larger batch size for local processing
                add_batch_size = 200  # Larger batch size for adding to ChromaDB
            
            all_embeddings = []
            
            # Generate all embeddings first in larger batches
            logger.info(f"Processing {len(documents)} documents in {(len(documents)-1)//batch_size + 1} batches...")
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i + batch_size]
                try:
                    batch_embeddings = self.embedding_model.embed_documents(batch_docs)
                    all_embeddings.extend(batch_embeddings)
                    logger.info(f"✅ Processed embedding batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1} ({len(batch_docs)} docs)")
                except Exception as e:
                    logger.error(f"❌ Error in embedding batch {i//batch_size + 1}: {e}")
                    # Add dummy embeddings to maintain consistency
                    dummy_embedding = [0.0] * 384  # Standard dimension for all-MiniLM-L6-v2
                    all_embeddings.extend([dummy_embedding] * len(batch_docs))
            
            # Save to cache for future use
            self.save_embeddings_cache(documents, ids, metadatas, all_embeddings)
            
            # Add to collection in batches
            logger.info(f"Adding {len(documents)} documents to ChromaDB collection...")
            for i in range(0, len(documents), add_batch_size):
                batch_docs = documents[i:i + add_batch_size]
                batch_ids = ids[i:i + add_batch_size]
                batch_metadatas = metadatas[i:i + add_batch_size]
                batch_embeddings = all_embeddings[i:i + add_batch_size]
                
                try:
                    self.collection.add(
                        embeddings=batch_embeddings,
                        documents=batch_docs,
                        ids=batch_ids,
                        metadatas=batch_metadatas
                    )
                    logger.info(f"✅ Added batch {i//add_batch_size + 1}/{(len(documents)-1)//add_batch_size + 1} to collection")
                except Exception as e:
                    logger.error(f"❌ Error adding batch to collection: {e}")
            
            logger.info(f"Successfully loaded {len(documents)} document chunks into the collection")
            
        except Exception as e:
            logger.error(f"Error loading and embedding data: {e}")
            raise
    
    def truncate_context(self, context, max_length=6000):
        """Truncate context to fit within model limits while preserving structure"""
        if len(context) <= max_length:
            return context
        
        # Try to truncate at section boundaries
        sections = context.split('\n\n---\n\n')
        truncated_sections = []
        current_length = 0
        
        for section in sections:
            if current_length + len(section) + 10 <= max_length:  # +10 for separators
                truncated_sections.append(section)
                current_length += len(section) + 10
            else:
                # If we can fit part of this section
                remaining_space = max_length - current_length - 10
                if remaining_space > 500:  # Only add if meaningful amount of space
                    truncated_section = section[:remaining_space] + "..."
                    truncated_sections.append(truncated_section)
                break
        
        result = '\n\n---\n\n'.join(truncated_sections)
        logger.info(f"Context truncated from {len(context)} to {len(result)} characters")
        return result

    def query(self, user_symptoms):
        """Query the RAG system with user symptoms"""
        try:
            logger.info(f"Processing query: {user_symptoms[:100]}...")
            
            # Generate query embedding using API
            try:
                query_embedding = self.embedding_model.embed_query(user_symptoms)
            except Exception as e:
                logger.error(f"Error generating query embedding: {e}")
                return "Sorry, I'm having trouble processing your symptoms right now. Please try again later."
            
            # Search for relevant documents with more results since we're dealing with chunks
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=5,  # Get more chunks to ensure comprehensive coverage
                include=['documents', 'metadatas']
            )
            
            # Extract relevant documents and group by disease
            disease_docs = {}
            diseases_mentioned = set()
            
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    if results['metadatas'] and results['metadatas'][0][i]:
                        metadata = results['metadatas'][0][i]
                        disease = metadata.get('disease', 'Unknown')
                        diseases_mentioned.add(disease)
                        
                        if disease not in disease_docs:
                            disease_docs[disease] = []
                        disease_docs[disease].append(doc)
            
            # Combine documents by disease and truncate
            combined_docs = []
            for disease, docs in disease_docs.items():
                # Take first 2 chunks per disease to avoid too much repetition
                disease_content = '\n\n'.join(docs[:2])
                combined_docs.append(f"=== {disease} ===\n{disease_content}")
            
            # Join all disease information
            retrieved_context = '\n\n---\n\n'.join(combined_docs)
            
            # Truncate context to fit model limits
            retrieved_context = self.truncate_context(retrieved_context, max_length=8000)
            
            # Create more concise prompt
            prompt = f"""You are a medical AI assistant. Based on the medical information provided, analyze the symptoms and provide a differential diagnosis.

MEDICAL CONTEXT:
{retrieved_context}

PATIENT SYMPTOMS: {user_symptoms}

Provide:
1. Most likely diagnoses (ranked)
2. Key distinguishing features
3. Recommended next steps

Keep response concise but comprehensive. This is for educational purposes only."""

            # Get response from LLM
            llm_response = self.llm.invoke(input=prompt)
            
            # Add footer with disclaimer and diseases referenced
            response_content = llm_response.content
            
            if diseases_mentioned:
                diseases_list = ", ".join(sorted(diseases_mentioned))
                response_content += f"\n\n**Conditions referenced:** {diseases_list}"
            
            response_content += "\n\n**⚠️ DISCLAIMER:** Educational purposes only. Consult healthcare professionals for actual diagnosis."
            
            logger.info("Query processed successfully")
            return response_content
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            if "context_length_exceeded" in str(e) or "reduce the length" in str(e):
                return "The symptom description is too detailed for processing. Please try with a shorter, more focused description of the main symptoms."
            return f"I apologize, but I encountered an error while analyzing your symptoms: {str(e)}. Please try again or consult with a healthcare professional."

def get_engine():
    """Factory function to create RAG Engine instance"""
    return RAG_Engine()
