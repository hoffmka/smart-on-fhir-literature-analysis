import pandas as pd

# Read results from csv
df = pd.read_csv('data/screening.csv')

# Sorting by Citations
df = df.sort_values("Cited by", ascending=False)
df = df.head(100)

data = {
    'article': df['Title'],
    'keywords': df['Cited by']
}
df = pd.DataFrame(data)
print(df)