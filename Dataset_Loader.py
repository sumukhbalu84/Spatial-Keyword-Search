import os
import pandas as pd

def load_tweet_dataset(folder_path):
    """Load tweets from all .txt files in the specified dataset folder, normalize and tokenize them."""
    data = []

    for filename in sorted(os.listdir(folder_path)):  # Ensure correct file order
        file_path = os.path.join(folder_path, filename)

        # Only open files (avoiding directories)
        if os.path.isfile(file_path):  
            with open(file_path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    
                    obj_id = int(parts[0])  # Object ID
                    lat, lon = float(parts[1]), float(parts[2])  # Spatial coordinates
                    num_keywords = int(parts[3])  # Number of keywords
                    
                    # Extract keywords and weights
                    keywords = set()  # Use a set to store unique, lowercase keywords
                    weights = []
                    start_index = 4  # First keyword appears at index 4
                    
                    for i in range(num_keywords):
                        keyword_index = start_index + (i * 2)  # Keywords at even positions
                        weight_index = keyword_index + 1       # Weights follow keywords

                        keyword = parts[keyword_index].lower().strip()  # Normalize
                        weight = float(parts[weight_index])  # Convert to float

                        keywords.add(keyword)
                        weights.append(weight)

                    # Append cleaned data
                    data.append([obj_id, lat, lon, keywords, weights])

    # Convert to Pandas DataFrame
    return pd.DataFrame(data, columns=["id", "latitude", "longitude", "keywords", "weights"])