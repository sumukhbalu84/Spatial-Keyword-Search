# Spatial Keyword Search

This project implements **TKQN (Top-k Nearest Neighbor Queries)** using the **POWER Algorithm** for efficient **spatial-keyword queries**.  
It supports **positive and negative keyword filtering** using a **Quadtree + Inverted Index (TEQ Index).**  

## Features
- **Supports Positive & Negative Spatial-Keyword Queries**
- **Efficient Quadtree-Based Spatial Indexing**
- **Keyword-Based Filtering with Inverted Index**
- **Haversine Distance for Accurate Spatial Queries**
- **Top-K Ranking Using POWER Algorithm**
- **Verifiable Query Results with Sample Tweet Output**

## Step 1: Dataset Loader
The `Dataset_Loader.py` script **loads and normalizes tweets** from the U-ASK dataset.  
It ensures **cleaned and tokenized** data is inserted into the indexing structure.

## Step 2: TEQ Index (Spatial + Keyword Indexing)
- **Quadtree-based spatial partitioning** stores tweet locations efficiently.
- **Inverted Index** maps keywords to tweet IDs for fast lookup.
- **Two-pass indexing approach** inserts location and text separately.

## Step 3: Query Execution with POWER Algorithm
The `run_queries.py` script executes **various test queries**, including:  
- **Basic Keyword Queries** (e.g., "food", "sports")  
- **Spatial Queries** (e.g., tweets near New York, LA)  
- **Combined Spatial + Keyword Queries**  
- **Negative Keyword Queries** (e.g., food tweets **excluding** “burgers”)  

### **How to Run Queries**
Clone the repository and install dependencies:
```bash
git clone https://github.com/YOUR_USERNAME/Spatial-Keyword-Search.git
cd Spatial-Keyword-Search
pip install pandas
```

Run query tests:
```bash
python3 run_queries.py
```

### **Example Output**
```
Running Query: Food tweets in NYC excluding 'burgers'
  - Searching for tweets near (40.7128, -74.006) with keywords {'food'} excluding {'burgers'}
  - 1001 tweets passed both filters.
 Top-5 Results: [608597, 346917, 1919226, 1659298, 1664504]

Verifying sample tweets...
Tweet ID: 608597, Location: (25.27345668, 51.49714899), Keywords: {'craving', 'finally', 'food', 'al'}
Tweet ID: 346917, Location: (25.25811788, 51.48728551), Keywords: {'lunch', 'driver', 'heavy', 'parang', 'food', 'rooti'}
Sample verification complete.
```
All results exclude 'burgers' as expected.
