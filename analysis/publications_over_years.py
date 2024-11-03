import pandas as pd
import matplotlib.pyplot as plt

# Sample DataFrame (Replace this with your actual DataFrame)
# Assuming 'pub_year' is the column containing the years of publication
df = pd.read_csv('data/merged_data.csv')

# Count the number of publications per year
publication_counts = df['Year'].value_counts().sort_index()
total_publications = publication_counts.sum()

# Plotting the bar chart
plt.figure(figsize=(10, 6))
bars = publication_counts.plot(kind='bar', color='#64AADC')
plt.title('Number of Publications over the Years')
#plt.xlabel('Publication Year')
plt.ylabel('Number of Publications')
plt.xticks(rotation=0)
plt.grid(axis='y')

# Adding total number of publications as annotation
plt.text(0.05, 0.9, f'Total Publications: {total_publications}', 
         fontsize=12, ha='left', va='top', transform=plt.gca().transAxes)

# Adding count on top of each bar
for bar in bars.patches:
    plt.text(bar.get_x() + bar.get_width() / 2, 
             bar.get_height(), 
             int(bar.get_height()), 
             ha='center', 
             va='bottom')  # Adjusts the text position
    
# Show the plot
plt.tight_layout()
plt.savefig('results/figures/publications_over_years.png', format='png', dpi=300, bbox_inches='tight')
plt.show()