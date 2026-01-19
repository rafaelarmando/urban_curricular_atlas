import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random
from collections import Counter

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Urban Dean's Dashboard", layout="wide")

# Sidebar
st.sidebar.image("https://www.urbanschool.org/uploaded/logos/urban_logo_blue_sm.png", width=150)
st.sidebar.title("Dean's Command Center")
st.sidebar.markdown("""
**Strategic Modules:**
1. 🌍 **Curriculum Atlas** (DEIB Map)
2. ⚖️ **Wellness Audit** (Homework)
3. 👥 **Equity Check** (Enrollment)
4. 🗣️ **Sentiment** (Report Cards)
""")

# --- 2. DATA LOADING & SIMULATION ENGINE ---
@st.cache_data
def load_master_data():
    # A. THE REAL CURRICULUM (From your texts)
    base_courses = [
        # ================= MATH =================
        {"Course": "Math 1A/1B", "Dept": "Math", "Type": "Required", "DEIB Focus": "Medium", "DEIB Tag": "Inclusive Pedagogy", "Homework (Hrs)": 2.5},
        {"Course": "Math 2A/2B", "Dept": "Math", "Type": "Required", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 3.0},
        {"Course": "Math 3A/3B", "Dept": "Math", "Type": "Required", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 3.5},
        {"Course": "Data Science", "Dept": "Math", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "Ethics & Bias", "Homework (Hrs)": 3.5},
        {"Course": "Statistics", "Dept": "Math", "Type": "Elective", "DEIB Focus": "Medium", "DEIB Tag": "Social Data", "Homework (Hrs)": 3.0},
        {"Course": "UAS Calculus", "Dept": "Math", "Type": "UAS (Adv)", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 5.5},
        {"Course": "UAS CS 3 (AI/ML)", "Dept": "Math", "Type": "UAS (Adv)", "DEIB Focus": "Medium", "DEIB Tag": "Algorithmic Bias", "Homework (Hrs)": 5.0},
        {"Course": "UAS Infinity", "Dept": "Math", "Type": "UAS (Adv)", "DEIB Focus": "Medium", "DEIB Tag": "Philosophy", "Homework (Hrs)": 5.0},
        
        # ================= SCIENCE =================
        {"Course": "Fund. Science 1", "Dept": "Science", "Type": "Required", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 2.5},
        {"Course": "Fund. Science 2", "Dept": "Science", "Type": "Required", "DEIB Focus": "Medium", "DEIB Tag": "Genetics", "Homework (Hrs)": 3.0},
        {"Course": "Marine Biology", "Dept": "Science", "Type": "Elective", "DEIB Focus": "Medium", "DEIB Tag": "Env Justice", "Homework (Hrs)": 3.0},
        {"Course": "Climate Change", "Dept": "Science", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "Social Justice", "Homework (Hrs)": 3.0},
        {"Course": "UAS Adv Physics", "Dept": "Science", "Type": "UAS (Adv)", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 5.5},
        {"Course": "UAS Genetics", "Dept": "Science", "Type": "UAS (Adv)", "DEIB Focus": "High", "DEIB Tag": "Bioethics", "Homework (Hrs)": 5.0},
        {"Course": "UAS Env Sci: Resources", "Dept": "Science", "Type": "UAS (Adv)", "DEIB Focus": "High", "DEIB Tag": "Sustainability", "Homework (Hrs)": 4.5},

        # ================= HISTORY =================
        {"Course": "World History A", "Dept": "History", "Type": "Required", "DEIB Focus": "High", "DEIB Tag": "Non-Western", "Homework (Hrs)": 3.0},
        {"Course": "UAS Making America", "Dept": "History", "Type": "Required", "DEIB Focus": "High", "DEIB Tag": "Indigeneity", "Homework (Hrs)": 4.5},
        {"Course": "UAS Asian Am. History", "Dept": "History", "Type": "UAS (Adv)", "DEIB Focus": "High", "DEIB Tag": "Race & Resistance", "Homework (Hrs)": 4.0},
        {"Course": "History of Queer Theater", "Dept": "History", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "LGBTQ+", "Homework (Hrs)": 3.5},
        {"Course": "Economics", "Dept": "History", "Type": "Elective", "DEIB Focus": "Medium", "DEIB Tag": "Inequality", "Homework (Hrs)": 3.5},
        {"Course": "UAS Women's History", "Dept": "History", "Type": "UAS (Adv)", "DEIB Focus": "High", "DEIB Tag": "Gender", "Homework (Hrs)": 4.5},
    ]

    # B. SIMULATION ENGINE (Adding "Fake" Students & Comments to Real Courses)
    extended_data = []
    
    # Word Banks
    rigorous_words = ["struggle", "challenging", "rigorous", "failed", "complex", "grit", "hard", "potential", "gap"]
    inclusive_words = ["perspective", "voice", "identity", "share", "community", "growth", "brave", "nuance", "lived"]
    standard_words = ["participation", "assignment", "test", "quiz", "consistent", "pleasure", "class", "time", "completed"]

    for c in base_courses:
        # 1. Simulate Enrollment Size
        total_students = random.randint(12, 22)
        
        # 2. Simulate Gender Skew (Logic: STEM Advanced = Male Skew, DEIB/Gender = Female/NB Skew)
        if c['Dept'] in ['Math', 'Science'] and c['Type'] == 'UAS (Adv)':
            male_pct = random.uniform(0.60, 0.85) # Problematic Male Skew
        elif "Women" in c['Course'] or "Queer" in c['Course'] or c['DEIB Tag'] in ["Gender", "LGBTQ+"]:
            male_pct = random.uniform(0.10, 0.30) # Female/NB Skew
        else:
            male_pct = random.uniform(0.40, 0.60) # Balanced

        n_male = int(total_students * male_pct)
        n_nb = random.randint(0, 3) 
        n_female = total_students - n_male - n_nb
        
        # 3. Simulate Comments
        if c['Type'] == 'UAS (Adv)' and c['Dept'] != 'History':
            vocab = rigorous_words + standard_words
        elif c['DEIB Focus'] == "High":
            vocab = inclusive_words + standard_words
        else:
            vocab = standard_words
            
        corpus = [random.choice(vocab) for _ in range(150)]
        
        # Merge it all
        c_copy = c.copy()
        c_copy.update({
            "Total Students": total_students,
            "Male": n_male,
            "Female": n_female,
            "Non-Binary": n_nb,
            "Male %": round(n_male/total_students, 2),
            "Comment Corpus": corpus
        })
        extended_data.append(c_copy)
        
    return pd.DataFrame(extended_data)

