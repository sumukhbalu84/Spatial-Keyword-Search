from Dataset_Loader import load_tweet_dataset

# Step 1: Load the dataset
DATASET_PATH = "path_to_datasets/tweet2M"  # UPDATE this with your dataset path

print(f"Loading dataset from: {DATASET_PATH} ...")
df = load_tweet_dataset(DATASET_PATH)

# Print dataset summary
print("\n Dataset Loaded Successfully!")
print(f"Total Entries: {df.shape[0]}")
print(df.head())  # Show first few rows