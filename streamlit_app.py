import requests
import streamlit as st
import pandas as pd
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import main_functions
import plotly.express as px

### Reference ###
# GET data from API call and save to JSON file
# response = requests.get(url).json()
# main_functions.save_to_file(response, "JSON_Files/arts_articles.json")

# Page Configuration
st.set_page_config(
    page_title="Project 1",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/library/api-reference',
        'Report a bug': "https://docs.streamlit.io/library/api-reference",
        'About': "# This is Project 1 for COP 4813 - Prof. Gregory Reis"
    })
st.title("Project 1 - News App")

# API Sidebar Menu
api_selectbox = st.sidebar.selectbox("Select an API:",
                                     options=["", "Top Stories API", "Most Popular Articles"]
                                     )
# Read from api key
nyt_api = main_functions.read_from_file("JSON_Files/api_keys.json")

# Pass api key to dictionary to access the string
nyt_key = nyt_api["nyt_api"]

# Selectbox Switch Statement
match api_selectbox:


    #### Part A - The Top Stories API ####
    case "Top Stories API":

        # Topics SelectBox
        topic = st.selectbox("Choose a topic:",
                             options=["", "arts", "automobiles", "books", "business", "fashion", "food", "health",
                                      "home", "insider", "magazine",
                                      "movies", "nyregion", "opinion", "politics", "realestate", "science", "sports",
                                      "sundayreview",
                                      "technology", "theater", "t-magazine", "travel", "upshot", "us",
                                      "world"])  # Dict of options

        if topic:
            url = "https://api.nytimes.com/svc/topstories/v2/{0}.json?api-key={1}".format(topic, nyt_key)
            response = requests.get(url).json()
            main_functions.save_to_file(response, "JSON_Files/articlesChosenByTheUser.json")  # Save user topic to file
            articlesChosenByTheUser = main_functions.read_from_file("JSON_Files/articlesChosenByTheUser.json")

            abstracts = ""
            for i in articlesChosenByTheUser["results"]:
                abstracts = abstracts + i["abstract"]

            # Tokenize string into words
            words = word_tokenize(abstracts)

            # Remove/filter punctuation from words
            no_punkt = []
            for w in words:
                if w.isalpha():
                    no_punkt.append(w)

            stopwordsEnglish = stopwords.words("english")

            stop_words = set(stopwords.words("english"))

            # Remove stock words
            filtered_list = []
            for w in no_punkt:
                if w not in stopwordsEnglish:
                    filtered_list.append(w)

            print(filtered_list)

            # Dividing the screen into 2 columns
            col1, col2 = st.columns(2, gap="medium")

            # Populating each column
            with col1:
                st.subheader("I - WordCloud")
                max_numbers_of_words = st.slider("Choose a maximum number of words to be displayed", 1, 100, 200)

                # Color Map SelectBox
                cmap = st.selectbox("Choose a colormap",
                                    options=['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn',
                                             'BuGn_r', 'BuPu',
                                             'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r',
                                             'Greens', 'Greens_r',
                                             'Greys', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10',
                                             'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r',
                                             'terrain',
                                             'terrain_r', 'twilight', 'twilight_r', 'twilight_shifted',
                                             'twilight_shifted_r', 'viridis',
                                             'viridis_r', 'winter', 'winter_r'])

                color = st.color_picker("Choose a background color", '#00f900')

                # Frequency Distribution
                # Create histogram and plot data
                st.subheader("II - Frequency Distribution")

                show_plot = st.checkbox("Check here to display the frequency distribution plot")

                # Show Plot and Slider
                if show_plot:
                    # Call method to create a table from data
                    freq_distribution = FreqDist(filtered_list)
                    print(type(freq_distribution))

                    # GET the most common freq data used words from freq_distribution method
                    words_Freq = st.slider("Choose a maximum number of words to be plotted", 1, 10, 20)
                    most_common_words = pd.DataFrame(freq_distribution.most_common(words_Freq))

                    # Create another DataFrame with columns
                    most_common = pd.DataFrame(
                        # create dict
                        {
                            "words": most_common_words[0],  # column 1
                            "count": most_common_words[1]  # column 2
                        }
                    )

                    fig = px.histogram(most_common, x="words", y="count", title="Frequency Distribution", color="count")
                    st.plotly_chart(fig)  # Plotly fig

            with col2:

                # WordCloud
                user_wordcloud = WordCloud(width=1000,
                                           height=1000,
                                           stopwords=stopwordsEnglish,
                                           colormap=cmap,
                                           max_words=max_numbers_of_words,
                                           background_color=color).generate(abstracts)

                fig, ax = plt.subplots()
                plt.imshow(user_wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(fig)

    #### Part B - Most Popular Articles ####
    case "Most Popular Articles":
        st.header("Most Popular Articles")
        st.subheader("I - Comparing Most Shared, Viewed and Emailed Articles")

        # Articles SelectBox
        article_type = st.selectbox("Select your preferred set of articles",
                                    options=["", "shared", "viewed", "emailed"])

        # Age of Articles SelectBox ( in Days)
        num_of_days = st.selectbox("Select the age of your article (in days)",
                                   options=["", "7", "30"])

        if article_type and num_of_days:

            url_2 = "https://api.nytimes.com/svc/mostpopular/v2/{0}/{1}.json?api-key={2}".format(article_type,
                                                                                                 num_of_days, nyt_key)
            response_2 = requests.get(url_2).json()

            main_functions.save_to_file(response_2, "JSON_Files/popularArticles.json")  # Save user topic to file

            popularArticles = main_functions.read_from_file("JSON_Files/popularArticles.json")

            abstracts_2 = ""
            for i in popularArticles["results"]:
                abstracts_2 = abstracts_2 + i["abstract"]

            # Tokenize string into words
            words = word_tokenize(abstracts_2)

            # Remove/filter punctuation from words
            no_punkt = []
            for w in words:
                if w.isalpha():
                    no_punkt.append(w)

            stopwordsEnglish = stopwords.words("english")

            stop_words = set(stopwords.words("english"))

            # Remove stock words
            filtered_list = []
            for w in no_punkt:
                if w not in stopwordsEnglish:
                    filtered_list.append(w)

            print(filtered_list)

            # Dividing the screen into 2 columns
            col1, col2 = st.columns(2, gap="medium")

            # Populating each column
            with col1:

                max_numbers_of_words2 = st.slider("Choose a maximum number of words to be displayed", 1, 100, 200)

                # Color Map SelectBox
                cmap2 = st.selectbox("Choose a colormap",
                                     options=['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn',
                                              'BuGn_r', 'BuPu',
                                              'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r',
                                              'Greens', 'Greens_r',
                                              'Greys', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10',
                                              'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r',
                                              'terrain',
                                              'terrain_r', 'twilight', 'twilight_r', 'twilight_shifted',
                                              'twilight_shifted_r', 'viridis',
                                              'viridis_r', 'winter', 'winter_r'])
                # Color Picker
                color2 = st.color_picker("Choose a background color", '#00f900')

                # Frequency Distribution
                # Create histogram and plot data
                st.subheader("II - Frequency Distribution")

                show_plot2 = st.checkbox("Check here to display the frequency distribution plot")

                # Show Plot and Slider
                if show_plot2:
                    # Call method to create a table from data
                    freq_distribution2 = FreqDist(filtered_list)
                    print(type(freq_distribution2))

                    # GET the most common freq data used words from freq_distribution method
                    words_Freq2 = st.slider("Choose a maximum number of words to be plotted", 1, 10, 20)
                    most_common_words2 = pd.DataFrame(freq_distribution2.most_common(words_Freq2))

                    # Create another DataFrame with columns
                    most_common2 = pd.DataFrame(
                        # create dict
                        {
                            "words": most_common_words2[0],  # column 1
                            "count": most_common_words2[1]  # column 2
                        }
                    )

                    fig2 = px.histogram(most_common2, x="words", y="count", title="Frequency Distribution",
                                        color="count")
                    st.plotly_chart(fig2)  # Plotly fig

                with col2:
                    # WordCloud
                    user_wordcloud2 = WordCloud(width=1000,
                                                height=1000,
                                                stopwords=stopwordsEnglish,
                                                colormap=cmap2,
                                                max_words=max_numbers_of_words2,
                                                background_color=color2).generate(abstracts_2)

                    fig2, ax = plt.subplots()
                    plt.imshow(user_wordcloud2, interpolation='bilinear')
                    plt.axis('off')
                    st.pyplot(fig2)