class Boundary:
    """Defines the boundary of a rectangular region in the Quadtree."""
    def __init__(self, center_x, center_y, width, height):
        self.center_x = center_x  # Longitude (x)
        self.center_y = center_y  # Latitude (y)
        self.width = width
        self.height = height

    def contains(self, tweet):
        """Check if a tweet (point) is inside this boundary."""
        return (self.center_x - self.width <= tweet.x < self.center_x + self.width and
                self.center_y - self.height <= tweet.y < self.center_y + self.height)


class Tweet:
    """Represents a tweet with a location and keywords."""
    def __init__(self, tweet_id, keywords, lon, lat):
        self.id = tweet_id  # Unique tweet ID
        self.keywords = keywords  # Set of keywords
        self.x = lon  # Longitude (x-axis)
        self.y = lat  # Latitude (y-axis)


class Quadtree:
    """This function retrieves a tweet within a given radius"""
    def range_query(self, center_x, center_y, radius):
        """Finds all tweets within the given radius from (center_x, center_y)."""
        results = []

        # Check tweets in this node
        for tweet in self.tweets:
            distance = ((tweet.x - center_x) ** 2 + (tweet.y - center_y) ** 2) ** 0.5  # Euclidean Distance
            if distance <= radius:
                results.append(tweet)

        # Recursively search child nodes
        if self.divided:
            for child in self.children:
                results.extend(child.range_query(center_x, center_y, radius))

        return results
    """A simple Quadtree for spatial partitioning of tweets."""
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary  # The region this Quadtree covers
        self.capacity = capacity  # Maximum tweets before subdivision
        self.tweets = []  # List of tweets in this region
        self.divided = False  # Flag to check if the node has been split
        self.children = []  # Four sub-regions (when split)

    def insert(self, tweet):
        """Inserts a tweet into the Quadtree."""
        if not self.boundary.contains(tweet):
            return False  # Ignore tweets outside the current region

        if len(self.tweets) < self.capacity:
            self.tweets.append(tweet)  # Add tweet if capacity allows
            return True

        # If we reach capacity, divide the Quadtree into four parts
        if not self.divided:
            self.subdivide()

        # Try inserting the tweet into one of the child quadrants
        for child in self.children:
            if child.insert(tweet):
                return True

        return False  # Should never reach this

    def subdivide(self):
        """Splits the current Quadtree into four equal parts."""
        x, y = self.boundary.center_x, self.boundary.center_y
        w, h = self.boundary.width / 2, self.boundary.height / 2

        self.children = [
            Quadtree(Boundary(x - w, y - h, w, h)),  # Top-left
            Quadtree(Boundary(x + w, y - h, w, h)),  # Top-right
            Quadtree(Boundary(x - w, y + h, w, h)),  # Bottom-left
            Quadtree(Boundary(x + w, y + h, w, h))   # Bottom-right
        ]
        self.divided = True

class InvertedIndex:
    """Maps keywords to a set of tweet IDs for fast text searches."""
    def __init__(self):
        self.index = {}

    def add_tweet(self, tweet):
        """Adds a tweet's keywords to the inverted index."""
        for keyword in tweet.keywords:
            if keyword not in self.index:
                self.index[keyword] = set()
            self.index[keyword].add(tweet.id)

    def search(self, query_keywords, exclude_keywords=None):
        """Finds tweet IDs that match the given keywords and excludes unwanted keywords."""
        result = set()

        # Find tweets that match positive query keywords
        for keyword in query_keywords:
            if keyword in self.index:
                result = result | set(self.index[keyword])  # Ensure we perform union.

        # Remove tweets that contain excluded keywords
        if exclude_keywords:
            for keyword in exclude_keywords:
                if keyword in self.index:
                    result = result - set(self.index[keyword])  # Ensure we perform set difference

        return result
    
class TEQIndex:
    """Combines a Quadtree for spatial partitioning and an Inverted Index for keyword searches."""
    
    def __init__(self, boundary, capacity=4):
        self.quadtree = Quadtree(boundary, capacity)  # Spatial index
        self.inverted_index = InvertedIndex()  # Textual index
        self.tweet_store = {}  # Stores all tweet objects by ID

    def insert_location(self, tweet_id, lon, lat):
        """First Pass: Insert only location data into the Quadtree."""
        tweet = Tweet(tweet_id, set(), lon, lat)  # Empty keyword set
        self.quadtree.insert(tweet)  # Only store spatial data
        self.tweet_store[tweet_id] = tweet  # Store tweet object for future updates

    def insert_text(self, tweet_id, keywords):
        """Second Pass: Insert only keyword data into the Inverted Index."""
        if tweet_id in self.tweet_store:  # Ensure the tweet exists
            self.tweet_store[tweet_id].keywords = keywords  # Update tweet with keywords
        self.inverted_index.add_tweet(self.tweet_store[tweet_id])  # Store only textual data

    @staticmethod
    def get_dynamic_boundary(df):
        """Compute the world boundary dynamically from dataset."""
        min_lon, max_lon = df["longitude"].min(), df["longitude"].max()
        min_lat, max_lat = df["latitude"].min(), df["latitude"].max()
        center_x, center_y = (min_lon + max_lon) / 2, (min_lat + max_lat) / 2
        width, height = (max_lon - min_lon) / 2, (max_lat - min_lat) / 2
        return Boundary(center_x, center_y, width, height)