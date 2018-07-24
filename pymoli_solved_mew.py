
#left to do: comment code, write summary (purpsosefully left this not as a comment)
    
#Dependencies
import pandas as pd
import numpy as np
import os

file_path = os.path.join(os.getcwd(), 'purchase_data.csv') #raw data file filepath
file_to_load = file_path 
purchase_date = pd.read_csv(file_to_load) #read file
purch_df = pd.DataFrame(purchase_date) #create main df

purchases = purch_df['Purchase ID'].count() #total number of purchases
avg_purch = purch_df['Price'].values.sum()/purchases #average purchase total
total_rev = purch_df['Price'].values.sum() #total revenue
unique_items = purch_df['Item ID'].nunique() #number of unique items for sale
unique_players = purch_df['SN'].nunique()#unique players
item_ids= purch_df["Item ID"].unique()# list of unique items for sale

# unique_item_prices = purch_df['Price'].unique()#WRONG! Do not use! 
# avg_item_price = unique_item_prices.sum()/unique_items #WRONG! Do not use! 

unique_players_dict = {'Unique Players': unique_players} #dict of unique players
unique_players_df = pd.DataFrame(unique_players_dict, index = ['Total']) # df of unique players
unique_players_df

# print('Total Number of Players: ' + str(unique_players))
#print('Number of Unique Items: ' + str(unique_items))
# print('Average Purchase Price: $' + str(round(avg_purch,2)))
# print('Total Number of Purchases: ' + str(purchases))
# print('Total Revenue: $' + str(total_rev))
# print('Average Item Price: $' + str(round(avg_item_price,2))) #WRONG! Do Not Use! 

unique_players_list = list(purch_df['Item ID']. unique()) #list of unique item ID's
print("Unique Item ID's " + str(unique_players_list))

summary_dict = {'Average Purchase': "${:.2f}".format(avg_purch), #dict for summary df
                'Total Revenue': "${:,.2f}".format(total_rev),
                'Total Purchases': purchases,
                'Unique Items': unique_items}

summary_df = pd.DataFrame(summary_dict, index =['Summary']) #df for summary of data
summary_df

def gender_demo(x):#function to create a series
    names = {
        'Unique Players': x['SN'].nunique(), #uniqe players
        'Percent': "{:.1%}".format(x['SN'].nunique()/unique_players)} #percent of players

    return pd.Series(names)

purch_df.groupby('Gender').apply(gender_demo) # group by Gender and return a series

def purchase_analysis_gender(x):#function to create a series
    names = {
        'Purchase Count': x['Purchase ID'].count(), #purchase count
        'Average Purchase': "${:.2f}".format((x['Price'].sum()/x['Purchase ID'].count()),2), # average purchase 
        'Total Purchases': "${:,.2f}".format(x['Price'].sum())} #Total purchases 

    return pd.Series(names)

purch_df.groupby('Gender').apply(purchase_analysis_gender) #group by gender and return a series

bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999] # age bins
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"] # age bins labels

def age_demo(x):#function to create a series
    names = {
        'Purchase Count': x['Purchase ID'].count(), # purchase count
        'Percentage of Players': "{:.2%}".format(x['Gender'].count()/unique_players) , #Percentage of players 
        'Average Purchase': "${:.2f}".format(x['Price'].sum()/x['Price'].count()), #average purchase 
        'Total Purchases': "${:,.2f}".format(x['Price'].sum())} #total purchases 

    return pd.Series(names)

purch_df['Age Brackets']=pd.cut(purch_df['Age'],bins, labels= group_names) #cut df into bins
purch_df.groupby('Age Brackets').apply(age_demo) #group by Age bins and return a series

def top_spenders(x):#function to create a series
    names = {
            'Purchase Count': x['Purchase ID'].count(), #purchase count
            'Average Purchase': "${:.2f}".format(x['Price'].sum()/x['Price'].count()), # average purchase
            'Total Purchases': x['Price'].sum()} # ISSUE with formatting.  Using .format changes values.   #total purchases

    return pd.Series(names)

purch_df.groupby('SN').apply(top_spenders).sort_values(by=['Total Purchases'],ascending =False).head(5) #groupby SN and return a series

def top_items(x):#function to create a series
    names = {
            'Purchase Count': x['Purchase ID'].count(), #dropping .format from line below will change formatting to 9.0 #purchase count
            'Total Purchases': "${:.2f}".format(x['Price'].sum())} #total purchases

    return pd.Series(names)

purch_df.groupby(['Item ID','Item Name', 'Price']).apply(top_items).sort_values(by=['Purchase Count'],ascending =False).head(5) #groupby Item ID, Item Name and Price and return a series

def top_sales(x):#function to create a series
    names = {
            'Purchase Count': x['Purchase ID'].count(), #adding .format from line below will change output???????? #purchase count
            
            'Total Purchases': x['Price'].sum()} #Total purchases
            #'Total Purchases':"${:.2f}".format(x['Price'].sum())} #replace previous line with this and it will change the output

    return pd.Series(names)

purch_df.groupby(['Item ID','Item Name', 'Price']).apply(top_sales).sort_values(by=['Total Purchases'],ascending =False).head(5) #groupby Item ID, Name and Price and return a series

#Summary of three obeservable trends
print(r'Observation 1: Males make up over 80% of players and account for more than 80% of revenue.')
print(r'This observation suggests marketing efforts should be focused on primarily on males.'
      ' It is interesting to note that females make up 14.1% of players but spend slightly more than males. The Other/Non-disclosed group spends slightly more than females.'
      ' It would be of interest to market to these groups in an effort to obtain more revenue per player. '
      'This also suggests there is room for increasing the average purchase per player by a very small amount. ')
print()
print(r'Observation 2: The average player spends only $3.05 and the max spent by any player is under $19.00.'
       'This suggests a low ceiling for revenue per player.  Our efforts should likely be focused on player aquisition and not increaseing revenue per player. '
       'Once the number of players is high enough, increasing revenue per player will be more lucrative. It would also be of interest to investigate the number of items offered '
       'and how many of each are purchased. Our resources may be better spent by pushing items we already have instead of adding more items.')
print()
print(r'Observation 3: This dataset is largely incomplete.'
       'This dataset lacks important features for driving business decisions. We are looking at revenue when profit may be of more importance. This data says nothing about '
       'profitablility. The data is also lacking player location, player engagement time and player retention information. Average lifetime value of a player is an industry '
       'standard that we are not measuring. It would also be of value to have marketing '
       'information. This dataset is small but may still be used in a limited capacity to drive business decisions outlined above. From this analysists perspective we should gather much '
       'more data and rerun the analysis.')
