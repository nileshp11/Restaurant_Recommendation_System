from __future__ import division
import pandas as pd
import pickle
from sklearn import cross_validation
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier, RandomForestRegressor, AdaBoostRegressor
from sklearn.cross_validation import KFold


def classfier(train, test):
    predictors = ['average_stars', 'compliments', 'fans', 'Business_stars', 'User_votes', 'User_review_count',
                  'Business_review_count', 'avg_business_rating', 'avg_user_rating', 'Accepts Credit Cards',
                  'Accepts Insurance', 'Ages Allowed', 'Alcohol', 'Attire', 'BYOB', 'BYOB/Corkage',
                  'By Appointment Only', 'Caters', 'Coat Check', 'Corkage', 'Delivery', 'Dietary Restrictions',
                  'Dogs Allowed', 'Drive-Thru', 'Good For Dancing', 'Good For Groups', 'Good for Kids',
                  'Hair Types Specialized In', 'Happy Hour', 'Has TV', 'Noise Level', 'Open 24 Hours',
                  'Order at Counter', 'Outdoor Seating', 'Price Range', 'Smoking', 'Take-out', 'Takes Reservations',
                  'Waiter Service', 'Wheelchair Accessible', 'Wi-Fi', 'background_music', 'breakfast', 'brunch',
                  'casual', 'classy', 'dessert', 'dinner', 'divey', 'dj', 'garage', 'hipster', 'intimate', 'jukebox',
                  'karaoke', 'latenight', 'live', 'lot', 'lunch', 'open', 'romantic', 'street',
                  'touristy', 'trendy', 'upscale', 'valet', 'validated',
                  'video']  # 

    alg = LogisticRegression(random_state=1)  # AdaBoostRegressor(DecisionTreeRegressor(max_depth=10), n_estimators=500, random_state=1)#RandomForestRegressor(random_state = 0, n_estimators = 500)#ExtraTreesClassifier(random_state=1, n_estimators=500, min_samples_split=2, min_samples_leaf=1)#DecisionTreeRegressor(max_depth=10)#LogisticRegression(random_state=1)

    
    # train_target = train["Review_stars"]
    alg.fit(train[predictors], train.Review_stars)
    predictions = alg.predict(test[predictors])
    # print test_predictions, df["Review_stars"]
    
    # print predictions
    

    #print "Predictions:", predictions[0 : 10]
    predictions = predictions.astype(int)
    cnt = 0

    i = 0
    for x,row in test.iterrows():
      if ((predictions[i] > 3 and row["Review_stars"] > 3) or (predictions[i] < 3 and row["Review_stars"] < 3)):
        cnt = cnt + 1  
      i = i + 1


    accuracy = cnt / len(predictions)
    print "Accuracy: ", accuracy * 100


dfTrain = pd.read_pickle("../dataset/TrainData.p")
dfTest = pd.read_pickle("../dataset/TestData.p")
print "train dataset:", len(dfTrain)
print "test dataset:", len(dfTest)
classfier(dfTrain, dfTest)
