import pandas as pd

# Read results from csv
df = pd.read_csv('data/overall.csv')
print(df.columns)

# Sort by 'document_type' and then by 'year'
document_type_order = ['Book', 'Book chapter', 'Review', 'Article', 'Conference paper', 'Letter', 'Editorial', 'Note', 'Short survey']
df['Document Type'] = pd.Categorical(df['Document Type'], categories=document_type_order, ordered=True)
df_sorted = df.sort_values(by=['Document Type','Cited by', 'Year'])

# Reset the index and create a new sequential index
df_reset = df_sorted.reset_index(drop=True)
# Create a new column 'id' with the current index values
df_reset['id'] = df_reset.index

# Move 'id' column to the first position
cols = ['id'] + [col for col in df_reset.columns if col != 'id']
df_reset = df_reset[cols]

# Drop unneccesary columns
df_reset = df_reset.drop(columns=['Author full names', 'Author(s) ID', 'Volume', 'Issue', 'Art. No.', 'Page start', 'Page end', 'Page count', 'Funding Texts', 'Correspondence Address', 'Sponsors', 'Conference code', 'ISSN', 'ISBN', 'CODEN', 'PubMed ID', 'Language of Original Document', 'EID', 'Link', 'Source'])

############################################################
# Write to csv and excel
df_reset.to_excel('data/screening.xlsx', index=False)
df_reset.to_csv('data/screening.csv', index=False)


# Inclusion and exclusion keywords
inclusion_keywords = ["SMART on FHIR", "FHIR", "clinical decision support", "Infrastructure", "implementation", "deployment"]
exclusion_keywords = ["machine learning", "veterinary", "sports", "music"]