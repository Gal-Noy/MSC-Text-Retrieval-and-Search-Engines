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

## Query Format

Boolean queries should be written one per line in the queries file. Supported operators:

- `AND` - Intersection of posting lists
- `OR` - Union of posting lists
- `NOT` - Complement of posting list

**Example queries:**

```
information AND retrieval
computer OR science
NOT obsolete
```

## Output Files

- **Retrieval Output**: Contains document IDs for each query (one line per query)
- **Statistics Output**: Includes term frequency analysis and collection characteristics
