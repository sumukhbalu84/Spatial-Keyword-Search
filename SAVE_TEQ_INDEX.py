from teq_index import TEQIndex
from Power import execute_power_tkqn
from Dataset_Loader import load_tweet_dataset
import pickle
import os

# Load dataset  
DATASET_PATH = "/Users/shreyasbattula/Downloads/U-ask_data/"  ##INSERT YOUR DATASET PATH HERE
for filename in sorted(os.listdir(DATASET_PATH)):
    df = load_tweet_dataset(DATASET_PATH+filename)

    # Define TEQ Index
    boundary = TEQIndex.get_dynamic_boundary(df)
    teq_index = TEQIndex(boundary)

    # Insert tweets into TEQ Index (Two-Pass Method)
    print("\nBuilding TEQ Index...")
    for _, row in df.iterrows():
        teq_index.insert_location(row.id, row.longitude, row.latitude)

    for _, row in df.iterrows():
        teq_index.insert_text(row.id, row.keywords)

    print(f"\nTEQ Index Built Successfully for {filename}!")

    ## SAVE TEQ INDEX TO A FILE 

    with open(f"./INDEXES/teq_index_{filename}.pkl", "wb") as f:
        pickle.dump(teq_index, f)
    print(f"\nTEQ Index Saved Successfully for {filename}!")
