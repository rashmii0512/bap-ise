import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('all_project_data.csv')

def recommend_guides(project_title, df=df):

    # Add the new project title to the DataFrame without using append
    new_df = df._append({'Project Title': project_title}, ignore_index=True)


    # Calculate TF-IDF vectors for the project titles
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(new_df['Project Title'])

    # Calculate cosine similarity of the new project title with all existing project titles
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
    sim_scores = list(enumerate(cosine_sim[0]))

    # Sort the projects based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar projects
    sim_scores = sim_scores[1:11]

    # Get the project indices and scores
    project_indices = [i[0] for i in sim_scores]
    project_scores = [i[1] * 100 for i in sim_scores]

    # Return the top 10 most similar projects' guides along with their similarity scores
    recommended_guides = df['Guide'].iloc[project_indices]
    recommended_df = pd.DataFrame(recommended_guides)
    # add similarity score percentage

    recommended_df['Similarity Score'] = project_scores
    # sort by similarity score
    recommended_df = recommended_df.sort_values(by='Similarity Score', ascending=False)
    # reset index
    recommended_df['index'] = project_indices

    recommended_df = recommended_df.head(3).reset_index(drop=True)
    # return top 3
    return recommended_df


# Load the data

# Test the function with a project title
if __name__ == '__main__':
    project_title = "plant disease identification using machine learning"
    print(recommend_guides(project_title))
# project_title = "plant disease indentification using machine learning"
