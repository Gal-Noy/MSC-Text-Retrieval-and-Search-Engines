import os
import re
import zipfile
from collections import defaultdict
from typing import Dict, List, Tuple


class InvertedIndex:    
    def __init__(self):
        self.index: Dict[str, List[int]] = defaultdict(list)  # term -> list of internal doc IDs
        self.doc_id_map: Dict[int, str] = {}  # internal ID -> original DOCNO
        self.next_doc_id: int = 1  # counter for assigning internal IDs
    
    def parse_document(self, text: str) -> Tuple[str, List[str]]:
        """Extract DOCNO and terms from TEXT tags."""
        docno_match = re.search(r'<DOCNO>\s*(\S+)\s*</DOCNO>', text)
        if not docno_match:
            return None, []
        
        doc_id = docno_match.group(1).strip()
        text_content = re.findall(r'<TEXT>(.*?)</TEXT>', text, re.DOTALL)
        all_text = ' '.join(text_content)
        terms = all_text.split()
        
        return doc_id, terms
    
    def add_document(self, doc_text: str) -> None:
        """Parse and add a document to the index."""
        doc_id, terms = self.parse_document(doc_text)
        
        if not doc_id or not terms:
            return
        
        internal_id = self.next_doc_id
        self.doc_id_map[internal_id] = doc_id
        self.next_doc_id += 1
        
        unique_terms = set(terms)
        
        for term in unique_terms:
            self.index[term].append(internal_id)
    
    def build_from_directory(self, data_dir: str) -> None:
        """Build the index from all ZIP files in the directory."""
        zip_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.zip')])
        
        print(f"Found {len(zip_files)} ZIP files to process")
        
        for zip_file in zip_files:
            zip_path = os.path.join(data_dir, zip_file)
            print(f"Processing {zip_file}...")
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for file_name in zf.namelist():
                    with zf.open(file_name) as f:
                        content = f.read().decode('utf-8', errors='ignore')
                    
                    # Split file content into individual documents
                    documents = re.split(r'<DOC>', content)
                    
                    for doc in documents:
                        if doc.strip():
                            if '</DOC>' not in doc:
                                doc = doc + '</DOC>'
                            doc = '<DOC>' + doc
                            self.add_document(doc)
            
            print(f"  Completed {zip_file} - Total documents: {len(self.doc_id_map)}")
        
        print(f"\nIndex construction complete!")
        print(f"Total documents indexed: {len(self.doc_id_map)}")
        print(f"Total unique terms: {len(self.index)}")
    
    def get_posting_list(self, term: str) -> List[int]:
        """Return posting list for a term."""
        return self.index.get(term, [])
    
    def get_original_doc_id(self, internal_id: int) -> str:
        """Convert internal ID to original DOCNO."""
        return self.doc_id_map.get(internal_id, "")
