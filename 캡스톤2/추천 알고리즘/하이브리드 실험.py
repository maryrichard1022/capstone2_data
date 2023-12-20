import pandas as pd
import numpy as np
from scipy.stats import mode
from sklearn.metrics import f1_score
from sklearn.metrics import jaccard_score
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

# UBCF를 위한 자가드 유사도
def calculate_jaccard_similarity(matrix):
    num_users = matrix.shape[0]
    similarities = np.zeros((num_users, num_users))

    for i in range(num_users):
        for j in range(i, num_users):
            similarity = jaccard_score(matrix.iloc[i], matrix.iloc[j])
            similarities[i, j] = similarity
            similarities[j, i] = similarity

    return similarities

# 정확도를 계산하는 함수 
def f1(y_true, y_pred):
    return f1_score(y_true, y_pred)

# 모델별 정확도를 계산하는 함수 
def score(model):
    id_pairs = zip(x_test['user_id'], x_test['place_id'])
    
    # 예측 값
    y_pred = np.array([model(user, place) for (user, place) in id_pairs]).astype(int)
    #print("y_pred", y_pred)
    
    # 실제 값
    y_true = np.array(x_test['heart'])
    #print("y_true", y_true)
    return f1(y_true, y_pred)



# 정확도를 계산하는 함수 
def f1(y_true, y_pred):
    return f1_score(y_true, y_pred)

# 모델별 정확도를 계산하는 함수 
def score(model):
    id_pairs = zip(x_test['user_id'], x_test['place_id'])
    
    # 예측 값
    y_pred = np.array([model(user, place) for (user, place) in id_pairs]).astype(int)
    #print("y_pred", y_pred)
    
    # 실제 값
    y_true = np.array(x_test['heart'])
    #print("y_true", y_true)
    return f1(y_true, y_pred)


print("=================IBCF 코사인 유사도 성능=================")
for i in range(20):

    # 데이터 셋 가져오기
    likes = pd.read_csv(f"C:/Users/김가연/Desktop/23-2학기/캡스톤2/data/hearts_data.csv", encoding='UTF-8-SIG')
    likes = likes[["place_id", "user_id"]]
    likes.loc[:, "heart"] = 1 # 하트 누른 데이터만 있으므로 다 1로 만듦
    likes = likes.drop_duplicates(subset=['place_id', 'user_id'], keep='first') # 오류 방지 위해

    x = likes.copy()
    y = likes['user_id']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y)


    #  train 데이터로 Full matrix 구하기 
    likes_matrix = x_train.pivot(index='user_id', columns='place_id', values='heart')

    # train set 사용자들의 Cosine similarities 계산
    matrix_dummy = likes_matrix.copy().fillna(0)


    ##### =============================== UBCF(자가드 유사도) ======================
    # # 자카드 유사도 구하기
    # user_similarity = cosine_similarity(matrix_dummy, matrix_dummy)
    # user_similarity = pd.DataFrame(user_similarity, index=likes_matrix.index, columns=likes_matrix.index)


    # def CF_UBCF(user_id, place_id):
    #     if place_id in likes_matrix:

    #         sim_scores = user_similarity[user_id].copy()
    #         place_likes = likes_matrix[place_id].copy()     
    #         none_likes_idx = place_likes[place_likes.isnull()].index
    #         place_likes = place_likes.drop(none_likes_idx)
    #         sim_scores = sim_scores.drop(none_likes_idx)

    #         if sim_scores.sum() != 0.0:
    #             predicted_likes = np.dot(sim_scores, place_likes) / sim_scores.sum()
    #         else:
    #             #predicted_likes = mode(place_likes, keepdims=True).mode[0]
    #             predicted_likes = 0.0
                
    #     else:
    #         predicted_likes = 0.0 # 특정 장소에 대한 좋아요 없는 경우 예측 불가
    #     return predicted_likes

    #     # 정확도 계산
    # print("UBCF F1 score :", score(CF_UBCF))



# def UBCF_recommender(user, n_items):
#     # 현재 사용자가 찜한 장소
#     liked_index = likes_matrix.loc[user][likes_matrix.loc[user] > 0].index
    
