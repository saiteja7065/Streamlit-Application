"""
dashboard.py - Analytics dashboard for Note-to-Task AI
"""
import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(tasks):
    if not tasks:
        st.info('No tasks to analyze.')
        return
    df = pd.DataFrame(tasks)
    total = len(df)
    completed = df['done'].sum()
    st.subheader('Progress')
    st.progress(completed / total if total else 0)
    st.write(f"{completed} of {total} tasks completed.")
    # Priority Pie
    st.subheader('Priority Distribution')
    fig1 = px.pie(df, names='priority', title='Task Priorities')
    st.plotly_chart(fig1, use_container_width=True)
    # Category Bar
    st.subheader('Category Distribution')
    cat_counts = df['category'].value_counts().reset_index()
    cat_counts.columns = ['category', 'count']
    fig2 = px.bar(cat_counts, x='category', y='count', labels={'category':'Category','count':'Count'})
    st.plotly_chart(fig2, use_container_width=True)
