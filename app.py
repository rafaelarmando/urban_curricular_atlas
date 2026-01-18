import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Urban Curriculum Atlas", layout="wide")

# Sidebar
st.sidebar.image("https://www.urbanschool.org/uploaded/logos/urban_logo_blue_sm.png", width=150)
st.sidebar.title("Curriculum Atlas")
st.sidebar.info("Multi-Departmental Audit")
st.sidebar.markdown("""
**Departments Loaded:**
* 📐 Math
* 🧬 Science
* 🏛️ History
""")

# --- 2. DATA LOADING (Parsed from your specific texts) ---
@st.cache_data
def load_curriculum():
    data = [
        # --- MATH (Previously Loaded) ---
        {"Course": "Math 1A/1B", "Dept": "Math", "Type": "Required", "DEIB Focus": "Medium", "DEIB Tag": "Inclusive Pedagogy", "Homework (Hrs)": 2.5},
        {"Course": "Math 2A/2B", "Dept": "Math", "Type": "Required", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 3.0},
        {"Course": "Math 3A/3B", "Dept": "Math", "Type": "Required", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 3.5},
        {"Course": "Data Science", "Dept": "Math", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "Ethics & Bias", "Homework (Hrs)": 3.5},
        {"Course": "Statistics", "Dept": "Math", "Type": "Elective", "DEIB Focus": "Medium", "DEIB Tag": "Social Science Data", "Homework (Hrs)": 3.0},
        {"Course": "UAS Calculus", "Dept": "Math", "Type": "UAS (Adv)", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 5.5},
        {"Course": "UAS Infinity", "Dept": "Math", "Type": "UAS (Adv)", "DEIB Focus": "Medium", "DEIB Tag": "Philosophy", "Homework (Hrs)": 5.0},

        # --- SCIENCE (Parsed from new text) ---
        {"Course": "Fundamentals of Science 1", "Dept": "Science", "Type": "Required", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 2.5},
        {"Course": "Fundamentals of Science 2", "Dept": "Science", "Type": "Required", "DEIB Focus": "Medium", "DEIB Tag": "Evolution/Genetics", "Homework (Hrs)": 3.0},
        {"Course": "Applied Physics: Electronics", "Dept": "Science", "Type": "Elective", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 2.5},
        {"Course": "Marine Biology", "Dept": "Science", "Type": "Elective", "DEIB Focus": "Medium", "DEIB Tag": "Environmental Justice", "Homework (Hrs)": 3.0},
        {"Course": "Neuroscience", "Dept": "Science", "Type": "Elective", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 3.5},
        {"Course": "Climate Change: Challenges", "Dept": "Science", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "Social Justice", "Homework (Hrs)": 3.0},
        {"Course": "UAS Adv Biology: Genetics", "Dept": "Science", "Type": "UAS (Adv)", "DEIB Focus": "High", "DEIB Tag": "Bioethics/Race", "Homework (Hrs)": 5.0},
        {"Course": "UAS Adv Biology: Infectious Disease", "Dept": "Science", "Type": "UAS (Adv)", "DEIB Focus": "High", "DEIB Tag": "Global Health Equity", "Homework (Hrs)": 5.0},
        {"Course": "UAS Adv Chemistry", "Dept": "Science", "Type": "UAS (Adv)", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 6.0},
        {"Course": "UAS Adv Physics: Mechanics", "Dept": "Science", "Type": "UAS (Adv)", "DEIB Focus": "Low", "DEIB Tag": "None", "Homework (Hrs)": 5.5},
        {"Course": "UAS Env Sci: Physical Resources", "Dept": "Science", "Type": "UAS (Adv)", "DEIB Focus": "High", "DEIB Tag": "Sustainability", "Homework (Hrs)": 4.5},

        # --- HISTORY (Parsed from new text - High DEIB) ---
        {"Course": "World History A (Ottoman)", "Dept": "History", "Type": "Required", "DEIB Focus": "High", "DEIB Tag": "Religious Minorities", "Homework (Hrs)": 3.0},
        {"Course": "World History B (Japan)", "Dept": "History", "Type": "Required", "DEIB Focus": "High", "DEIB Tag": "Non-Western Perspectives", "Homework (Hrs)": 3.0},
        {"Course": "UAS Making America", "Dept": "History", "Type": "Required", "DEIB Focus": "High", "DEIB Tag": "Indigeneity/Slavery", "Homework (Hrs)": 4.5},
        {"Course": "UAS Remaking America", "Dept": "History", "Type": "Required", "DEIB Focus": "High", "DEIB Tag": "Civil Rights", "Homework (Hrs)": 4.5},
        {"Course": "UAS Asian American History", "Dept": "History", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "Race & Resistance", "Homework (Hrs)": 4.0},
        {"Course": "UAS Race in Latin Am. History", "Dept": "History", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "Colonialism/Race", "Homework (Hrs)": 4.0},
        {"Course": "History of Queer Theater", "Dept": "History", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "LGBTQ+", "Homework (Hrs)": 3.5},
        {"Course": "South African History", "Dept": "History", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "Anti-Eurocentric", "Homework (Hrs)": 3.5},
        {"Course": "UAS Women's US History", "Dept": "History", "Type": "Elective", "DEIB Focus": "High", "DEIB Tag": "Gender", "Homework (Hrs)": 4.0},
        {"Course": "UAS Modern Middle East", "Dept": "History", "Type": "Elective", "DEIB Focus": "Medium", "DEIB Tag": "Global Conflict", "Homework (Hrs)": 4.5},
        {"Course": "Economics", "Dept": "History", "Type": "Elective", "DEIB Focus": "Medium", "DEIB Tag": "Global Inequality", "Homework (Hrs)": 3.5},
    ]
    return pd.DataFrame(data)

