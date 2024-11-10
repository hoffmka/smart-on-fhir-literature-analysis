import pandas as pd

# Read results from files
df_books = pd.read_excel('screening/screening_books-chapter_done.xlsx')
df_reviews = pd.read_excel('screening/screening_review_done.xlsx')

# Concatinate
df = pd.concat([df_books, df_reviews], ignore_index=True)
df.to_csv('results/screened_literature.csv')


# Excluded
df_excluded = df[df['Included']==0] # 98 records
# Included
df_included = df[df['Included']==1] # 26 records

# Key literature elements
df_key_literature = df_included[df_included['further excluded']!=1] # 6 elements
df_key_literature.to_csv('results/key_literature.csv')


# Convert DataFrame to Markdown format
markdown_table = df_key_literature.to_markdown(index=False)

# Print the Markdown table (or save it to a file if needed)
print(markdown_table)

# Optionally, save to a README.md file
with open('README.md', 'a') as file:  # 'a' to append or 'w' to overwrite
    file.write("\n## Data Table\n\n")
    file.write(markdown_table)
    file.write("\n")