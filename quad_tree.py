from typing import Dict, List, Tuple

class TEQCell:
    def __init__(self, ltp: str):
        """
        Initialize a TEQCell instance.

        Args:
        - ltp (str): Location table pointer, points to a hash file on disk
                     that maps object IDs to their locations.
        """
        self.ltp: str = ltp  # Location table pointer
        self.iti: Dict[str, Tuple[int, float, str, str]] = {}  # Inverted textual index
        self.oti: Dict[str, str] = {}  # Full text storage (object text index)
        self.neigh: List["TEQCell"] = []  # Neighboring cells

    def add_inverted_index(self, keyword: str, size: int, max_weight: float, list_ptr: str, set_ptr: str):
        """
        Adds an entry to the inverted textual index (iti).

        Args:
        - keyword (str): The textual keyword.
        - size (int): Number of objects containing the keyword.
        - max_weight (float): Maximum weight of the keyword in the cell.
        - list_ptr (str): Pointer to the file storing the keyword's inverted list.
        - set_ptr (str): Pointer to the file storing the keyword's inverted set.
        """
        self.iti[keyword] = (size, max_weight, list_ptr, set_ptr)

    def add_object_text(self, obj_id: str, text_ptr: str):
        """
        Adds an entry to the object text index (oti).

        Args:
        - obj_id (str): Object ID.
        - text_ptr (str): Pointer to the file storing the full text of the object.
        """
        self.oti[obj_id] = text_ptr

    def add_neighbor(self, neighbor: "TEQCell"):
        """
        Adds a neighboring cell.

        Args:
        - neighbor (TEQCell): A neighboring TEQCell.
        """
        self.neigh.append(neighbor)

    def get_keyword_info(self, keyword: str) -> Tuple[int, float, str, str]:
        """
        Retrieves keyword information from the inverted textual index.

        Args:
        - keyword (str): Keyword to retrieve.

        Returns:
        - Tuple[int, float, str, str]: (size, max_weight, list_ptr, set_ptr) for the keyword.
        """
        return self.iti.get(keyword, None)

    def get_object_text_pointer(self, obj_id: str) -> str:
        """
        Retrieves the pointer to the full text of an object.

        Args:
        - obj_id (str): Object ID.

        Returns:
        - str: Pointer to the object's full text.
        """
        return self.oti.get(obj_id, None)

    def get_neighbors(self) -> List["TEQCell"]:
        """
        Retrieves the list of neighboring cells.

        Returns:
        - List[TEQCell]: Neighboring TEQCells.
        """
        return self.neigh


# Example: Creating a TEQCell and populating it
cell = TEQCell(ltp="location_table_1.bin")

# Add inverted index entries
cell.add_inverted_index("pizza", 150, 0.87, "pizza_list.bin", "pizza_set.bin")
cell.add_inverted_index("burger", 50, 0.65, "burger_list.bin", "burger_set.bin")

# Add object text index entries
cell.add_object_text("obj_1", "textual1.bin")
cell.add_object_text("obj_2", "textual2.bin")

# Add neighbors
neighbor_cell = TEQCell(ltp="location_table_2.bin")
cell.add_neighbor(neighbor_cell)

# Retrieve data
print(cell.get_keyword_info("pizza"))  # Output: (150, 0.87, 'pizza_list.bin', 'pizza_set.bin')
print(cell.get_object_text_pointer("obj_1"))  # Output: "textual1.bin"
print(len(cell.get_neighbors()))  # Output: 1
