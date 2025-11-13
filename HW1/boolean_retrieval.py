from typing import List
from inverted_index import InvertedIndex


class BooleanRetrieval:
    """Boolean query processor using RPN."""
    
    def __init__(self, inv_index: InvertedIndex):
        self.inv_index = inv_index
        self.all_docs = sorted(list(self.inv_index.doc_id_map.keys()))
    
    def intersect(self, p1: List[int], p2: List[int]) -> List[int]:
        """Intersect two sorted posting lists."""
        result = []
        i, j = 0, 0
        
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                result.append(p1[i])
                i += 1
                j += 1
            elif p1[i] < p2[j]:
                i += 1
            else:
                j += 1
        
        return result
    
    def union(self, p1: List[int], p2: List[int]) -> List[int]:
        """Union two sorted posting lists."""
        result = []
        i, j = 0, 0
        
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                result.append(p1[i])
                i += 1
                j += 1
            elif p1[i] < p2[j]:
                result.append(p1[i])
                i += 1
            else:
                result.append(p2[j])
                j += 1
        
        while i < len(p1):
            result.append(p1[i])
            i += 1
        
        while j < len(p2):
            result.append(p2[j])
            j += 1
        
        return result
    
    def negate(self, p1: List[int], p2: List[int]) -> List[int]:
        """Subtract p2 from p1 (AND NOT operation)."""
        result = []
        i, j = 0, 0
        
        while i < len(p1):
            if j >= len(p2):
                result.extend(p1[i:])
                break
            
            if p1[i] < p2[j]:
                result.append(p1[i])
                i += 1
            elif p1[i] == p2[j]:
                i += 1
                j += 1
            else:
                j += 1
        
        return result
    
    def retrieve(self, query: str) -> List[str]:
        """Retrieve original document IDs for a query."""
        tokens = query.strip().split()
        stack: List[List[int]] = []
        
        for token in tokens:
            if token == 'AND':
                if len(stack) < 2:
                    return []
                p2 = stack.pop()
                p1 = stack.pop()
                if len(p1) > len(p2): # process shorter list first
                    p1, p2 = p2, p1
                stack.append(self.intersect(p1, p2))
                
            elif token == 'OR':
                if len(stack) < 2:
                    return []
                p2 = stack.pop()
                p1 = stack.pop()
                stack.append(self.union(p1, p2))
                
            elif token == 'NOT':
                if len(stack) < 1:
                    return []
                p2 = stack.pop()
                p1 = stack.pop() if stack else self.all_docs
                stack.append(self.negate(p1, p2))
                    
            else:
                stack.append(self.inv_index.get_posting_list(token))
        
        if len(stack) != 1:
            return []
        
        return [self.inv_index.get_original_doc_id(iid) for iid in stack[0]]
