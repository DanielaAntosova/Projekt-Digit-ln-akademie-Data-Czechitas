import pandas as pd
from collections import Counter

# Load the dataset
data = pd.read_csv('Spojeni_rating_basics (1).csv')

# Define the set of color adjectives to look for
color_adjectives = {'blue', 'green', 'red', 'yellow', 'black', 'white', 'pink', 'purple', 'orange', 'brown', 'gray', 'turquoise', 'gold', 'silver'}

# Extract all color adjectives from the 'primaryTitle' column, handling NaN values and non-string types
all_color_words = []
for title in data['primaryTitle']:
    if isinstance(title, str):  # Check if title is a string
        words = title.split()  # Split title into words
        all_color_words.extend([word.lower() for word in words if word.lower() in color_adjectives])

# Count occurrences of color adjectives
color_count = Counter(all_color_words)

# Calculate total occurrences of color adjectives
total_color_words = sum(color_count.values())

# Calculate percentages for each color, rounding to one decimal place
if total_color_words > 0:
    color_percentages = {color: round((count / total_color_words) * 100, 1) for color, count in color_count.items()}
else:
    color_percentages = {}

# Create DataFrame for readability
color_percentages_df = pd.DataFrame(list(color_percentages.items()), columns=['Color', 'Percentage'])
color_percentages_df.sort_values(by='Percentage', ascending=False, inplace=True)

# Save the DataFrame to a CSV file
color_percentages_df.to_csv('movies_colors.csv', index=False)

# Display the DataFrame
print(color_percentages_df)
