import streamlit as st
import pickle 
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names=[]
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters  

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox('Select a movie to get recommendations on its basis', movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    width = 150  # Set the width of the image
    spacing = 10  # Set the spacing between posters
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0], width=width)
        st.markdown("<style>.st-image img { margin-top: " + str(spacing) + "px; }</style>", unsafe_allow_html=True)
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1], width=width)
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2], width=width)
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3], width=width)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4], width=width)
