# movie_recommendation.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample movie dataset
movies = {
    'Movie ID': [1, 2, 3, 4, 5],
    'Title': ['The Matrix', 'The Godfather', 'The Dark Knight', 'Pulp Fiction', 'The Shawshank Redemption'],
    'Description': [
        'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
        'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
        'When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.',
        'The lives of two mob hitmen, a boxer, a gangster’s wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
        'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'
    ]
}

# Convert to DataFrame
df = pd.DataFrame(movies)

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english')

# Transform the descriptions into TF-IDF vectors
tfidf_matrix = vectorizer.fit_transform(df['Description'])

# Calculate cosine similarity between movies
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get movie recommendations based on a given title
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = df.index[df['Title'] == title].tolist()[0]

    # Get pairwise similarity scores for all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the most similar movies
    sim_scores = sim_scores[1:6]  # Exclude the movie itself (index 0)
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 5 most similar movies
    return df['Title'].iloc[movie_indices]

# Test the recommendation system with a sample movie
recommended_movies = get_recommendations('The Matrix')
print("Recommended Movies based on 'The Matrix':")
for movie in recommended_movies:
    print(movie)
