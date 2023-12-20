# 초반 : 레이블링을 통해 추천
# 1. 서비스 시작 시, 카테고리와 필터 분포가 다양하게 n개의 플레이스를 보여주면서 마음에 드는 장소를 선택하라고 함
# 2. 사용자가 선택한 플레이스의 카테고리와 필터를 바탕으로 비슷한 장소를 n개 추천
# 3. 찜하기 테이블이 어느정도 채워지면, 레이블링과 UBCF+IBCF를 모두 사용하여 추천해주는 방식으로 설계

import numpy as np
import pandas as pd

places = pd.read_csv(f"C:/Users/김가연/Desktop/23-2학기/캡스톤2/data/완료/places.csv", encoding='UTF-8-SIG')
filters_places = pd.read_csv(f"C:/Users/김가연/Desktop/23-2학기/캡스톤2/data/완료/filters_places.csv", encoding='UTF-8-SIG')


merged_df = pd.merge(places, filters_places, left_on='id', right_on='place_id')
place = merged_df[['category_id', 'filter_id','name_x', 'id_x']]
place = place.rename(columns={'name_x' : 'name', 'id_x' : 'id'})

# category_id가 1에서 7까지인 행만 선택 (8ㅇㅁ)
selected_rows = place[place['category_id'].between(1, 7)]


place_sampled = selected_rows.groupby(['category_id', 'filter_id']).apply(lambda x: x.sample(n=min(1, len(x)))).reset_index(drop=True)


# 이 랜덤으로 뽑힌 플레이스에서 사용자가 찜 버튼을 누르면 해당 플레이스의 찜이 저장됨
# 저장됨 찜을 바탕으로 플레이스의 카테고리, 필터가 동일한 장소들을 추천해주는 방식

#np.random.seed(42)

# 임의로 사용자가 찜한 플레이스 목록 생성
user_likes = pd.DataFrame(place_sampled.sample(n=3))

# 사용자가 찜한 플레이스와 동일한 카테고리, 필터를 가진 다른 플레이스 추천
def recommend_similar_places(user_likes, place):
    recommended_places = pd.DataFrame(columns=place.columns)
    
    for index, row in user_likes.iterrows():
        similar_places = place[(place['category_id'] == row['category_id']) & (place['filter_id'] == row['filter_id'])]
        similar_places = similar_places[similar_places['name'] != row['name']]
        
        if not similar_places.empty:
            sampled_places = similar_places.drop_duplicates(subset=['name'])
            sampled_places = sampled_places.sample(n=min(3, len(similar_places)), replace=True) # 각 조건에 해당하는(카테고리 필터 쌍) 장소를 n=3개씩 뽑음
            recommended_places = pd.concat([recommended_places, sampled_places], ignore_index=True)
            recommended_places = recommended_places.drop_duplicates(subset=['name'])
            #print(recommended_places)
            
            # 각 조건에 해당하는 장소 3개씩 뽑은 것 중에 랜덤하게 5개 장소 뽑음
            recommended_places = recommended_places.sample(frac=1, random_state=42).head(5)
            #print(recommended_places)
    return recommended_places

# 사용자에게 추천할 플레이스
recommended_places = recommend_similar_places(user_likes, place)
print(recommended_places)