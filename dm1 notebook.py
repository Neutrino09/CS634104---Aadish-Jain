# -*- coding: utf-8 -*-
"""dm1 notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dVbcbewAphSID342X9RGaZd9cjXUu4kX
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install mlxtend

import pandas as pd

# Load Amazon and Best Buy datasets
amazon_df = pd.read_csv('Amazon transactions.csv')
best_buy_df = pd.read_csv('Best Buy transactions.csv')

# Load K-Mart, Nike, and Generic datasets
kmart_df = pd.read_csv('Kmart transactions.csv')
nike_df = pd.read_csv('Nike transactions.csv')
generic_df = pd.read_csv('Generic transactions.csv')

# Concatenate all datasets
all_transactions = pd.concat([amazon_df, best_buy_df, kmart_df, nike_df, generic_df], ignore_index=True)

# Save the concatenated dataset to a new CSV file
all_transactions.to_csv('All_transactions.csv', index=False)

"""# Apriori"""

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def preprocess_and_apriori(df, min_support, min_confidence):
    # Convert all non-numeric values to strings
    df = df.applymap(str)

    # Handle NaN values by filling them with an empty string
    df.fillna('', inplace=True)

    # Perform Apriori algorithm
    te = TransactionEncoder()
    te_ary = te.fit(df.values).transform(df.values)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

    # Apriori algorithm
    frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)

    # Association rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

    return frequent_itemsets, rules

# Load K-Mart data from CSV file
kmart_df = pd.read_csv('Kmart transactions.csv')
kmart_min_support = 0.1
kmart_min_confidence = 0.7
kmart_frequent_itemsets, kmart_rules = preprocess_and_apriori(kmart_df, kmart_min_support, kmart_min_confidence)
print("\nK-Mart Frequent Itemsets:")
print(kmart_frequent_itemsets)
print("\nK-Mart Association Rules:")
print(kmart_rules)

# Load Nike data from CSV file
nike_df = pd.read_csv('Nike transactions.csv')
nike_min_support = 0.1
nike_min_confidence = 0.7
nike_frequent_itemsets, nike_rules = preprocess_and_apriori(nike_df, nike_min_support, nike_min_confidence)
print("\nNike Frequent Itemsets:")
print(nike_frequent_itemsets)
print("\nNike Association Rules:")
print(nike_rules)

# Load Generic data from CSV file
generic_df = pd.read_csv('Generic transactions.csv')
generic_min_support = 0.2
generic_min_confidence = 0.7
generic_frequent_itemsets, generic_rules = preprocess_and_apriori(generic_df, generic_min_support, generic_min_confidence)
print("\nGeneric Frequent Itemsets:")
print(generic_frequent_itemsets)
print("\nGeneric Association Rules:")
print(generic_rules)

# Load Amazon data from CSV file
amazon_df = pd.read_csv('Amazon transactions.csv')
amazon_min_support = 0.2
amazon_min_confidence = 0.7
amazon_frequent_itemsets, amazon_rules = preprocess_and_apriori(amazon_df, amazon_min_support, amazon_min_confidence)
print("\nAmazon Frequent Itemsets:")
print(amazon_frequent_itemsets)
print("\nAmazon Association Rules:")
print(amazon_rules)

# Load Best Buy data from CSV file
bestbuy_df = pd.read_csv('Best Buy transactions.csv')
bestbuy_min_support = 0.2
bestbuy_min_confidence = 0.7
bestbuy_frequent_itemsets, bestbuy_rules = preprocess_and_apriori(bestbuy_df, bestbuy_min_support, bestbuy_min_confidence)
print("\nBest Buy Frequent Itemsets:")
print(bestbuy_frequent_itemsets)
print("\nBest Buy Association Rules:")
print(bestbuy_rules)

"""# BRUTE FORCE"""

import itertools
import time
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Function for the brute-force method
def brute_force_frequent_itemsets(transactions, min_support):
    itemsets = set()
    frequent_itemsets = []

    unique_items = set(item for sublist in transactions for item in sublist)

    for k in range(1, len(unique_items) + 1):
        # Generate all possible k-itemsets
        k_itemsets = list(itertools.combinations(unique_items, k))

        # Check support for each k-itemset
        frequent_k_itemsets = [itemset for itemset in k_itemsets if is_frequent(itemset, transactions, min_support)]

        if not frequent_k_itemsets:
            break

        frequent_itemsets.extend(frequent_k_itemsets)
        itemsets.update(frequent_k_itemsets)

    return itemsets

