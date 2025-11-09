import joblib
from pprint import pprint

idx_map = joblib.load("C:/Users/Acer/Desktop/Files/projects/dynamic-recommender/backend/ml/models/product_index_map.joblib")
print(f"Loaded index map with {len(idx_map)} products\n")
pprint(list(idx_map.keys())[:20])
