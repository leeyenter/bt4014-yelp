import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

print("Loading review.json")
review = pd.read_json('data/review.json', lines=True, orient='columns')
print("Loading business.json")
business = pd.read_json('data/business.json', lines=True, orient='columns').set_index('business_id')
business.drop(['attributes', 'hours'], axis=1, inplace=True)
print("Loading user.json")
user = pd.read_json('data/user.json', lines=True, orient='columns').set_index('user_id')
print("Loading checkin.json")
checkin = pd.read_json('data/checkin.json', lines=True, orient='columns').set_index('business_id')

for num_reviews in [2000, 50000, 100000, 300000]:
    print("Generating sample of", num_reviews, "reviews")
    
    review_sample = review.sample(num_reviews, random_state = 1)
    
    business_ids = review_sample[['business_id']].drop_duplicates().set_index('business_id')
    user_ids = review_sample[['user_id']].drop_duplicates().set_index('user_id')
    
    business_sample = business_ids.join(business).reset_index()
    user_sample = user_ids.join(user).reset_index()
    checkin_sample = business_ids.join(checkin).reset_index()
    
    print("   - Saving to Parquet")

    review_sample.to_parquet("data/"+str(num_reviews)+"_review.parquet")
    business_sample.to_parquet("data/"+str(num_reviews)+"_business.parquet")
    user_sample.to_parquet("data/"+str(num_reviews)+"_user.parquet")
    checkin_sample.to_parquet("data/"+str(num_reviews)+"_checkin.parquet")