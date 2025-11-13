# Boolean Retrieval System

An information retrieval system that builds an inverted index from a document collection and performs boolean query retrieval.

## Usage

### Basic Usage

Run with default settings:

```bash
python main.py
```

### Command-Line Arguments

Customize the behavior with optional arguments:

```bash
python main.py [OPTIONS]
```

**Options:**

- `--data-dir PATH` - Directory containing the document collection (default: `data/`)
- `--queries-file PATH` - File containing boolean queries (default: `BooleanQueries.txt`)
- `--retrieval-output PATH` - Output file for retrieval results (default: `Part_2.txt`)
- `--statistics-output PATH` - Output file for collection statistics (default: `Part_3.txt`)

**Example:**

```bash
python main.py --data-dir /path/to/documents \
               --queries-file my_queries.txt \
               --retrieval-output results.txt \
               --statistics-output stats.txt
```

## Output Files

- **Retrieval Output**: Contains document IDs for each query (one line per query)
- **Statistics Output**: Includes term frequency analysis and collection characteristics

## Disclosure

This project was developed with assistance from Claude Sonnet 4.5.
