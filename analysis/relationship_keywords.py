import pandas as pd

# Read results from csv
resultset_df = pd.read_csv('data/screening.csv')

# Fill empty values in Column1 with values from Column2
resultset_df['Author Keywords'] = resultset_df['Author Keywords'].fillna(resultset_df['Index Keywords'])

# check how many records are available without keywords
resultset_df['Author Keywords'].isna().sum()
# n = 30



############################################################
# Write to csv and excel
df_reset.to_excel('data/keywords.xlsx', index=False)
df_reset.to_csv('data/keywords.csv', index=False)


data = {
    'article': resultset_df['Title'],
    'keywords': resultset_df['Author Keywords']
}
df = pd.DataFrame(data)


# Function to harmonize keywords
def harmonize_keywords(keyword_entry):
    if pd.isna(keyword_entry):  # Check for None or NaN
        return []
    elif isinstance(keyword_entry, str):
        # Remove any extra spaces and split by semicolon
        if keyword_entry.startswith("[") and keyword_entry.endswith("]"):
            # If it's a string representation of a list, convert it to a list
            return eval(keyword_entry)  # Use with caution, eval can execute arbitrary code
        else:
            return [kw.strip() for kw in keyword_entry.split(';')]
    return []

# Apply the harmonization function
df['harmonized_keywords'] = df['keywords'].apply(harmonize_keywords)

###############################
# Create a Co-Occurrence Matrix

from itertools import combinations
from collections import Counter

# Flatten the keyword lists and find co-occurrences
print(df['harmonized_keywords'].isna().sum())  # Count of NaN values

valid_keywords = df['harmonized_keywords'].dropna()  # Remove NaN entries
keyword_pairs = []
for keywords in valid_keywords:
    keyword_pairs.extend(combinations(keywords, 2))

# Count each keyword pair
co_occurrences = Counter(keyword_pairs)
filtered_pairs = {pair: count for pair, count in co_occurrences.items() if count > 2}  # filter by threshold

########################
# Create a Network Graph

import networkx as nx
import matplotlib.pyplot as plt

# Create the graph
G = nx.Graph()

# Add edges and nodes with co-occurrence weights
for (kw1, kw2), count in filtered_pairs.items():
    G.add_edge(kw1, kw2, weight=count)

# Draw the network graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, k=0.3)  # Position nodes using the Fruchterman-Reingold force-directed algorithm
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color="lightblue")
nx.draw_networkx_edges(G, pos, width=[G[u][v]['weight']*0.2 for u, v in G.edges()])
nx.draw_networkx_labels(G, pos, font_size=10)
plt.title("Keyword Co-Occurrence Network")

plt.show()