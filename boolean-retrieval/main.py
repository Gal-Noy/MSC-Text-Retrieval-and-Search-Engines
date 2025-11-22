import os
import argparse
from inverted_index import InvertedIndex
from boolean_retrieval import BooleanRetrieval


def process_boolean_queries(inv_index: InvertedIndex, queries_file: str, output_file: str):
    """Process boolean queries and write retrieved documents to output file."""
    print("\n" + "=" * 60)
    print("Boolean Retrieval")
    print("=" * 60)
    
    retrieval = BooleanRetrieval(inv_index)
    
    with open(queries_file, 'r') as f:
        queries = [line.strip() for line in f if line.strip()]
    
    with open(output_file, 'w') as f:
        for i, query in enumerate(queries, 1):
            print(f"Query {i}: {query}")
            results = retrieval.retrieve(query)
            print(f"  {len(results)} documents")
            f.write(' '.join(results) + '\n')
    
    print(f"Written to {output_file}")


def generate_collection_statistics(inv_index: InvertedIndex, output_file: str):
    """Generate collection statistics including term frequencies and analysis."""
    print("\n" + "=" * 60)
    print("Collection Statistics")
    print("=" * 60)
    
    term_freq = [(term, len(postings)) for term, postings in inv_index.index.items()]
    term_freq.sort(key=lambda x: x[1], reverse=True)
    
    top_10 = term_freq[:10]
    bottom_10 = term_freq[-10:]
    
    print("Top 10 highest DF:")
    for term, df in top_10:
        print(f"  {term}: {df}")
    
    print("\nTop 10 lowest DF:")
    for term, df in bottom_10:
        print(f"  {term}: {df}")
    
    print("\nFinding similar terms...")
    similar_terms = find_similar_terms(inv_index, term_freq)
    
    with open(output_file, 'w') as f:
        f.write("1. Top 10 terms with highest document frequency:\n")
        for term, df in top_10:
            f.write(f"   {term}: {df}\n")
        
        f.write("\n2. Top 10 terms with lowest document frequency:\n")
        for term, df in bottom_10:
            f.write(f"   {term}: {df}\n")
        
        f.write("\n3. Characteristics of high vs low DF terms:\n")
        f.write("   High DF terms are stopwords (the, of, in, a, and) appearing across most documents\n")
        f.write("   regardless of topic, carrying little semantic value. Low DF terms are rare words,\n")
        f.write("   often specific names or typos, appearing in very few documents. They are highly\n")
        f.write("   discriminative but may be too specific for general queries.\n")
        
        f.write("\n4. Two terms with similar DF appearing in same documents:\n")
        if similar_terms:
            term1, term2, df1, df2, shared_count, shared_docs = similar_terms
            f.write(f"   Term 1: '{term1}' (DF={df1})\n")
            f.write(f"   Term 2: '{term2}' (DF={df2})\n")
            f.write(f"   Shared documents: {shared_count}\n")
            f.write(f"   Example docs: {', '.join(shared_docs[:5])}\n")
            f.write(f"\n   Method: Searched mid-frequency terms (DF 50-200) with similar DF (within 5%)\n")
            f.write(f"   and high overlap (>80% shared documents). Such terms often represent related\n")
            f.write(f"   concepts, synonyms, or co-occurring phrases in specific contexts.\n")
    
    print(f"Written to {output_file}")


def find_similar_terms(inv_index: InvertedIndex, term_freq):
    """Find two terms with similar DF appearing in same documents."""
    mid_freq = [(t, df) for t, df in term_freq if 50 <= df <= 200]
    
    for i in range(len(mid_freq) - 1):
        term1, df1 = mid_freq[i]
        
        for j in range(i + 1, min(i + 50, len(mid_freq))):
            term2, df2 = mid_freq[j]
            
            if abs(df1 - df2) / max(df1, df2) > 0.05:
                continue
            
            p1 = set(inv_index.get_posting_list(term1))
            p2 = set(inv_index.get_posting_list(term2))
            shared = p1.intersection(p2)
            
            if len(shared) / min(len(p1), len(p2)) > 0.8 and len(shared) > 10:
                docs = [inv_index.get_original_doc_id(iid) for iid in list(shared)[:10]]
                return (term1, term2, df1, df2, len(shared), docs)
    
    return None


def main():
    parser = argparse.ArgumentParser(description='AP Collection IR System')
    parser.add_argument(
        '--data-dir',
        default=os.path.join(os.path.dirname(__file__), 'data'),
        help='Directory containing the document collection (default: data/)'
    )
    parser.add_argument(
        '--queries-file',
        default=os.path.join(os.path.dirname(__file__), 'BooleanQueries.txt'),
        help='File containing boolean queries (default: BooleanQueries.txt)'
    )
    parser.add_argument(
        '--retrieval-output',
        default='Part_2.txt',
        help='Output file for boolean retrieval results (default: Part_2.txt)'
    )
    parser.add_argument(
        '--statistics-output',
        default='Part_3.txt',
        help='Output file for collection statistics (default: Part_3.txt)'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.data_dir):
        print(f"Error: Data directory not found: {args.data_dir}")
        return
    
    if not os.path.exists(args.queries_file):
        print(f"Error: Queries file not found: {args.queries_file}")
        return
    
    print("=" * 60)
    print("AP Collection IR System")
    print("=" * 60)
    print("\nBuilding index...")
    
    inv_index = InvertedIndex()
    inv_index.build_from_directory(args.data_dir)
    
    process_boolean_queries(inv_index, args.queries_file, args.retrieval_output)
    generate_collection_statistics(inv_index, args.statistics_output)
    
    print("\n" + "=" * 60)
    print("Completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
