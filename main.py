from Dataset_Loader import load_tweet_dataset
from teq_index import TEQIndex, Boundary, Tweet

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