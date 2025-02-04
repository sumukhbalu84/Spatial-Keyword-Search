import heapq
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance (in km) between two geographic points using the Haversine formula.
    This helps measure how far apart two tweets are.
    """
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in km

def spatial_score(tweet, query_location):
    """
    Computes the spatial relevance of a tweet based on its distance from the query location.
    Closer tweets get a higher score.
    """
    distance = haversine_distance(tweet.y, tweet.x, query_location[1], query_location[0])
    return 1 / (1 + distance)  # Inverse distance, so closer tweets get higher scores

def textual_score(tweet, query_keywords):
    """
    Computes how well a tweet matches the search keywords.
    More matching keywords = higher score.
    """
    if not query_keywords:
        return 0  # No keywords in query means no text score
    matched_keywords = len(set(tweet.keywords) & query_keywords)  # Count matching words
    return matched_keywords / len(query_keywords)  # Percentage of keywords matched

import heapq

def execute_power_tkqn(teq_index, query_location, query_keywords, k, lambda_value=0.7):
    """
    Runs the POWER algorithm to find the top-k most relevant tweets based on location and keywords.
    
    Parameters:
    - teq_index: The TEQ Index (Quadtree + Inverted Index)
    - query_location: (latitude, longitude) of the search location (or None)
    - query_keywords: Set of words we want in the tweets (or None)
    - k: Number of top results to return
    - lambda_value: Controls the importance of spatial vs textual relevance (higher = more spatial importance)

    Returns:
    - A list of top-k tweet IDs, ranked by their combined score.
    """

    # Step 1: Retrieve tweets based on spatial and keyword filtering
    spatial_candidates = []
    if query_location:  # Only perform spatial search if location is provided
        spatial_candidates = teq_index.quadtree.range_query(query_location[0], query_location[1], radius=100)
        print(f"  - Found {len(spatial_candidates)} tweets near location {query_location}")

    textual_candidates = set()  # Use a set for faster lookup
    if query_keywords:  # Only perform keyword search if keywords are provided
        textual_candidates = teq_index.inverted_index.search(query_keywords)
        print(f"  - Found {len(textual_candidates)} tweets containing keywords {query_keywords}")

    # Step 2: Filter tweets that match both conditions
    candidate_tweets = {}
    if query_location and query_keywords:
        # Keep only tweets that appear in both spatial and keyword search
        for tweet in spatial_candidates:
            if tweet.id in textual_candidates:
                candidate_tweets[tweet.id] = tweet
    elif query_location:
        # If no keyword query, use only spatial candidates
        candidate_tweets = {t.id: t for t in spatial_candidates}
    elif query_keywords:
        # If no spatial query, use only keyword candidates
        candidate_tweets = {t_id: teq_index.tweet_store[t_id] for t_id in textual_candidates if t_id in teq_index.tweet_store}
    else:
        return []  # No valid query parameters given

    print(f"  - {len(candidate_tweets)} tweets passed both filters.")

    # Step 3: Use a max-heap (priority queue) to track the top-k most relevant tweets
    top_k_heap = []
    
    for tweet in candidate_tweets.values():
        s_score = spatial_score(tweet, query_location) if query_location else 0  # Use spatial score only if location is given
        t_score = textual_score(tweet, query_keywords) if query_keywords else 0  # Use textual score only if keywords are given
        final_score = lambda_value * s_score + (1 - lambda_value) * t_score  # Weighted combination

        # Store tweets in the priority queue (negative score to maintain max-heap behavior)
        heapq.heappush(top_k_heap, (-final_score, tweet.id))
        
        if len(top_k_heap) > k:
            heapq.heappop(top_k_heap)  # Remove lowest-scoring tweet if heap exceeds k

    # Step 4: Extract results from the heap and return them in sorted order
    top_k_results = []
    while top_k_heap:
        _, tweet_id = heapq.heappop(top_k_heap)
        top_k_results.append(tweet_id)

    return top_k_results[::-1]  # Return tweets in descending order of relevance