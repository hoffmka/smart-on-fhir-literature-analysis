import pandas as pd

# Read results from csv
scopus_df = pd.read_csv('data/scopus.csv')
wos_df = pd.read_excel('data/webofscience.xls')
pubmed_df = pd.read_csv('data/pubmed.csv')

# Rename columns
wos_df = wos_df.rename(columns={'Author Full Names': 'Author full names', 'Article Title': 'Title', 'Publication Year': 'Year', 'Language': 'Language of Original Document'})

pubmed_df = pubmed_df.rename(columns={'Journal/Book': 'Journal', 'Publication Year': 'Year'})

######################################################
# Merging results of Scopus, Web of Science and PubMed
######################################################

######################################################
# Merge wos entries to scorpus
# Create boolean masks for DOI and Title
doi_wos_present_in_scopus = wos_df['DOI'].isin(scopus_df['DOI'])
title_wos_present_in_scopus = wos_df['Title'].str.lower().isin(scopus_df['Title'].str.lower())

# Combine the two conditions
either_present = doi_wos_present_in_scopus | title_wos_present_in_scopus

# Create a new column in wos_df indicating if either DOI or Title is present in scopus_df
wos_df['either_present'] = either_present

# Print the rows where neither DOI nor Title is present
missing_entries_wos = wos_df[~either_present]
print("Entries in wos_df where neither DOI nor Title is present in scopus_df:")
print(missing_entries_wos)
# RESULT: All entries of wos_df are present in scopus_df
########################################################

######################################################
# Merge pubmed entries to scorpus
# Create boolean masks for DOI and Title
doi_pubmed_present_in_scopus = pubmed_df['DOI'].isin(scopus_df['DOI'])
title_pubmed_present_in_scopus = pubmed_df['Title'].str.lower().isin(scopus_df['Title'].str.lower())

# Combine the two conditions
either_present = doi_pubmed_present_in_scopus | title_pubmed_present_in_scopus

# Create a new column in wos_df indicating if either DOI or Title is present in scopus_df
pubmed_df['either_present'] = either_present

# Print the rows where neither DOI nor Title is present
missing_entries_pubmed = pubmed_df[~either_present]
print("Entries in pubmed_df where neither DOI nor Title is present in scopus_df:")
print(missing_entries_pubmed)

# RESULT: 3 entries (id=14, 17, 51) of pubmed_df 
# are not present in scopus_df
########################################################

# Add missing Document types
missing_entries_pubmed.loc[14, 'Document Type'] = 'Article'
missing_entries_pubmed.loc[17, 'Document Type'] = 'Article'
missing_entries_pubmed.loc[51, 'Document Type'] = 'Article'
missing_entries_pubmed['Language of Original Document'] = 'English'

#######################################
# Create a new dataframe for the result
resultset_df = scopus_df

# Get the common columns between resultset_df(scopus_df) and wos_df
common_columns = resultset_df.columns.intersection(missing_entries_pubmed.columns)

# Filter missing entries to only include the columns that exist in scopus_df
missing_entries_filtered = missing_entries_pubmed[common_columns]

# Append the filtered missing entries to scopus_df
resultset_df = pd.concat([resultset_df, missing_entries_filtered], ignore_index=True)

# check for dublicate titles
print(resultset_df['Title'].duplicated().sum())  # Number of duplicate titles in resultset_df

#####################################################
# Write to csv
resultset_df.to_csv('review/results/resultset.csv', index=False)