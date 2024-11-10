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
# Write to file
df_reset.to_excel('screening/screening.xlsx', index=False)
# Books and Book chapter (n=59)
df_books = df_reset[df_reset["Document Type"].isin(["Book", "Book chapter"])]
df_books.to_excel('screening/screening_books-chapter.xlsx', index=False)
# Review (n=114)
df_review = df_reset[df_reset["Document Type"].isin(["Review"])]
df_review.to_excel('screening/screening_reviews.xlsx', index=False)
# Journal Article (n=401)
df_article = df_reset[df_reset["Document Type"].isin(["Article"])]
df_article.to_excel('screening/screening_articles.xlsx', index=False)
# Conference papers (n=101)
df_conference = df_reset[df_reset["Document Type"].isin(["Conference paper"])]
df_conference.to_excel('screening/screening_conference.xlsx', index=False)
# Others (n=24)
df_others = df_reset[df_reset["Document Type"].isin(['Letter', 'Editorial', 'Note', 'Short survey'])]
df_others.to_excel('screening/screening_others.xlsx', index=False)