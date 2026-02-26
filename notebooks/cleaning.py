import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('zomato.csv')

# Drop unnecessary columns
df.drop(['url', 'address', 'phone','reviews_list','menu_item','dish_liked'], axis=1, inplace=True)


# Removes '/5', handles strings, and keeps NaNs as NaNs
df['rate'] = df['rate'].str.split('/').str[0]

# Convert 'NEW' and '-' to NaN and change the whole column to float
df['rate'] = df['rate'].replace(['NEW', '-'], np.nan).astype(float)

# Replace nan with mean
df['rate'] = df['rate'].fillna(df['rate'].mean())

# Handle approx_cost for two people Remove commas and convert to numeric
df['approx_cost(for two people)'] = df['approx_cost(for two people)'].str.replace(',', '').astype(float)

df.dropna(subset=['approx_cost(for two people)'], inplace=True) #Decied to drop rows with missing cuz low %

# Handle online_order and book_table
df['online_order'] = df['online_order'].map({'Yes': 1, 'No': 0})
df['book_table'] = df['book_table'].map({'Yes': 1, 'No': 0})

# Handle location
df['location'] = df['location'].fillna('Unknown')
df['location'] = df['location'].str.strip() # Remove leading/trailing whitespace
df['location'] = df['location'].replace(' ', 'Unknown') # Replace empty strings with 'Unknown'

# Handle rest_type
df['rest_type'] = df['rest_type'].fillna('Unknown')
df['rest_type'] = df['rest_type'].str.strip() # Remove leading/trailing whitespace
df['rest_type'] = df['rest_type'].replace(' ', 'Unknown') # Replace empty strings with 'Unknown'

# Handle cuisine
df['cuisines'] = df['cuisines'].fillna('Unknown')
df['cuisines'] = df['cuisines'].str.strip() # Remove leading/trailing whitespace
df['cuisines'] = df['cuisines'].replace(' ', 'Unknown') # Replace empty strings with 'Unknown'


# Handle listed_in(type)
df['listed_in(type)'] = df['listed_in(type)'].fillna('Unknown')
df['listed_in(type)'] = df['listed_in(type)'].str.strip() # Remove leading/trailing whitespace
df['listed_in(type)'] = df['listed_in(type)'].replace(' ', 'Unknown') # Replace empty strings with 'Unknown'

# Handle listed_in(city)
df['listed_in(city)'] = df['listed_in(city)'].fillna('Unknown')
df['listed_in(city)'] = df['listed_in(city)'].str.strip() # Remove leading/trailing whitespace
df['listed_in(city)'] = df['listed_in(city)'].replace(' ', 'Unknown') # Replace empty strings with 'Unknown'

# Handle name
df['name'] = df['name'].fillna('Unknown')
df['name'] = df['name'].str.strip() # Remove leading/trailing whitespace
df['name'] = df['name'].replace(' ', 'Unknown') # Replace empty strings with 'Unknown'

# Drop duplicates for name and location
df.drop_duplicates(subset=['name', 'location'], keep='first', inplace=True)


# Clean Data Set
df.to_csv('zomato_cleaned.csv', index=False)
