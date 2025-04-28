# File: student_performance_app/main.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Title
st.title("📘 Student Habits vs Academic Performance Dashboard")

# File uploader
dataset = r"D:\Python\Data_Area\student_habits_performance.csv"#st.file_uploader("Upload Student Habits CSV", type=["csv"])

if dataset:
    # Read CSV
    df = pd.read_csv(dataset)

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # Basic info
    st.write(f"Shape of dataset: {df.shape}")
    st.write("Null Values:")
    st.dataframe(df.isnull().sum())

    # Data Processing
    numeric_cols = ['study_hours_per_day', 'mental_health_rating', 'social_media_hours', 'netflix_hours', 'attendance_percentage', 'sleep_hours', 'exercise_frequency', 'exam_score']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')


    if all(col in df.columns for col in numeric_cols):
        df['Overall Habit Score'] = df[numeric_cols].mean(axis=1)

        def categorize_performance(score):
            if score >= 25:
                return 'Excellent'
            elif score >= 20:
                return 'Good'
            elif score >= 18:
                return 'Average'
            else:
                return 'Needs Improvement'

        df['Habit Category'] = df['Overall Habit Score'].apply(categorize_performance)

        st.subheader("Processed Data Preview")
        st.dataframe(df.head())

        # Sidebar filters
        st.sidebar.header("Filter Options")
        if 'gender' in df.columns:
            gender_filter = st.sidebar.multiselect("Select gender", options=df['gender'].unique(), default=df['gender'].unique())
        else:
            gender_filter = []

        if 'diet_quality' in df.columns:
            diet_filter = st.sidebar.multiselect("Select diet_quality", options=df['diet_quality'].unique(), default=df['diet_quality'].unique())
        else:
            diet_filter = []

        if 'age' in df.columns:
            age_filter = st.sidebar.multiselect("Select Age ",options=df['age'].unique(),default = df['age'].unique())
        else:
            age_filter=[]
            


        filtered_df = df.copy()
        if gender_filter:
            filtered_df = filtered_df[filtered_df['gender'].isin(gender_filter)]
        if diet_filter:
            filtered_df = filtered_df[filtered_df['diet_quality'].isin (diet_filter)]
        if age_filter:
            filtered_df = filtered_df[filtered_df['age'].isin (age_filter)]

        # Dashboard Plots
        st.subheader("Overall Habit Score Distribution")
        fig1 = px.histogram(filtered_df, x='Overall Habit Score', nbins=10, title='Overall Habit Score Distribution')
        st.plotly_chart(fig1)

        st.subheader("Average Habit Metrics")
        avg_scores = filtered_df[numeric_cols].mean().reset_index()
        avg_scores.columns = ['Metric', 'Average Score']
        fig2 = px.bar(avg_scores, x='Metric', y='Average Score', title='Average Habit Metrics')
        st.plotly_chart(fig2)

        st.subheader("Habit Category Distribution")
        habit_counts = filtered_df['Habit Category'].value_counts().reset_index()
        habit_counts.columns = ['Habit Category', 'Count']
        fig3 = px.pie(habit_counts, names='Habit Category', values='Count', title='Habit Category Distribution')
        st.plotly_chart(fig3)

        if 'exam_score' in df.columns:
            st.subheader("Exam Score vs Overall Habit Score")
            fig4 = px.scatter(filtered_df, x='Overall Habit Score', y='exam_score', color='Habit Category', title='Exam Score vs Habit Score')
            st.plotly_chart(fig4)


        if 'exam_score' in df.columns:
            st.subheader("Exam Score vs Hours of Study")
            fig4 = px.scatter(filtered_df, x='study_hours_per_day', y='exam_score', color='Habit Category', title='Exam Score vs study hours/day')
            st.plotly_chart(fig4)

        # Download processed CSV
        st.subheader("Download Processed Data")
        processed_csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Processed CSV", data=processed_csv, file_name='processed_student_habits.csv', mime='text/csv')

    else:
        st.error("Dataset missing required numeric columns: " + ", ".join(numeric_cols))
        st.stop()

else:
    st.info("Awaiting for CSV file to be uploaded.")

# End
