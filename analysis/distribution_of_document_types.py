import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read results from csv
resultset_df = pd.read_csv('data/overall.csv')

# Harmonize Document types from different data sources
resultset_df.loc[resultset_df['Document Type'] == 'Proceedings Paper'] = 'Conference paper'
resultset_df.loc[resultset_df['Document Type'] == 'Article'] = 'Journal Article'
resultset_df.loc[resultset_df['Document Type'] == 'Conference paper'] = 'Conference Paper'
resultset_df.loc[resultset_df['Document Type'] == 'Book chapter'] = 'Book Chapter'

# Count the occurrences of each document type
doc_counts = resultset_df['Document Type'].value_counts()
doc_counts.sum()

# Define your custom order for document types
custom_order = ['Journal Article', 'Conference Paper', 'Review', 'Book', 'Book Chapter', 'Others']

# Define categories to group as "Others"
others_categories = ['Editorial', 'Letter', 'Note', 'Short survey']

# Summarize these categories as 'Others'
doc_counts['Others'] = doc_counts[others_categories].sum()
doc_counts = doc_counts.drop(others_categories)

# Reindex to apply the custom order, filling missing values with 0
doc_counts = doc_counts.reindex(custom_order, fill_value=0)

# Calculate percentages and prepare labels
total = doc_counts.sum()
labels = [f"{label} ({count})" for label, count in zip(doc_counts.index, doc_counts)]
labels[-1] += " *"  # Add asterisk to "Others"

# Define discrete colors for each section
colors = ['#f0826298', '#f7a94198', '#00824498', '#cd161998', '#e8412c98', '#72777798']  # Custom colors for each category

# Plot the pie chart
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(doc_counts, labels=labels, autopct='', colors=colors, startangle=90, counterclock=True, labeldistance=1.15)

# Draw a circle in the middle to make it look like a donut chart
centre_circle = plt.Circle((0,0), 0.60, fc='white')
fig.gca().add_artist(centre_circle)

# Title in the center
plt.text(0, 0, "Publication Type\nDistribution", ha='center', va='center', fontsize=12, weight='bold')

# Add a description for the Others category
text_x = 1.0  # X position for the text
text_y = 1.5  # Y position for the text
plt.text(text_x, text_y, "* includes: Editorial, Letter, Short survey, and Note", ha='center', va='center', fontsize=8)

# Add a description for the Others category
text2_x = 0.0  # X position for the text
text2_y = -1.2  # Y position for the text
plt.text(text2_x, text2_y, "Overall (n=699)", ha='center', va='center', fontsize=8)

# Draw lines from the pie edges to the labels
for i, wedge in enumerate(wedges):
    angle = (wedge.theta1 + wedge.theta2) / 2  # Middle angle of the wedge
    x = np.cos(np.deg2rad(angle)) * 1.1  # Position at the edge of the pie chart
    y = np.sin(np.deg2rad(angle)) * 1.1
    
    # Draw lines to each label
    plt.plot([x, x * 0.9], [y, y * 0.9], color='black', lw=1)  # Line from outer edge to label


# Save plot
plt.savefig('results/figures/distribution_of_document_types.png', format='png', dpi=300, bbox_inches='tight')

plt.show()


