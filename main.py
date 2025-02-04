from Dataset_Loader import load_tweet_dataset
from teq_index import TEQIndex, Boundary, Tweet
from Power import execute_power_tkqn

# Step 1: Load the dataset
DATASET_PATH = "/Users/sumukhbalu/Documents/UCR/Quarter-2/Spatial Computing/Project/U-ask_data/tweet2000000"
print(f"Loading dataset from: {DATASET_PATH} ...")
df = load_tweet_dataset(DATASET_PATH)

# Step 2: Define the spatial boundary dynamically based on dataset
boundary = TEQIndex.get_dynamic_boundary(df)  # Dynamically determine the spatial extent
teq_index = TEQIndex(boundary)

# Step 3: First Pass – Insert Only Locations into the Quadtree
print("\n First Pass: Inserting Locations into TEQ (Spatial Indexing)...")
for row in df.itertuples(index=False):
    teq_index.insert_location(row.id, row.longitude, row.latitude)

# Step 4: Second Pass – Insert Keywords into the Inverted Index
print("\n Second Pass: Inserting Textual Data into TEQ (Keyword Indexing)...")
for row in df.itertuples(index=False):
    teq_index.insert_text(row.id, row.keywords)

print("\n TEQ Index Built Successfully!")

# Step 4: Execute POWER Query
query_location = (34.05, -118.25)  # Example: Los Angeles
query_keywords = {"earthquake", "damage"}  # Example: Disaster-related keywords
k = 5  # Get the top 5 most relevant tweets

print("\nRunning POWER TKQN Query...")
top_k_results = execute_power_tkqn(teq_index, query_location, query_keywords, k)

print(f"\nTop-{k} Most Relevant Tweets: {top_k_results}")

print("\nVerifying Top-k Results:\n")
for tweet_id in top_k_results:
    tweet = teq_index.tweet_store.get(tweet_id)  # Retrieve tweet details
    if tweet:
        print(f"Tweet ID: {tweet.id} | Location: ({tweet.y}, {tweet.x}) | Keywords: {tweet.keywords}")
    else:
        print(f"Tweet ID: {tweet_id} not found in index.")

# Check if the dataset has any tweets near Los Angeles
query_lat, query_lon = 34.05, -118.25  # Los Angeles

nearby_tweets = []
radius = 100  # Set an initial search radius of 100 km

for tweet in teq_index.tweet_store.values():
    distance = ((tweet.y - query_lat) ** 2 + (tweet.x - query_lon) ** 2) ** 0.5  # Approximate Euclidean distance
    if distance <= radius:
        nearby_tweets.append(tweet)

print(f"\nTotal Tweets Near Los Angeles (within {radius} km): {len(nearby_tweets)}")
for tweet in nearby_tweets[:10]:  # Print first 10 nearby tweets
    print(f"Tweet ID: {tweet.id} | Location: ({tweet.y}, {tweet.x}) | Keywords: {tweet.keywords}")