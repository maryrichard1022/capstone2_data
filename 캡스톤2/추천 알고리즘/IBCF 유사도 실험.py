import pandas as pd
import numpy as np
from scipy.stats import mode
from sklearn.metrics import f1_score
from sklearn.metrics import jaccard_score
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

# 각 행 간의 Jaccard 유사도 계산
def calculate_jaccard_similarity(matrix):
    num_users = matrix.shape[0]
    similarities = np.zeros((num_users, num_users))

    for i in range(num_users):
        for j in range(i, num_users):
            similarity = jaccard_score(matrix.iloc[i], matrix.iloc[j])
            similarities[i, j] = similarity
            similarities[j, i] = similarity

    return similarities


for i in range(20):

    likes = pd.read_csv(f"C:/Users/김가연/Desktop/23-2학기/캡스톤2/data/hearts_data.csv", encoding='UTF-8-SIG')
    likes = likes[["place_id", "user_id"]]
    likes.loc[:, "heart"] = 1
    likes = likes.drop_duplicates(subset=['place_id', 'user_id'], keep='first')


    x = likes.copy()
    y = likes['user_id']


    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y)

    #  train 데이터로 Full matrix 구하기 
    likes_matrix = x_train.pivot(index='place_id', columns='user_id', values='heart')


    # train set 사용자들의 Cosine similarities 계산
    matrix_dummy = likes_matrix.copy().fillna(0)


    # 코사인 유사도
    item_similarity = cosine_similarity(matrix_dummy, matrix_dummy)

    # 자카드 유사도
    #item_similarity = calculate_jaccard_similarity(matrix_dummy)
    #item_similarity = pd.DataFrame(item_similarity, index=likes_matrix.index, columns=likes_matrix.index)
    #item_similarity



    from scipy.stats import mode
    def ibcf_binary(user_id, place_id):
        if place_id in likes_matrix:
            sim_scores = item_similarity[place_id]
            #print(sim_scores)
            
            user_likes = likes_matrix[user_id]
            #print(place_likes)
            
            none_likes_idx = user_likes[user_likes.isnull()].index
            
            #print(place_likes[place_likes.isnull()])
            #print(none_likes_idx)
            
            user_likes = user_likes.dropna()
            #print(place_likes[place_likes.isnull()])
            
            
            sim_scores = sim_scores.drop(none_likes_idx)
            #print(sim_scores[sim_scores.isnull()])
            #print("sim_scores 합계",sim_scores.sum())
            #print(sim_scores)
            
            
            #weighted_sum = np.sum(sim_scores * place_likes)
            #similarity_sum = np.sum(np.abs(sim_scores))
            #predicted_likes = weighted_sum / similarity_sum
            if sim_scores.sum() != 0.0:
                # 교재에 있는 기존 방식
                predicted_likes = np.dot(sim_scores, user_likes) / sim_scores.sum()
            else:
                predicted_likes = mode(user_likes, keepdims=True).mode[0]
            
        else:
            predicted_likes = 0.0 # 특정 장소에 대한 좋아요 없는 경우 예측 불가
        return predicted_likes


    # 정확도를 계산하는 함수 
    def f1(y_true, y_pred):
        return f1_score(y_true, y_pred)

    # 모델별 정확도를 계산하는 함수 
    def score(model):
        id_pairs = zip(x_test['user_id'], x_test['place_id'])
        
        # 예측 값
        y_pred = np.array([model(user, place) for (user, place) in id_pairs]).astype(int)
        print("y_pred", y_pred)
        
        # 실제 값
        y_true = np.array(x_test['heart'])
        print("y_true", y_true)
        return f1(y_true, y_pred)



    def CF_IBCF(user_id, place_id):
        if place_id in item_similarity:      # 현재 영화가 train set에 있는지 확인
            # 현재 영화와 다른 영화의 similarity 값 가져오기
            sim_scores = item_similarity[place_id]
            # 현 사용자의 모든 rating 값 가져오기
            user_likes = likes_matrix[user_id]
            # 사용자가 평가하지 않은 영화 index 가져오기
            non_likes_idx = user_likes[user_likes.isnull()].index
            # 사용자가 평가하지 않은 영화 제거
            user_likes = user_likes.drop(non_likes_idx)
            # 사용자가 평가하지 않은 영화의 similarity 값 제거
            
            sim_scores = pd.DataFrame(sim_scores)
            sim_scores =  sim_scores.drop(non_likes_idx)
            
            # 현 영화에 대한 예상 rating 계산, 가중치는 현 영화와 사용자가 평가한 영화의 유사도
            if sim_scores.sum() != 0.0:
                predicted_likes = np.dot(sim_scores, user_likes) / sim_scores.sum()
            else:
                predicted_likes = mode(user_likes, keepdims=True).mode[0]
                #predicted_likes = 0.0
        else:
            predicted_likes = 0.0
        return predicted_likes

    # 정확도 계산
    print("=============코사인 유사도============")
    print(score(CF_IBCF))