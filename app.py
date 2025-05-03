from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# Create Flask application
app = Flask(__name__)

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

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    titles = df['Title'].tolist()
    close_matches = get_close_matches(title, titles, n=1, cutoff=0.6)

    if not close_matches:
        return None

    matched_title = close_matches[0]
    idx = df.index[df['Title'] == matched_title].tolist()[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]

    return matched_title, df['Title'].iloc[movie_indices]


# Route for home page
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form['movie_title']
    result = get_recommendations(title)

    if result is None:
        message = "No recommendations found. Please check the title or try another movie."
        return render_template('index.html', message=message)

    matched_title, recommendations = result
    return render_template('index.html', title=matched_title, recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)
