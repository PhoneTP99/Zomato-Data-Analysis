import pandas as pd
import numpy as np

def clean_zomato_data(file_path):
    # 1. Load Data
    df = pd.read_csv(file_path)
    
    # 2. Drop "Heavy" columns immediately
    to_drop = ['url', 'address', 'phone', 'reviews_list', 'menu_item', 'dish_liked']
    df.drop(columns=to_drop, inplace=True, errors='ignore')

    # 3. Clean categorical columns using their ORIGINAL names first
    # This avoids the KeyError if the renaming logic behaves differently
    standard_fix_cols = ['location', 'rest_type', 'cuisines', 'name', 
                         'listed_in(type)', 'listed_in(city)']
    
    for col in standard_fix_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown').astype(str).str.strip().replace('', 'Unknown')

    # 4. Handle Rate and Cost using ORIGINAL names
    # Fix Rate
    if 'rate' in df.columns:
        df['rate'] = (df['rate'].astype(str)
                      .str.split('/').str[0]
                      .replace(['NEW', '-', 'nan'], np.nan)
                      .astype(float))
        df['rate'] = df['rate'].fillna(df['rate'].mean())

    # Fix Cost
    cost_col_original = 'approx_cost(for two people)'
    if cost_col_original in df.columns:
        df[cost_col_original] = (df[cost_col_original].astype(str)
                                 .str.replace(',', '')
                                 .replace('nan', np.nan)
                                 .astype(float))
    
    # 5. Binary Mapping
    binary_map = {'Yes': 1, 'No': 0}
    for col in ['online_order', 'book_table']:
        if col in df.columns:
            df[col] = df[col].map(binary_map)

    # 6. NOW Rename the columns for Power BI
    # This ensures all cleaning is done, then names are standardized
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace(' ', '_')
                  .str.replace('(', '')
                  .str.replace(')', '')
                  .str.replace('-', '_')
                  .str.replace('__', '_')) # Clean up double underscores
    
    # 7. Final Polish (Using new names)
    df.drop_duplicates(subset=['name', 'location'], keep='first', inplace=True)
    
    # Use the new name for the cost column dropna
    new_cost_name = 'approx_cost_for_two_people'
    if new_cost_name in df.columns:
        df.dropna(subset=[new_cost_name], inplace=True)

    return df

# --- EXECUTION ---
df_cleaned = clean_zomato_data('zomato.csv')
df_cleaned.to_csv('zomato_final_cleaned.csv', index=False)

print(f"Success! Cleaned data shape: {df_cleaned.shape}")
print("Final Columns:", df_cleaned.columns.tolist())