df = load_curriculum()

# --- 3. DASHBOARD UI ---

st.title("Urban School Curriculum Atlas")
st.markdown("### Cross-Departmental Strategic Audit")
st.markdown("""
Using data from the **Math, Science, and History** catalogs to analyze:
1.  **Urban Includes:** Where is DEIB (Diversity, Equity, Inclusion, Belonging) taught?
2.  **Urban Inspires:** Are we balancing Academic Rigor (Homework Load) with Wellness?
""")

tab1, tab2, tab3 = st.tabs(["🌍 DEIB Heatmap", "⚖️ Homework Balance", "🔎 Course Explorer"])

# --- TAB 1: DEIB ANALYSIS ---
with tab1:
    st.header("Mapping 'Urban Includes'")
    st.write("Which departments are carrying the weight of the DEIB strategic plan?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sunburst Chart showing Dept -> Tag -> Course
        fig_sun = px.sunburst(
            df[df['DEIB Focus'] != 'Low'],
            path=['Dept', 'DEIB Tag', 'Course'],
            color='DEIB Focus',
            color_discrete_map={'High': '#00CC96', 'Medium': '#636EFA'},
            title="Distribution of Explicit DEIB Content"
        )
        st.plotly_chart(fig_sun, use_container_width=True)

    with col2:
        st.info("**Strategic Insight:**")
        st.markdown("""
        * **History** is the primary driver of DEIB content (Race, Gender, Colonialism).
        * **Science** has emerging nodes in *Genetics*, *Public Health*, and *Climate Justice*.
        * **Math** offers specific entry points via *Data Ethics*.
        """)

# --- TAB 2: HOMEWORK & WELLNESS ---
with tab2:
    st.header("Mapping 'Urban Inspires' (Wellness Audit)")
    st.write("Comparing homework load across Departments and Course Types.")
    
    # Box Plot for Departmental Comparison
    fig_box = px.box(
        df, 
        x="Dept", 
        y="Homework (Hrs)", 
        color="Dept",
        points="all",
        hover_data=["Course", "Type"],
        title="Homework Load Distribution by Department"
    )
    st.plotly_chart(fig_box, use_container_width=True)
    
    st.divider()
    
    # Scatter Plot for Wellness (Homework vs DEIB)
    st.subheader("The 'Rigor vs. Relevance' Matrix")
    fig_scatter = px.scatter(
        df,
        x="Homework (Hrs)",
        y="Dept",
        size="Homework (Hrs)",
        color="DEIB Focus",
        symbol="Type",
        hover_name="Course",
        title="Identifying High-Load / Low-Relevance Courses",
        height=500
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.warning("**Wellness Watchlist:** Courses with > 5 hours of homework/week.")
    high_load = df[df['Homework (Hrs)'] >= 5.0].sort_values(by="Homework (Hrs)", ascending=False)
    st.dataframe(high_load[['Course', 'Dept', 'Type', 'Homework (Hrs)']], hide_index=True)

# --- TAB 3: DATA TABLE ---
with tab3:
    st.dataframe(df)