# Function to check support for an itemset
def is_frequent(itemset, transactions, min_support):
    support_count = sum(1 for transaction in transactions if set(itemset).issubset(transaction))
    support = support_count / len(transactions)
    return support >= min_support

# Function to calculate brute force execution time
def brute_force_execution_time(transactions, min_support):
    start_time = time.time()
    brute_force_frequent_itemsets(transactions, min_support)
    return time.time() - start_time

# Function to calculate Apriori algorithm execution time
def apriori_execution_time(transactions, min_support):
    te = TransactionEncoder()
    te_ary = te.fit_transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    start_time = time.time()
    apriori(df, min_support=min_support)
    return time.time() - start_time

# Function to get frequent itemsets using Apriori algorithm
def get_frequent_itemsets(transactions, min_support):
    te = TransactionEncoder()
    te_ary = te.fit_transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    return frequent_itemsets

# Load other datasets from CSV files
amazon_df = pd.read_csv('Amazon transactions.csv')
bestbuy_df = pd.read_csv('Best Buy transactions.csv')
kmart_df = pd.read_csv('Kmart transactions.csv')
nike_df = pd.read_csv('Nike transactions.csv')
generic_df = pd.read_csv('Generic transactions.csv')

# Convert all non-numeric values to strings
amazon_df = amazon_df.applymap(str)
bestbuy_df = bestbuy_df.applymap(str)
kmart_df = kmart_df.applymap(str)
nike_df = nike_df.applymap(str)
generic_df = generic_df.applymap(str)

# Use Amazon data for brute force method
min_support_amazon = 0.2
brute_force_time_amazon = brute_force_execution_time(amazon_df.values, min_support_amazon)
print(f"Brute Force Execution Time for Amazon: {brute_force_time_amazon} seconds")

# Use Best Buy data for brute force method
min_support_bestbuy = 0.2
brute_force_time_bestbuy = brute_force_execution_time(bestbuy_df.values, min_support_bestbuy)
print(f"Brute Force Execution Time for Best Buy: {brute_force_time_bestbuy} seconds")

# Use K-Mart data for brute force method
min_support_kmart = 0.2
brute_force_time_kmart = brute_force_execution_time(kmart_df.values, min_support_kmart)
print(f"Brute Force Execution Time for K-Mart: {brute_force_time_kmart} seconds")

# Use Nike data for brute force method
min_support_nike = 0.2
brute_force_time_nike = brute_force_execution_time(nike_df.values, min_support_nike)
print(f"Brute Force Execution Time for Nike: {brute_force_time_nike} seconds")

# Use Generic data for brute force method
min_support_generic = 0.2
brute_force_time_generic = brute_force_execution_time(generic_df.values, min_support_generic)
print(f"Brute Force Execution Time for Generic: {brute_force_time_generic} seconds")

# Calculate and compare Apriori execution times
apriori_time_amazon = apriori_execution_time(amazon_df, 0.2)
apriori_time_bestbuy = apriori_execution_time(bestbuy_df, 0.2)
apriori_time_kmart = apriori_execution_time(kmart_df, 0.2)
apriori_time_nike = apriori_execution_time(nike_df, 0.2)
apriori_time_generic = apriori_execution_time(generic_df, 0.2)

def apriori_execution_time(transactions, min_support):
    te = TransactionEncoder()
    te_ary = te.fit_transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    start_time = time.time()
    apriori(df, min_support=min_support)
    return time.time() - start_time

apriori_time_amazon = apriori_execution_time(amazon_df.values, 0.2)
apriori_time_bestbuy = apriori_execution_time(bestbuy_df.values, 0.2)
apriori_time_kmart = apriori_execution_time(kmart_df.values, 0.2)
apriori_time_nike = apriori_execution_time(nike_df.values, 0.2)
apriori_time_generic = apriori_execution_time(generic_df.values, 0.2)

print(f"Apriori Execution Time for Amazon: {apriori_time_amazon} seconds")
print(f"Apriori Execution Time for Best Buy: {apriori_time_bestbuy} seconds")
print(f"Apriori Execution Time for K-Mart: {apriori_time_kmart} seconds")
print(f"Apriori Execution Time for Nike: {apriori_time_nike} seconds")
print(f"Apriori Execution Time for Generic: {apriori_time_generic} seconds")