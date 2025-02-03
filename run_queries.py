from teq_index import TEQIndex
from Power import execute_power_tkqn
from Dataset_Loader import load_tweet_dataset

# Load dataset
DATASET_PATH = "/Users/sumukhbalu/Documents/UCR/Quarter-2/Spatial Computing/Project/U-ask_data/tweet2000000"  # Update this with the actual dataset path
df = load_tweet_dataset(DATASET_PATH)

# Define TEQ Index
boundary = TEQIndex.get_dynamic_boundary(df)
teq_index = TEQIndex(boundary)

# Insert tweets into TEQ Index (Two-Pass Method)
print("\nBuilding TEQ Index...")
for row in df.itertuples(index=False):
    teq_index.insert_location(row.id, row.longitude, row.latitude)

for row in df.itertuples(index=False):
    teq_index.insert_text(row.id, row.keywords)

print("\nTEQ Index Built Successfully!")

# Define test queries
query_tests = [
    # Basic Keyword Queries
    {"query_location": None, "query_keywords": {"gourmet", "burgers"}, "k": 5, "description": "Food-related tweets"},
    {"query_location": None, "query_keywords": {"stadiums", "football"}, "k": 5, "description": "Sports-related tweets"},
    {"query_location": None, "query_keywords": {"wanna", "party", "lights"}, "k": 5, "description": "Nightlife-related tweets"},

    # Spatial Queries
    {"query_location": (40.7128, -74.0060), "query_keywords": None, "k": 5, "description": "Tweets near New York City"},
    {"query_location": (34.0522, -118.2437), "query_keywords": None, "k": 5, "description": "Tweets near Los Angeles"},
    {"query_location": (51.5074, -0.1278), "query_keywords": None, "k": 5, "description": "Tweets near London"},

    # Combined Spatial & Keyword Queries
    {"query_location": (40.7128, -74.0060), "query_keywords": {"gourmet", "burgers", "pizza"}, "k": 5, "description": "Food tweets near NYC"},
    {"query_location": (34.0522, -118.2437), "query_keywords": {"football", "stadiums", "team"}, "k": 5, "description": "Sports tweets near LA"},
    {"query_location": (36.1699, -115.1398), "query_keywords": {"party", "night", "lights"}, "k": 5, "description": "Nightlife tweets near Las Vegas"},

    # Edge Cases
    {"query_location": None, "query_keywords": {"heartburn"}, "k": 5, "description": "Rare keyword search"},
    {"query_location": (0, 0), "query_keywords": None, "k": 5, "description": "Tweets in empty ocean region"},
    {"query_location": None, "query_keywords": {"today", "now", "life"}, "k": 5, "description": "Common words search"},
]

# Run test queries
for i, test in enumerate(query_tests):
    print(f"\nRunning Query {i+1}: {test['description']}")

    query_location = test["query_location"]
    query_keywords = test["query_keywords"]
    k = test["k"]

    if query_location and query_keywords:
        print(f"  - Searching for tweets near {query_location} with keywords {query_keywords}")
    elif query_location:
        print(f"  - Searching for tweets near {query_location}")
    elif query_keywords:
        print(f"  - Searching for tweets containing {query_keywords}")

    # Execute POWER Query
    top_k_results = execute_power_tkqn(teq_index, query_location, query_keywords, k)

    print(f" Top-{k} Results: {top_k_results}")