df = load_master_data()

# --- 3. DASHBOARD UI ---

st.title("Urban School: Strategic Analytics Dashboard")
st.markdown("Integrating **Curricular Vision** with **Data Science**.")

# CREATE 4 TABS TO HOLD EVERYTHING
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Curriculum Map (DEIB)", 
    "⚖️ Wellness & Rigor", 
    "👥 Enrollment Equity", 
    "🗣️ Sentiment Analysis"
])

# --- TAB 1: CURRICULUM ATLAS (DEIB) ---
with tab1:
    st.header("Mapping 'Urban Includes'")
    st.markdown("Where is Equity explicitly taught?")
    
    # Legend
    leg1, leg2, leg3 = st.columns(3)
    leg1.success("🟢 High Focus (Explicit Equity)")
    leg2.info("🔵 Medium Focus (Integrated)")
    leg3.error("🔴 Low Focus (Standard)")
    
    # Sunburst
    fig_sun = px.sunburst(
        df,
        path=['Dept', 'DEIB Focus', 'Course'],
        values='Homework (Hrs)',
        color='DEIB Focus',
        color_discrete_map={'High': '#00C853', 'Medium': '#2962FF', 'Low': '#D50000'},
        title="Curriculum Audit: DEIB Distribution"
    )
    fig_sun.update_layout(showlegend=False)
    st.plotly_chart(fig_sun, use_container_width=True)

# --- TAB 2: WELLNESS (HOMEWORK) ---
with tab2:
    st.header("Mapping 'Urban Inspires'")
    st.markdown("Balancing Academic Rigor with Student Wellness.")
    
    # Scatter Plot
    fig_scatter = px.scatter(
        df,
        x="Homework (Hrs)",
        y="Dept",
        size="Homework (Hrs)",
        color="DEIB Focus",
        symbol="Type",
        hover_name="Course",
        title="Rigor vs. Relevance Matrix",
        height=500
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.warning("⚠️ **Burnout Risk:** Courses with > 5.0 hours of homework/week:")
    st.dataframe(df[df['Homework (Hrs)'] >= 5.0][['Course', 'Dept', 'Homework (Hrs)']], hide_index=True)

# --- TAB 3: DEMOGRAPHICS (ENROLLMENT) ---
with tab3:
    st.header("Enrollment Equity Audit")
    st.markdown("Simulated gender breakdown to identify 'Gatekeeping' courses.")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        # Stacked Bar
        df_gender = df.melt(id_vars=["Course", "Dept"], value_vars=["Male", "Female", "Non-Binary"], var_name="Gender", value_name="Count")
        fig_gender = px.bar(
            df_gender, 
            x="Course", 
            y="Count", 
            color="Gender", 
            title="Gender Composition by Class",
            color_discrete_map={"Male": "#636EFA", "Female": "#EF553B", "Non-Binary": "#00CC96"}
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with c2:
        st.error("🚩 **Inequity Flags**")
        st.caption("Classes > 65% Male:")
        skewed = df[df['Male %'] > 0.65].sort_values('Male %', ascending=False)
        for _, row in skewed.iterrows():
            st.write(f"**{row['Course']}**")
            st.progress(row['Male %'])

# --- TAB 4: SENTIMENT (COMMENTS) ---
with tab4:
    st.header("Report Card Sentiment Analysis")
    st.markdown("Analyzing the 'Emotional Signature' of our feedback.")
    
    c1, c2 = st.columns(2)
    with c1:
        course_choice = st.selectbox("Select Course:", df['Course'].unique())
        course_row = df[df['Course'] == course_choice].iloc[0]
        
        # Word Frequency
        counts = Counter(course_row['Comment Corpus']).most_common(8)
        common_df = pd.DataFrame(counts, columns=['Word', 'Count'])
        
        fig_words = px.bar(common_df, x='Count', y='Word', orientation='h', title=f"Top Words: {course_choice}")
        fig_words.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_words, use_container_width=True)
        
    with c2:
        st.info("ℹ️ **Strategic Note**")
        if course_row['Dept'] in ['Math', 'Science'] and course_row['Type'] == 'UAS (Adv)':
            st.write("Notice how this advanced STEM course uses words like **'Struggle'** or **'Rigorous'**. Does this language demotivate students?")
        else:
            st.write("Notice the focus on **'Voice'** and **'Identity'**. How can we bring this inclusive language into our STEM courses?")