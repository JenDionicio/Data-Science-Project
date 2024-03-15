# -*- coding: utf-8 -*-
"""Luke Main Spotify_Song_Prediction_Streamlit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dwff7qqFC17gFx5nJuuf5fYVVQJA_JHh
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as mlt
import missingno as mno

# %matplotlib inline

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""Exploratory Data Analysis


1.  Explore the shape and see what type of problem you are solving.
2. Define the problem and shape of the dataet.
3. Look for outliers if any and see its distribution across the columns, along the columns.
4. What type of null you have (Categorical or Numerical).
5. How would fix the null values.

"""

df = pd.read_csv("spotify.csv", encoding = 'ISO-8859-1')

df.describe()

df.info()

df['streams'] = pd.to_numeric(df['streams'], errors='coerce')

mean_value = round(df['streams'].mean())

# Replace string values with the rounded mean
df['streams'] = df['streams'].fillna(mean_value)

# Convert the column to integer type
df['streams'] = df['streams'].astype(int)

mean_value

df.info()

mno.matrix(df, figsize = (20, 6))

df.shape

cleaned_data= df.dropna(subset=['key', 'in_shazam_charts'])
cleaned_data.shape

mno.matrix(cleaned_data, figsize = (20, 6))

"""## Visualization

Analyse the data, try to come up with some intereszting and Insightful visualization.

Come up with different analysis and what do you infer and observe from it:
- **Univariate Analysis of all the Variables**
- **Bi-variate analysis of atleast 3 pair of variables/features**
   1.   Categorical Vs Categorical
   2.   Categorical Vs Numerical
   3.   Numerical Vs Numerical
- **Multi-variate analysis**
- Plot some Pie-Chart as well.
- Some box-plots as well.
"""

# sns.pairplot(cleaned_data)

cols = ['danceability_%', 'key', 'valence_%', 'energy_%']
ratios = cleaned_data[cols]
sns.pairplot(ratios)

columns_to_heatmap = ['streams','bpm','danceability_%','valence_%','energy_%','acousticness_%','instrumentalness_%','liveness_%','speechiness_%']
data_for_heatmap = cleaned_data[columns_to_heatmap]
mlt.figure(figsize=(10, 8))
sns.heatmap(data_for_heatmap.corr(), annot=True, cmap='coolwarm', fmt=".2f")
mlt.title('Heatmap')
mlt.show()

mlt.figure(figsize=(8, 6))
sns.countplot(x="key", data=cleaned_data, palette="Set1")
mlt.xlabel("Keys", fontsize=14)
mlt.ylabel("Count", fontsize=14)
mlt.title("Count of Each Key", fontsize=16)
mlt.show()

"""## Modelling


Build a model that can categorizes restaurants into 'Budget' and 'Expensive' and identify how different features influence the decision. Please explain the findings effectively for technical and non-technical audiences using comments and visualizations, if appropriate.
- **Build an optimized model that effectively solves the business problem.**
- **The model will be evaluated on the basis of Accuracy.**
- **Read the test.csv file and prepare features for testing.**
"""

pd.get_dummies(ratios['key'])

cleaned_data

quantitative_df = cleaned_data.select_dtypes(include=[np.number])
quantitative_df

quantitative_df.info()

cleaned_data.info()

quantitative_df.info()



X = quantitative_df.drop('streams', axis=1)
y = quantitative_df['streams']

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


from sklearn.linear_model import LinearRegression


lin_reg = LinearRegression()
lin_reg.fit(X_train,y_train)


# Optional for...reassurance? coeff_df = pd.DataFrame(lin_reg.coef_, X.columns, columns=['Coefficient'])
# coeff_df


feature_names = [f'Feature_{i}' for i in list(X.columns)]
df_X = pd.DataFrame(X, columns=feature_names)
# Coefficients represent the importance in linear regression
coefficients = lin_reg.coef_


# Making the coefficients positive to compare magnitude
importance = np.abs(coefficients)


# Plotting feature importance with feature names
mlt.figure(figsize=(10, 8))
mlt.barh(feature_names, importance)
mlt.xlabel('Absolute Coefficient Value')
mlt.title('Feature Importance (Linear Regression)')
mlt.show()


pred = lin_reg.predict(X_test)


mlt.figure(figsize=(10,7))
mlt.title("Actual vs. predicted house prices",fontsize=25)
mlt.xlabel("Actual test set house prices",fontsize=18)
mlt.ylabel("Predicted house prices", fontsize=18)
mlt.scatter(x=y_test,y=pred)
print(type(y_test))
print(type(pred))

from sklearn import metrics

print('MAE:', metrics.mean_absolute_error(y_test, pred))
print('MSE:', metrics.mean_squared_error(y_test, pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, pred)))

y_test.info

! pip install streamlit -q

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import seaborn as sns
# import matplotlib.pyplot as plt
# from PIL import Image
# 
# # Loading the dataset
# def load_data():
#     df = pd.read_csv('spotify.csv', encoding='latin-1')
#     return df
# 
# df = load_data()
# 
# # Set the title of the web app
# st.title("Welcome to Spotify's predictive dashboard!")
# 
# 
# # Load an image from file
# image = Image.open('spotify.png')
# 
# # Display the image
# st.image(image, caption='Spotify Image', use_column_width=True)
# 
# 
# 
# # Sidebar - Header
# st.sidebar.header('Select Page')
# 
# # Sidebar - Page selection
# page = st.sidebar.selectbox('Select', ['Background', 'Analysis', 'Predictions'])
# 
# # Display the selected page
# if page == 'Background':
#     # Displaying background information
#     st.subheader('Objectives')
#     st.write("🎯 Spotify is one of the largest music streaming service providers, with over 602 million monthly active users, including 236 million paying subscribers, as of December 2023. The goal of this project is to allow different businesses such as record labels to make data-driven decisions based on the dataset, highlighting key characteristics of hit songs in 2023.")
# 
#     st.subheader('Dataset')
#     st.write("🎯 What Spotify has available is it's most streamed songs in 2023. It provides insights into each song's attributes, popularity, and presence on various music platforms.")
#     st.write(df.head())
#     st.write("Source: https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023")
# 
# elif page == 'Analysis':
#     plt.figure(figsize=(8, 6))
#     sns.countplot(x="key", data=cleaned_data, palette="Set1")
#     plt.xlabel("Keys", fontsize=14)
#     plt.ylabel("Count", fontsize=14)
#     plt.title("Count of Each Key", fontsize=16)
# 
#     # Display the plot in the Streamlit app
#     st.pyplot(plt)
# 
# elif page == 'Predictions':
#     pass
#

!streamlit run app.py & npx localtunnel --port 8501

# image_spoti = image.open('spoti.png'), st.image(image_spoti, width=1000)

!curl ipecho.net/plain