#     # 현재 사용자와 유사한 사용자들의 찜한 장소의 평균 예상 찜 여부 계산
#     predictions = []
#     for place_id in likes_matrix.columns:
#         if place_id not in liked_index:
#             prediction = CF_UBCF(user, place_id)
            
#             # 0이 아닌 것은 제외
#             if prediction > 0.4:
#                 predictions.append((place_id, prediction))
    
#     #print("predictions", predictions)
    
    
#     # 예상 찜 여부를 기준으로 내림차순 정렬 (튜플이라서 이렇게 하는 듯)
#     predictions.sort(key=lambda x: x[1], reverse=True)
#     #print("predictions", predictions)
    
    
#     # 상위 n_items개의 장소를 추천
#     recommended_items = [place_id for place_id, _ in predictions[:n_items]]
    
#     return recommended_items



###### =============IBCF (코사인 유사도)
    likes_matrix_t = likes_matrix.transpose()
    matrix_dummy_t = likes_matrix_t.copy().fillna(0)

    # 코사인 유사도 계산하기
    item_similarity = calculate_jaccard_similarity(matrix_dummy_t)
    item_similarity = pd.DataFrame(item_similarity, index=likes_matrix_t.index, columns=likes_matrix_t.index)


    def CF_IBCF(user_id, place_id):
        if place_id in item_similarity:      # 현재 영화가 train set에 있는지 확인
            # 현재 장소와 다른 장소의 similarity 값 가져오기
            sim_scores = item_similarity[place_id]
            #print(sim_scores)
            # 현 사용자의 모든 찜 값 가져오기
            user_likes = likes_matrix_t[user_id]
            #print(user_likes)
            
            
            # 사용자가 평가하지 않은 장소 index 가져오기
            none_likes_idx = user_likes[user_likes.isnull()].index
            #print(none_likes_idx)
            # 사용자가 평가하지 않은 장소 제거
            user_likes = user_likes.dropna()
            #print(user_likes)
            # 사용자가 평가하지 않은 장소의 similarity 값 제거
            sim_scores = sim_scores.drop(none_likes_idx)
            #print(sim_scores)
            
            # 현 장소에 대한 예상 찜 계산, 가중치는 현 장소와 사용자가 평가한 장소의 유사도
            if sim_scores.sum() != 0.0:
                predicted_likes = np.dot(sim_scores, user_likes) / sim_scores.sum()
                #print(predicted_likes)
            else:
                #predicted_likes = mode(user_likes, keepdims=True).mode[0]
                predicted_likes = 0.0
        else:
            predicted_likes = 0.0
        return predicted_likes

    # 정확도 계산
    print("IBCF F1 score :", score(CF_IBCF))


# def IBCF_recommender(user, n_items):
#     # 현재 사용자가 찜한 장소
#     liked_index = likes_matrix.loc[user][likes_matrix.loc[user] > 0].index
    
#     # 모든 장소에 대한 예상 찜 여부 계산
#     predictions = []
#     for place_id in likes_matrix.columns:
#         if place_id not in liked_index:
#             prediction = CF_IBCF(user, place_id)
#             #print(prediction)
                        
#             # 0이 아닌 것은 제외
#             if prediction > 0.4:
#                 predictions.append((place_id, prediction))
#             #print(predictions)
#     # 예상 찜 여부를 기준으로 내림차순 정렬
#     predictions.sort(key=lambda x: x[1], reverse=True)
#     #print("predictions", predictions)
    
    
#     # 상위 n_items개의 장소를 추천
#     recommended_items = [place_id for place_id, _ in predictions[:n_items]]
#     #print("추천 장소", recommended_items)
#     return recommended_items

#UBCF_list = UBCF_recommender(user=30, n_items=50)
#print("UBCF 추천 갯수 :", len(UBCF_list))

# IBCF_list = IBCF_recommender(user=30, n_items=50)
# #print("IBCF 추천 갯수 :", len(IBCF_list))



# intersection = list(set(UBCF_list) & set(IBCF_list))
# #print("공통 추천 갯수 :", len(intersection))
# print("추천할 장소 id 리스트", intersection)
