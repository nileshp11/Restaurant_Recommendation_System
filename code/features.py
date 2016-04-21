from __future__ import division
import pandas as pd
import numpy as np
import glob


avg_val_map = []
avg_business_map = []
business_to_user_dict = dict()


def avg_category_rating(dfReview):
    avg_category_total = dict()
    avg_category_cnt = dict()  
    avg_category_rating = dict()

    for index, row in dfReview.iterrows():
        if row['user_id'] not in avg_category_total:        
            blank_dict = {}
            blank_dict_1 = {}
            avg_category_total[ row['user_id'] ] = blank_dict
            avg_category_cnt[ row['user_id'] ] = blank_dict_1
            d_total = avg_category_total[ row['user_id'] ]
            d_cnt = avg_category_cnt[ row['user_id'] ]
        for val in row['categories']:
            if val in d_total:
                d_total[val] = d_total[val] + row['Review_stars']
                d_cnt[val] = d_cnt[val] + 1
            else:
                d_total[val] = row['Review_stars']
                d_cnt[val] = 1
        avg_category_total[ row['user_id'] ] = d_total
        avg_category_cnt[ row['user_id'] ] = d_cnt

    for key, value in avg_category_total.iteritems():
        d_final = avg_category_total[ key ]
        d_cnt = avg_category_cnt[ key ]

        for k,v in d_final.iteritems():
            d_final[k] =  v / d_cnt[k]


        avg_category_rating[ key ] = d_final

    # with open('../dataset/avg_category_rating_train.p', 'wb') as handle:
    #     pickle.dump(avg_category_rating, handle)
    return dfReview


def find_friends(dfCombined,dfCombined):
    #user_list = business_to_user_dict[business_id]
    #print user_list
    #friends = dfCombined.loc[user_id]['friends']
    prnit "started phase 1"
    for index, row in dfCombined.iterrows():
        user_id = row['user_id']    # get each user id from review 
        business_id = row['business_id']   # get its business id
        user_list = []

        if business_id in business_to_user_dict.keys():
            user_list = business_to_user_dict[business_id]   # get user list for that business which reviewed that business
        
        print "started phase 2"
        if len(user_list) != 0:     # if noone reviewed dat business then get avg stars for that business 
            f_cnt = 0
            friend_avg_score = 0.0
            for friends in dfCombined.loc[dfCombined['user_id'] == user_id, 'friends']:  # for all friends for all users..
                score = 0.0  
                cnt = 0
                friend_avg_score = 0.0
                for each_friend in friends:   # friends of that user..
                    for i, j in enumerate(user_list):  # 
                        if j == each_friend:   # review by friend for that business..
                           # print each_friend
                            score = score + float(user_list[i+1])  # get ratings given by that friend for that business..
                            #print score
                            cnt = cnt+1 
                        else:
                            #print "here",float(avg_val_map[each_friend])
                            if each_friend in avg_val_map.keys():
                                friend_avg_score =  float(avg_val_map[each_friend])
                            else:
                                friend_avg_score = float(dfCombined['Business_stars'])
                        f_cnt = cnt
                                 
                if f_cnt > 0:
                    dfCombined.loc[(dfCombined['user_id'] == user_id )& (dfCombined['business_id'] == business_id), 'friends_avg_rating_business'] = (score / f_cnt)
                else:
                    dfCombined.loc[(dfCombined['user_id'] == user_id) & (dfCombined['business_id'] == business_id), 'friends_avg_rating_business'] = (friend_avg_score)

    return dfCombined


def make_business_dict(dfTrain):
    for index,line_contents in dfTrain.iterrows():
        bus_id = line_contents['business_id']
        if bus_id in business_to_user_dict:
            business_to_user_dict[bus_id].append(line_contents['user_id'])
            business_to_user_dict[bus_id].append(line_contents['Review_stars'])
        else:
            user_list = []
            user_list.append(line_contents['user_id'])
            user_list.append(line_contents['Review_stars'])
            business_to_user_dict[bus_id] = user_list

    # with open('../dataset/business_to_user_dict.p', 'wb') as handle:
    #         pickle.dump(business_to_user_dict, handle)  


def calc_default_business_rating(df):
    avg_business_map = df.groupby('business_id')['Review_stars'].agg([pd.np.mean])
    
    for name in avg_business_map.index:
        df.loc[df['business_id'] == name, 'avg_business_rating'] = avg_business_map.loc[name]['mean']
    
    return df

def calc_default_user_rating(df):
	# max_val = df.loc[df['stars'].idxmax()]['stars']
    # min_val = df.loc[df['stars'].idxmin()]['stars']
    avg_val_map = df.groupby('user_id')['Review_stars'].agg([pd.np.mean])

    for name in avg_val_map.index:
        df.loc[df['user_id'] == name, 'avg_user_rating'] = avg_val_map.loc[name]['mean']
    
    return df


# df = pd.read_pickle("../dataset/TrainData.p")
# df = pd.read_pickle("../dataset/TestData.p")
df = pd.read_pickle("../dataset/FeatureVector.p")

df['avg_business_rating'] = df['Business_stars']
df['avg_user_rating'] = df['average_stars']
df['avg_business_rating'] = df['Business_stars'];
df['avg_user_rating'] = df['average_stars'];
df['friends_avg_rating_business'] = df['average_stars']
df['avg_category_rating'] = df['average_stars']
df['min_category_rating'] = df['average_stars']
df['max_category_rating'] = df['average_stars']

df = calc_default_business_rating(df)
df = calc_default_user_rating(df)
# df.to_pickle("../dataset/FeatureVector_v1.p")

make_business_dict(df)
df = find_friends(df)
# dfCombined.to_pickle("../dataset/FeatureVector_v2.p")

for i, row in df.iterrows():
    cat_list = row['categories']
    if len(cat_list) == 0:
        avg = 0
        mn = 10
        mx  = -1
        if row['user_id'] in avg_category_rating:
            user_dict = avg_category_rating[ row['user_id']  ]
            for cat in cat_list:
                if cat in user_dict:
                    avg = avg + user_dict[cat]
                    mn = min(mn,user_dict[cat])
                    mx = max(mx,user_dict[cat])
                else:
                    avg = avg + row['average_stars']
                    mn = min(mn,row['average_stars'])
                    mx = max(mx,row['average_stars'])
            avg = avg / len(cat_list)
        
        df.set_value(i,'avg_category_rating',avg)
        df.set_value(i,'max_category_rating',mx)
        df.set_value(i,'min_category_rating',mn)
# df.to_pickle('../dataset/FeatureVector_v3.p')

sz = len(dfReview)
trainData = dfReview[:3 * sz // 4]
testData = dfReview[3 * sz // 4:]
trainData.to_pickle("../dataset/TrainData.p")
testData.to_pickle("../dataset/TestData.p")
