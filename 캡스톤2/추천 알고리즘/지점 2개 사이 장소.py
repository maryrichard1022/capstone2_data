import numpy as np
import pandas as pd


places = pd.read_csv(f"C:/Users/김가연/Desktop/23-2학기/캡스톤2/data/완료/places.csv", encoding='UTF-8-SIG')
places = places[["id", "latitude", "longitude"]]


x0, y0 = 37.520707, 126.979676
x1, y1 = 37.548463, 126.984184

filtered_places = places[(places['latitude'] >= min(x0, x1)) & (places['latitude'] <= max(x0, x1)) &
                          (places['longitude'] >= min(y0, y1)) & (places['longitude'] <= max(y0, y1))]

filtered_places = filtered_places.reset_index(drop=True)[["id"]]
print(filtered_places)