import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie details from TMDb API
def fetch_movie_details(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f0876dce92dd28505b9ec945cb32c688')
    data = response.json()
    return {
        'title': data['title'],
        'poster_path': f"https://image.tmdb.org/t/p/original/{data['poster_path']}",
        'overview': data['overview'],
        'release_date': data['release_date'],
        'genres': [genre['name'] for genre in data['genres']],
        'vote_average': data['vote_average']
    }

# Function to fetch movie poster from TMDb API
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f0876dce92dd28505b9ec945cb32c688')
    data = response.json()    
    return f"https://image.tmdb.org/t/p/original/{data['poster_path']}"

# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_movies = []
    recommend_movie_details = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_details = fetch_movie_details(movie_id)
        recommend_movies.append(movie_details['title'])
        recommend_movie_details.append(movie_details)
    return recommend_movies, recommend_movie_details

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

# Set up Streamlit app title
st.title('🎬 Discover Your Next Favorite Movie! by Arth')

# Note for users regarding API key usage
st.markdown("""
    **Note:** If you encounter issues with the application, it could be due to the usage of a freely available API key, which may have reached its usage limit.
""")

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    'Find the perfect movie for your mood! Select one from the list below:',
    movies['title'].values)

# Button to trigger recommendation
if st.button('Recommend'):
    st.markdown('## Recommendations')
    names, details = recommend(selected_movie_name)
    for movie_name, movie_details in zip(names, details):
        st.subheader(movie_name)
        st.image(movie_details['poster_path'], use_column_width=True)
        st.write(f"**Release Date:** {movie_details['release_date']}")
        st.write(f"**Genres:** {', '.join(movie_details['genres'])}")
        st.write(f"**Average Rating:** {movie_details['vote_average']}")
        st.write(f"**Overview:** {movie_details['overview']}")
        st.markdown("---")
