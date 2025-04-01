import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Welcome to IMDB Dashboard")
#Database Creation
conn = sqlite3.connect('DataScrap.db')
# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS Data (
    
    Title VARCHAR(150),
    Genre VARCHAR(50),
    Rating float,
    Votes TEXT,
    Duration TEXT)''')

# Commit the changes
conn.commit()

df = pd.read_excel('Final.xlsx')
#st.write("Here is a preview of the dataset:")
#st.write(df.head())
###########################################################
# 1.Top Rated Movies

#RATINGS
st.markdown("<h1 style='color: purple;'>Top 10 Movies Based on Rating Count</h1>", unsafe_allow_html=True)


top_10_movies = df.sort_values(by=['Rating'], ascending=False).head(10)
st.write(top_10_movies)

# VOTES
st.markdown("<h1 style='color: purple;'>Top 10 Movies Based on Votes Count</h1>", unsafe_allow_html=True)


top_10_movies = df.sort_values(by=['Votes'], ascending=False).head(10)
st.write(top_10_movies)
#################################################################
#2.Genre Distribution

#df['Genre'] = df['Genre'].str.split(',')

# Flatten the genre list and count occurrences
genre_counts = df.explode('Genre')['Genre'].value_counts()

# Plotting the bar chart
fig, ax = plt.subplots()
genre_counts.plot(kind='bar', ax=ax, color='skyblue')

# Set chart labels
ax.set_title('Count of Movies for Each Genre')
ax.set_xlabel('Movie-Genre')
ax.set_ylabel('Count of Movies')
ax.set_xticklabels(genre_counts.index, rotation=45, ha='right')

# Display the plot in Streamlit
st.markdown("<h1 style='color: purple;'>2.Genre Distribution Dashboard</h1>", unsafe_allow_html=True)



st.pyplot(fig)

######################################################################3

#3.Average Duration by Genre:
st.markdown("<h1 style='color: purple;'>3.Average Duration of Movies by Genre</h1>", unsafe_allow_html=True)


# Example dataset (replace with your actual data)
data = {
    
    'Genre': ['Comedy', 'Adventure', 'Fantasy','Crime'],
    'Duration': [1.22, 1.28, 1.32, 1.28]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Split genres and explode into individual rows
df['Genre'] = df['Genre'].str.split(', ')
df_exploded = df.explode('Genre')

# Calculate average duration for each genre
avg_duration = df_exploded.groupby('Genre')['Duration'].mean().reset_index()

# Create a dropdown to select a genre
selected_genre = st.selectbox('Choose a Genre:', avg_duration['Genre'])

# Display the average duration for the selected genre
avg_duration_value = avg_duration[avg_duration['Genre'] == selected_genre]['Duration'].values[0]
st.write(f'The average duration for {selected_genre} movies is: {avg_duration_value} minutes')

#Create a horizontal bar chart using seaborn
plt.figure(figsize=(8, 6))
sns.barplot(data=avg_duration, x='Duration', y='Genre', palette='viridis')

# Add labels and title to the chart
plt.xlabel('Average Duration (minutes)')
plt.ylabel('Genre')
plt.title('Average Movie Duration Per Genre')

# Show the plot in Streamlit
st.pyplot(plt)

#######################################################################
st.markdown("<h1 style='color: purple;'>4.Voting Trends by Genre</h1>", unsafe_allow_html=True)


data = {
    
    'Genre': ['Comedy', 'Adventure', 'Fantasy','Crime'],
    'Votes': [58530.16, 82241.98, 41490.89, 37787.6]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Split genres and explode into individual rows
df['Genre'] = df['Genre'].str.split(', ')
df_exploded = df.explode('Genre')

# Calculate average duration for each genre
avg_Votes = df_exploded.groupby('Genre')['Votes'].mean().reset_index()

# Create a horizontal bar chart using seaborn
plt.figure(figsize=(8, 6))
sns.barplot(data=avg_Votes, x='Votes', y='Genre', palette='viridis')

# Add labels and title to the chart
plt.xlabel('Average Votes')
plt.ylabel('Genre')
plt.title('Average Voting Counts Per Genre')

# Show the plot in Streamlit
st.pyplot(plt)

############################################################
st.markdown("<h1 style='color: purple;'>5.Rating Distribution</h1>", unsafe_allow_html=True)


df = pd.read_excel('Final.xlsx')
if 'Rating' in df.columns:
    # Display histogram
    st.subheader('Histogram of Movie Ratings')
    fig, ax = plt.subplots()
    ax.hist(df['Rating'].dropna(), bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Histogram of Movie Ratings')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Display boxplot
    st.subheader('Boxplot of Movie Ratings')
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='Rating', ax=ax, color='lightgreen')
    ax.set_title('Boxplot of Movie Ratings')
    st.pyplot(fig)
else:
    st.write("No 'rating' column found in the dataset!")
##########################################################################
st.markdown("<h1 style='color: purple;'>6.Genre-Based Rating Leaders</h1>", unsafe_allow_html=True)



# Find the top-rated movie for each genre
top_rated_movies = df.loc[df.groupby('Genre')['Rating'].idxmax()]

# Define a function to highlight the top-rated movie
def highlight_top_rated(row):
    if row['Title'] in top_rated_movies['Title'].values:
        return ['background-color: yellow'] * len(row)  # Highlight top-rated movie in yellow
    return [''] * len(row)

# Display the table with the highlighted top-rated movies
st.dataframe(df.style.apply(highlight_top_rated, axis=1))

######################################################
#7.Most Popular Genres by Voting
st.markdown("<h1 style='color: purple;'>7.Most Popular Genres by Voting</h1>", unsafe_allow_html=True)



# Split genres and explode into individual rows
df['Genre'] = df['Genre'].str.split(', ')
df_exploded = df.explode('Genre')

# Group by genre and calculate total votes for each genre
genre_votes = df_exploded.groupby('Genre')['Votes'].sum().reset_index()

# Plot the total votes by genre as a pie chart
plt.figure(figsize=(8, 8))
plt.pie(genre_votes['Votes'], labels=genre_votes['Genre'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set3', len(genre_votes)))
plt.title('Total Voting Counts per Genre')

# Display the pie chart in Streamlit
st.pyplot(plt)

####################################################################
#8.Duration Extremes
st.markdown("<h1 style='color: purple;'>8.Duration Extremes</h1>", unsafe_allow_html=True)


df = pd.read_excel('Final.xlsx')
  

            # Find the shortest and longest movies
shortest_movie = df.loc[df['Duration'].idxmin()]  # Movie with minimum duration
longest_movie = df.loc[df['Duration'].idxmax()]  # Movie with maximum duration

            # Display the shortest and longest movies as cards
st.subheader("Shortest Movie")
st.markdown(f"""
                <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; text-align: center;">
                    <h3>{shortest_movie['Title']}</h3>
                    <p><strong>Duration:</strong> {shortest_movie['Duration']} minutes</p>
                </div>
            """, unsafe_allow_html=True)

st.subheader("Longest Movie")
st.markdown(f"""
                <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; text-align: center;">
                    <h3>{longest_movie['Title']}</h3>
                    <p><strong>Duration:</strong> {longest_movie['Duration']} minutes</p>
                </div>
            """, unsafe_allow_html=True)

###################################################################
#9.Ratings by Genre
st.markdown("<h1 style='color: purple;'>9.Ratings by Genre</h1>", unsafe_allow_html=True)

df = pd.read_excel('Final.xlsx')

if isinstance(df['Genre'].iloc[0], str) and ',' in df['Genre'].iloc[0]:
            df['Genre'] = df['Genre'].apply(lambda x: x.split(',')).explode()

        # Convert 'Average Rating' to numeric (coerce errors to NaN)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

        # Drop rows with NaN values in either 'Genre' or 'Average Rating'
df.dropna(subset=['Genre', 'Rating'], inplace=True)


        # Group by 'Genre' and calculate the average rating for each genre
avg_ratings = df.groupby('Genre')['Rating'].mean().reset_index()

        # Pivot the data for heatmap (Genre as rows)
avg_ratings_pivot = avg_ratings.set_index('Genre').T  # Transpose for the heatmap format

        # Create a heatmap using seaborn
plt.figure(figsize=(10, 6))
sns.heatmap(avg_ratings_pivot, annot=True, cmap="coolwarm", cbar=True, linewidths=0.5, fmt=".2f")
        
        
        # Add a title and labels
plt.title("Average Ratings Across Genres", fontsize=16)
plt.xlabel("Genre", fontsize=12)
plt.ylabel("Rating", fontsize=12)

        # Display the heatmap in Streamlit
st.pyplot(plt)

##################################################################3

#10.Correlation Analysis:
# # Convert the 'Rating' and 'Voting Count' columns to numeric, handling errors gracefully
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')

# Drop rows with NaN values in the columns we care about
df.dropna(subset=['Rating', 'Votes'], inplace=True)

 # Create a scatter plot using Seaborn
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Votes', y='Rating')

 # Adding titles and labels
plt.title("Scatter Plot of Ratings vs Voting Count", fontsize=16)
plt.xlabel("Voting Count", fontsize=12)
plt.ylabel("Rating", fontsize=12)

# Display the plot in Streamlit
st.markdown("<h1 style='color: purple;'>10.Correlation Analysis</h1>", unsafe_allow_html=True)

st.pyplot(plt)
########################################################################

#11.User Data
# Display the data in Streamlit
st.markdown("<h1 style='color: green;'>Interactive Filtering Functionality</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color: purple;'>Filter movies based on their runtime</h1>", unsafe_allow_html=True)
# Convert 'Duration' column to numeric (coerce errors to NaN)
df = pd.read_excel('Duration.xlsx')
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')

        # Drop rows where 'Duration' is NaN (missing values)
df['Duration'].fillna(120, inplace=True)
# Convert duration from minutes to hours
#df['Duration (hrs)'] = df['Duration'] / 60

        # Display the unique values for Duration (hrs) to check the conversion
#st.write("Unique values in 'Duration (hrs)':")
#st.write(df['Duration (hrs)'].unique())

        # Allow the user to select a runtime range
runtime_filter = st.selectbox(
            "Select a runtime range:",
            ["< 2 hrs", "2-3 hrs", "> 3 hrs"]
        )

        # Apply the filter based on the selected range
if runtime_filter == "< 2 hrs":
            filtered_df = df[df['Duration'] < 2]
elif runtime_filter == "2-3 hrs":
            filtered_df = df[(df['Duration'] >= 2) & (df['Duration'] <= 3)]
elif runtime_filter == "> 3 hrs":
            filtered_df = df[df['Duration'] > 3]

        # Show the filtered results
st.write(f"Movies with runtime in the selected range: {runtime_filter}")
st.dataframe(filtered_df[['Title', 'Duration']])
####################################################################
#12.User Data
# Display the data in Streamlit
st.title('Filter movies based on IMDbratings')
st.write('Ratings: Filter movies based on IMDbratings')
# Filter the dataset based on the IMDb rating criteria
rating_threshold = st.slider(
            "Select Rating Threshold:",
            0.0, 10.0, 8.0, 0.1
        )

        # Filter movies based on the selected IMDb rating threshold
filtered_df = df[df['Rating'] > rating_threshold]

        # Display filtered results
st.write(f"Movies with Rating greater than {rating_threshold}:")
st.dataframe(filtered_df[['Title', 'Rating']])

#####################################################################   
#13.
# Display the data in Streamlit
st.markdown("<h1 style='color: purple;'>Filter Movies Based on Number of Votes</h1>", unsafe_allow_html=True)
#st.write('Votes: Filter movies based on the number of IMDb votes (e.g., > 100,000).')
# Filter the dataset based on the IMDb votes criteria
# Filter the dataset based on the number of votes
# Convert 'Votes' column to numeric (coerce errors to NaN)
df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')

        # Drop rows where 'Votes' is NaN (missing values)
df.dropna(subset=['Votes'], inplace=True)
vote_threshold = st.slider(
            "Select Minimum Number of Votes:",
            0, int(df['Votes'].max()), 10000, 1000
        )

        # Filter movies based on the selected number of votes threshold
filtered_df = df[df['Votes'] > vote_threshold]

        # Display filtered results
st.write(f"Movies with more than {vote_threshold} votes:")
st.dataframe(filtered_df[['Title', 'Votes']])

#####################################################################
#14.
# Display the data in Streamlit
st.markdown("<h1 style='color: purple;'>Filter Movies by Genre</h1>", unsafe_allow_html=True)
#st.write('Genres: Filter movies based on genre (e.g., Action, Comedy).')
# Display the unique genres available in the 'Genre' column
genres = df['Genre'].unique()
st.write("Available genres:")
st.write(genres)

        # Allow the user to select one or more genres
selected_genres = st.multiselect(
            "Select Genres:",
            genres,
            default=genres.tolist()  # Default to all genres selected
        )

if selected_genres:
            # Filter the dataset based on the selected genres
            filtered_df = df[df['Genre'].isin(selected_genres)]

            # Display the filtered results
            st.write(f"Movies in selected genres: {', '.join(selected_genres)}")
            st.dataframe(filtered_df[['Title', 'Genre']])
else:
            st.write("Please select at least one genre to filter.")

#####################################################################

#Multple Filters
# Using Markdown with HTML to change title color
st.markdown("<h1 style='color: purple;'>Filter Movies Based on Multiple Criteria</h1>", unsafe_allow_html=True)



df=pd.read_excel('Duration.xlsx')

          # Convert 'Duration' to numeric and handle errors (NaN values)
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')
df['Duration'].fillna(120, inplace=True)  # Fill NaN durations with default value (120 minutes)

        # Convert 'Rating' and 'Votes' to numeric
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')

        # Allow the user to filter based on runtime
runtime_filter = st.selectbox(
            "Select a runtime range:",
            ["All", "< 2 hrs", "2-3 hrs", "> 3 hrs"]
        )

        # Filter based on runtime selection
if runtime_filter == "< 2 hrs":
            df = df[df['Duration'] < 2]
elif runtime_filter == "2-3 hrs":
            df = df[(df['Duration'] >= 2) & (df['Duration'] <= 3)]
elif runtime_filter == "> 3 hrs":
            df = df[df['Duration'] > 3]

        # Allow the user to filter based on IMDb rating
min_rating = st.slider("Select minimum IMDb rating:", 0.0, 10.0, 8.0, 0.1)
df = df[df['Rating'] >= min_rating]

        # Allow the user to filter based on the number of votes
min_votes = st.number_input("Minimum number of votes:", min_value=0, value=10000)
df = df[df['Votes'] >= min_votes]

        # Allow the user to select specific genres
genre_filter = st.multiselect(
            "Select genres:",
            options=df['Genre'].unique(),
            default=df['Genre'].unique()[:3]  # Defaulting to the first 3 genres
        )
if genre_filter:
            df = df[df['Genre'].isin(genre_filter)]

        # Show the filtered results
if df.empty:
            st.write("No movies found matching the selected criteria.")
else:
            st.write(f"Filtered Movies (Showing {len(df)} results):")
            st.dataframe(df[['Title', 'Duration', 'Rating', 'Votes', 'Genre']])

#####################################################################

