# [Task 3 | Data Munging and Visualization] Quantify the network and engagement overlap between influencers
# Instructions:										
# Step 1: Network overlap: with the "following.json" dataset, write a function that takes any two influencers' user ID's 
# and calculate the fraction of followers these two influencers share over the total number of followers of the less 
# followed influencer. The reference date is April 30, 2022.
# Step 2: Engagement overlap: with the "engagement.json" dataset, write a function that takes any two influencers' user 
# ID's and calculate the fraction of engagers of these two influencers' tweets as a function of the total number of 
# engagers of the less engaged influencer, over the period of April 22, 2022 to April 30, 2022.
# Step 3: Produce two histograms of network overlap (Step 2) and engagement overlap (Step 3) measures, respectively, 
# across all influencer pairs
# Step 5: Use OLS to regress engagement overlap on network overlap measures for all influencers pairs, and plot 
# the regression results on a two-dimensional graph with standard error bands.
# Step 6: Develop a hypothesis on the determinants of the difference between network vs engagement overlaps, 
# i.e. what makes two influencers have high network overlap but low engagement overlap and vice versa?
# Step 7 (bonus): Conduct some exploratory data analysis to test your hypothesis in Step 6.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import seaborn as sns

def network_overlap(df, inf_id1, inf_id2):
    df = df[df['follow_timestamp'] <= '2022-04-30']

    #filter dataframes for both influencer's following list
    followers_df1 = df[df['influencer_uid'] == inf_id1][['follower_uid']]
    followers_df2 = df[df['influencer_uid'] == inf_id2][['follower_uid']]

    #count each influencer's # of followers
    followers_count1 = followers_df1['follower_uid'].nunique()
    followers_count2 = followers_df2['follower_uid'].nunique()
    
    #inner merge to get followers overlap
    shared_followers = pd.merge(followers_df1, followers_df2, on='follower_uid', how='inner')
    
    network_overlap = len(shared_followers) / min(followers_count1, followers_count2)
    
    return network_overlap

def engagement_overlap(df, inf_id1, inf_id2):
    df = df[(df['engaged_dt'] >= '2022-04-22') & (df['engaged_dt'] <= '2022-04-30')]

    engager_df1 = df[df['influencer_uid'] == inf_id1][['follower_uid']]
    engager_df2 = df[df['influencer_uid'] == inf_id2][['follower_uid']]

    engager_count1 = engager_df1['follower_uid'].nunique()
    engager_count2 = engager_df2['follower_uid'].nunique()

    shared_engager = pd.merge(engager_df1, engager_df2, on='follower_uid', how='inner')
    engagement_overlap = len(shared_engager) / min(engager_count1, engager_count2)

    return engagement_overlap

#get overlap fractions across all influencer pairs
#function created to reduce code redundancy
def overlaps_for_all_pair(is_network, df, inf_ids):
    overlap_data = []

    #run a nested for loop to measure every pair
    for i in range(len(inf_ids)):
        for j in range(i+1, len(inf_ids)):
            inf_id1 = inf_ids[i]
            inf_id2 = inf_ids[j]
            if is_network:
                each_overlap = network_overlap(df, inf_id1, inf_id2)
            else:
                each_overlap = engagement_overlap(df, inf_id1, inf_id2)
            overlap_data.append(each_overlap)

    return overlap_data

if __name__ == '__main__':
    following_df = pd.read_json('following.json')
    following_df['follow_timestamp'] = pd.to_datetime(following_df['follow_timestamp']).dt.normalize() #only keep the date

    test_fraction1 = network_overlap(following_df, 902200087, 14709326)
    print(f"The fraction of followers shared between influencer 902200087 and 14709326 is: {test_fraction1:.4f}")
    test_fraction2 = network_overlap(following_df, 110396781, 15675138)
    print(f"The fraction of followers shared between influencer 110396781 and 15675138 is: {test_fraction2:.4f}")

    engage_df = pd.read_json('engagement.json')
    engage_df['engaged_dt'] = pd.to_datetime(engage_df['engaged_dt'])
 
    test_fraction3 = engagement_overlap(engage_df, 902200087, 14709326)
    print(f"The fraction of engagers shared between influencer 902200087 and 14709326 is: {test_fraction3:.4f}")
    test_fraction4 = engagement_overlap(engage_df, 110396781, 15675138)
    print(f"The fraction of engagers shared between influencer 110396781 and 15675138 is: {test_fraction4:.4f}")
   
    #two dataset had different numbers of influencer IDs, to compare, I chose the influencerIDs both datasets shared
    network_inf_ids = following_df['influencer_uid'].unique()
    engage_inf_ids = engage_df['influencer_uid'].unique()
    influencer_ids = np.intersect1d(network_inf_ids, engage_inf_ids)

    #plotting histograms
    network_overlap_data = overlaps_for_all_pair(True, following_df, influencer_ids)
    plt.hist(network_overlap_data)
    plt.xlabel('Network Overlap')
    plt.ylabel('Frequency')
    plt.title('Histogram of Network Overlap')
    plt.show()

    engagement_overlap_data = overlaps_for_all_pair(False, engage_df, influencer_ids)
    plt.hist(engagement_overlap_data)
    plt.xlabel('Engagement Overlap')
    plt.ylabel('Frequency')
    plt.title('Histogram of Engagement Overlap')
    plt.show()

    #Run OLS to regress engagement overlap on network overlap
    x = sm.add_constant(network_overlap_data)
    y = engagement_overlap_data
    model = sm.OLS(y, x).fit()
    predictions = model.get_prediction(x)
    print(model.summary())

    #Use seaborn for plotting the regression, showing a 95% confidence interval as the standard error band
    sns.regplot(x=network_overlap_data, y=engagement_overlap_data, scatter=True, fit_reg=True, ci=95)
    plt.xlabel('Network Overlap')
    plt.ylabel('Engagement Overlap')
    plt.title('Regression of Engagement Overlap on Network Overlap')
    plt.show()

    ## Hypothesis on the determinants of the difference between network vs engagement overlaps:

    # 1. Some influencers post certain contents that resonates with a large group of users, but they do not aim to
    # build a vertical network (don't have a consistent follower base), resulting in high engagement overlap but
    # low network overlap with other influencers. Vice versa, some influencers may be dedicated to niche interests,
    # but they don't usually engage with audience actively, resulting in high network overlap but low engagement overlap
    # with other influencers of same interest.

    # 2. Influencers that post very similar content may have high network overlap but low engagement overlap, since
    # users might not engage in highly similar posts twice. 

    # 3. Influencers with similar follower demographics but posts with different frequency may have high network overlap 
    # but low engagement overlap