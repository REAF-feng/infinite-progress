#!/usr/bin/env python3
"""
Reset ChromaDB Collection Script
This script clears the existing collection and forces reloading with the new chunking strategy.
"""

import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

COLLECTION_NAME = "medical_docs"

def reset_collection():
    """Reset the ChromaDB collection to force reindexing with new chunking"""
    try:
        print("🔄 Resetting ChromaDB collection...")
        
        # Initialize ChromaDB client
        client = chromadb.Client()
        
        # Try to delete existing collection
        try:
            client.delete_collection(name=COLLECTION_NAME)
            print(f"✅ Deleted existing collection: {COLLECTION_NAME}")
        except Exception as e:
            print(f"ℹ️  Collection {COLLECTION_NAME} doesn't exist or already deleted: {e}")
        
        # Create new collection
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        print(f"✅ Created new collection: {COLLECTION_NAME}")
        print(f"📊 Collection document count: {collection.count()}")
        
        print("\n🎉 Collection reset successfully!")
        print("💡 The medical documents will be reindexed with improved chunking when you next run the application.")
        
    except Exception as e:
        print(f"❌ Error resetting collection: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🏥 Medical Diagnosis Assistant - Database Reset")
    print("=" * 50)
    print("This will clear the existing medical document index")
    print("and force reloading with improved text chunking.")
    print("=" * 50)
    
    response = input("Do you want to continue? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        reset_collection()
    else:
        print("❌ Operation cancelled.")
