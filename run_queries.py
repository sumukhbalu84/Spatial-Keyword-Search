# from teq_index import TEQIndex
# from Dataset_Loader import load_tweet_dataset
from Power import execute_power_tkqn
import pickle
# # Load dataset
# DATASET_PATH = "/Users/sumukhbalu/Documents/UCR/Quarter-2/Spatial Computing/Project/U-ask_data/tweet2000000"
# df = load_tweet_dataset(DATASET_PATH)

# # Define TEQ Index
# boundary = TEQIndex.get_dynamic_boundary(df)
# teq_index = TEQIndex(boundary)

# # Insert tweets into TEQ Index (Two-Pass Method)
# print("\nBuilding TEQ Index...")
# for _, row in df.iterrows():
#     teq_index.insert_location(row.id, row.longitude, row.latitude)

# for _, row in df.iterrows():
#     teq_index.insert_text(row.id, row.keywords)

# print("\nTEQ Index Built Successfully!")

# ## SAVE TEQ INDEX TO A FILE 
# import pickle
# with open("teq_index.pkl", "wb") as f:
#     pickle.dump(teq_index, f)
## ALL THIS HAS BEEN DONE ALREADY IN THE SAVE_TEQ_INDEX.PY FILE

# Load TEQ Index from a file
with open("./INDEXES/teq_index_2M.pkl", "rb") as f:
    teq_index = pickle.load(f)

# Define test queries
query_tests = [
    {"query_location": None, "query_keywords": {"gourmet", "burgers"}, "k": 5, "description": "Food-related tweets"},
    {"query_location": None, "query_keywords": {"stadiums", "football"}, "k": 5, "description": "Sports-related tweets"},
    {"query_location": None, "query_keywords": {"wanna", "party", "lights"}, "k": 5, "description": "Nightlife-related tweets"},
    {"query_location": (40.7128, -74.0060), "query_keywords": None, "k": 5, "description": "Tweets near New York City"},
    {"query_location": (34.0522, -118.2437), "query_keywords": None, "k": 5, "description": "Tweets near Los Angeles"},
    {"query_location": (51.5074, -0.1278), "query_keywords": None, "k": 5, "description": "Tweets near London"},
    {"query_location": (40.7128, -74.0060), "query_keywords": {"gourmet", "burgers", "pizza"}, "k": 5, "description": "Food tweets near NYC"},
    {"query_location": (34.0522, -118.2437), "query_keywords": {"football", "stadiums", "team"}, "k": 5, "description": "Sports tweets near LA"},
    {"query_location": (36.1699, -115.1398), "query_keywords": {"party", "night", "lights"}, "k": 5, "description": "Nightlife tweets near Las Vegas"},
    {"query_location": None, "query_keywords": {"heartburn"}, "k": 5, "description": "Rare keyword search"},
    {"query_location": (0, 0), "query_keywords": None, "k": 5, "description": "Tweets in empty ocean region"},
    {"query_location": None, "query_keywords": {"today", "now", "life"}, "k": 5, "description": "Common words search"},
    {"query_location": (40.7128, -74.0060), "query_keywords": {"food"}, "exclude_keywords": {"burgers"}, "k": 5, "description": "Food tweets in NYC excluding 'burgers'"},
    {"query_location": (34.0522, -118.2437), "query_keywords": {"sports"}, "exclude_keywords": {"football"}, "k": 5, "description": "Sports tweets in LA excluding 'football'"},
    {"query_location": (36.1699, -115.1398), "query_keywords": {"party"}, "exclude_keywords": {"lights"}, "k": 5, "description": "Party tweets in Las Vegas excluding 'lights'"},
]

# Run test queries
for i, test in enumerate(query_tests):
    print(f"\nRunning Query {i+1}: {test['description']}")
    query_location = test.get("query_location")
    query_keywords = test.get("query_keywords")
    exclude_keywords = test.get("exclude_keywords", None)
    k = test["k"]

    print(f"  - Searching for tweets near {query_location} with keywords {query_keywords} excluding {exclude_keywords}")

    top_k_results = execute_power_tkqn(teq_index, query_location, query_keywords, exclude_keywords, k)

    print(f" Top-{k} Results: {top_k_results}")

    # Print 2 sample tweets for manual verification
    print("\nVerifying sample tweets...")
    sample_tweets = top_k_results[:2]  # Get first 2 tweets from results

    for tweet_id in sample_tweets:
        if tweet_id in teq_index.tweet_store:
            tweet = teq_index.tweet_store[tweet_id]
            print(f"Tweet ID: {tweet.id}, Location: ({tweet.y}, {tweet.x}), Keywords: {tweet.keywords}")
            if exclude_keywords:
                assert not (tweet.keywords & exclude_keywords), f"ERROR: Found excluded keyword in Tweet {tweet.id}!"

    print("Sample verification complete.\n")
