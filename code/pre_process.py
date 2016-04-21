from __future__ import division
import simplejson as json
import pandas as pd

data = []
print "Reading User Object"
with open("../dataset/crap/yelp_academic_dataset_user.json") as fin:
    for line in fin:
        line_contents = json.loads(line)
        data.append(line_contents)

for element in data:
    del element["type"]
    del element["name"]
    voteCount = 0
    for keyValuePair in element["votes"].items():
        voteCount += keyValuePair[1]
    element["votes"] = voteCount
    complimentCount = 0
    for keyValuePair in element["compliments"].items():
        complimentCount += keyValuePair[1]
    element["compliments"] = complimentCount

dfUser = pd.DataFrame(data)
dfUser = dfUser.fillna(0)

dfUser.to_pickle("../dataset/User.p")


data = []
print "Reading Business Object"
with open("../dataset/crap/yelp_academic_dataset_business.json") as fin:
    for line in fin:
        line_contents = json.loads(line)
        data.append(line_contents)

categoryList = {}
catCnt = 0
noiseLevelList = {}
noiseCnt = 0
attireList = {}
attireCnt = 0
alcoholList = {}
alcoholCnt = 0

for element in data:
    del element["type"]
    del element["name"]
    del element["full_address"]
    del element["hours"]
    del element["city"]
    del element["neighborhoods"]
    del element["longitude"]
    del element["latitude"]
    del element["state"]

    lst = []
    for category in element["categories"]:
        if category not in categoryList:
            categoryList[category] = catCnt
            lst.append(catCnt)
            catCnt += 1
        else:
            lst.append(categoryList[category])

    element["categories"] = lst

    for keyValuePair in element["attributes"].items():
        if keyValuePair[0] == "Noise Level":
            if keyValuePair[1] not in noiseLevelList:
                noiseLevelList[keyValuePair[1]] = noiseCnt
                element[keyValuePair[0]] = noiseCnt
                noiseCnt += 1
            else:
                element[keyValuePair[0]] = noiseLevelList[keyValuePair[1]]
        elif keyValuePair[0] == "Attire":
            if keyValuePair[1] not in attireList:
                attireList[keyValuePair[1]] = attireCnt
                element[keyValuePair[0]] = attireCnt
                attireCnt += 1
            else:
                element[keyValuePair[0]] = attireList[keyValuePair[1]]
        elif keyValuePair[0] == "Alcohol":
            if keyValuePair[1] not in alcoholList:
                alcoholList[keyValuePair[1]] = alcoholCnt
                element[keyValuePair[0]] = alcoholCnt
                alcoholCnt += 1
            else:
                element[keyValuePair[0]] = alcoholList[keyValuePair[1]]
        elif "Music" in keyValuePair and keyValuePair[0] != 0:
            for tmp in keyValuePair[1].items():
                if tmp[1] == "True":
                    element[tmp[0]] = 1
                else:
                    element[tmp[0]] = 0
        elif "Parking" in keyValuePair and keyValuePair[0] != 0:
            for tmp in keyValuePair[1].items():
                if tmp[1] == "True":
                    element[tmp[0]] = 1
                else:
                    element[tmp[0]] = 0
        elif "Good For" in keyValuePair and keyValuePair[0] != 0:
            for tmp in keyValuePair[1].items():
                if tmp[1] == "True":
                    element[tmp[0]] = 1
                else:
                    element[tmp[0]] = 0
        elif "Ambience" in keyValuePair and keyValuePair[0] != 0:
            for tmp in keyValuePair[1].items():
                if tmp[1] == "True":
                    element[tmp[0]] = 1
                else:
                    element[tmp[0]] = 0
        else:
            if keyValuePair[1] == "True":
                element[keyValuePair[0]] = 1
            else:
                element[keyValuePair[0]] = 0

    del element["attributes"]

    if "open" in element:
        if element["open"] == "True":
            element["open"] = 1
        else:
            element["open"] = 0

            # print element

dfBusiness = pd.DataFrame(data)
dfBusiness = dfBusiness.fillna(0)
dfBusiness[['Accepts Credit Cards','Accepts Insurance','Ages Allowed','Alcohol','Attire','BYOB','BYOB/Corkage','By Appointment Only','Caters','Coat Check','Corkage','Delivery','Dietary Restrictions','Dogs Allowed','Drive-Thru','Good For Dancing','Good For Groups','Good for Kids','Hair Types Specialized In','Happy Hour','Has TV','Noise Level','Open 24 Hours','Order at Counter','Outdoor Seating','Price Range','Smoking','Take-out','Takes Reservations','Waiter Service','Wheelchair Accessible','Wi-Fi','background_music','breakfast','brunch','casual','classy','dessert','dinner','divey','dj','garage','hipster','intimate','jukebox','karaoke','latenight','live','lot','lunch','open','review_count','romantic','street','touristy','trendy','upscale','valet','validated','video']] = dfBusiness[
    ['Accepts Credit Cards','Accepts Insurance','Ages Allowed','Alcohol','Attire','BYOB','BYOB/Corkage','By Appointment Only','Caters','Coat Check','Corkage','Delivery','Dietary Restrictions','Dogs Allowed','Drive-Thru','Good For Dancing','Good For Groups','Good for Kids','Hair Types Specialized In','Happy Hour','Has TV','Noise Level','Open 24 Hours','Order at Counter','Outdoor Seating','Price Range','Smoking','Take-out','Takes Reservations','Waiter Service','Wheelchair Accessible','Wi-Fi','background_music','breakfast','brunch','casual','classy','dessert','dinner','divey','dj','garage','hipster','intimate','jukebox','karaoke','latenight','live','lot','lunch','open','review_count','romantic','street','touristy','trendy','upscale','valet','validated','video']].astype(int)
dfBusiness.to_pickle("../dataset/Business.p")


data = []
print "Reading Review Object"
business_to_user_dict = {}
with open('../dataset/crap/yelp_academic_dataset_review.json') as f:
    for line in f:
        line_contents = json.loads(line)

        s = sum(line_contents['votes'].values())  # sum of 3 types of votes
        line_contents['votes'] = s

        data.append(line_contents)
        bus_id = line_contents['business_id']
        if bus_id in business_to_user_dict:
            business_to_user_dict[bus_id].append(line_contents['user_id'])
        else:
            user_list = [line_contents['user_id']]
            business_to_user_dict[bus_id] = user_list

dfReview = pd.DataFrame(data)
dfReview.drop('type', axis=1, inplace=True)
dfReview.drop('text', axis=1, inplace=True)
dfReview['avg_business_rating'] = 0;
dfReview['avg_user_rating'] = 0;
dfReview.to_pickle("../dataset/Review.p")

print "Merging Objects"
dfBusiness = dfBusiness.rename(columns={'stars': 'Business_stars'})
dfReview = dfReview.rename(columns={'stars': 'Review_stars'})

dfBusiness = dfBusiness.rename(columns={'review_count': 'Business_review_count'})
dfUser = dfUser.rename(columns={'review_count': 'User_review_count'})

dfUser = dfUser.rename(columns={'votes': 'User_votes'})
dfReview = dfReview.rename(columns={'votes': 'Review_votes'})

df = pd.merge(dfBusiness, dfReview, how='inner', on='business_id')
df = pd.merge(df, dfUser, how='inner', on='user_id')

print "Sorting.."
df = df.sort_values(by='date')

print "Final Write..."
df.to_pickle("../dataset/FeatureVector.p")
