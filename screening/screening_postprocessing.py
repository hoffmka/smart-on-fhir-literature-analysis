import pandas as pd

# Read results from files
df_books = pd.read_excel('screening/screening_books-chapter_done.xlsx')
df_reviews = pd.read_excel('screening/screening_reviews_done.xlsx')
df_articles = pd.read_excel('screening/screening_articles_done.xlsx')

# Concatinate
df = pd.concat([df_books, df_reviews, df_articles], ignore_index=True)
df.to_csv('results/screened_literature.csv')


# Excluded
df_excluded = df[df['Included']==0] # 187 records
print(df_excluded)
# Included
df_included = df[df['Included']==1] # 52 records
print(df_included)

# Key literature elements
df_key_literature = df_included[df_included['further excluded']!=1] # 30 elements
print(df_key_literature)
df_key_literature.to_csv('results/key_literature.csv')


# Convert DataFrame to Markdown format
df_key_literature = df_key_literature[['Authors', 'Title', 'Year', 'DOI', 'Document Type', 'Cited by']]
markdown_table = df_key_literature.to_markdown(index=False)

# Print the Markdown table (or save it to a file if needed)
print(markdown_table)

# Optionally, save to a README.md file
with open('README.md', 'a') as file:  # 'a' to append or 'w' to overwrite
    file.write("\n## KEY LITERATURE OVERVIEW\n\n")
    file.write(markdown_table)
    file.write("\n")