import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

# Set page config
st.set_page_config(
    page_title="Mental Health & Lifestyle Dashboard",
    page_icon="🧠",
    layout="wide"
)

# Apply custom CSS for better styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e0e0ef;
        border-bottom: 2px solid #4e7496;
    }
    .st-cy {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("Mental Health & Lifestyle Dashboard")
st.markdown("Explore the relationship between lifestyle factors and mental health using this interactive dashboard.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Mental_Health_Lifestyle_Dataset.csv")
    
    # Convert Stress Level to numeric for easier analysis
    stress_map = {"Low": 1, "Moderate": 2, "High": 3}
    df["Stress Level Numeric"] = df["Stress Level"].map(stress_map)
    
    return df

df = load_data()

# SIDEBAR
st.sidebar.header("Filters")

# Country filter
countries = sorted(df["Country"].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=countries,
    default=countries
)

# Gender filter
genders = sorted(df["Gender"].unique())
selected_genders = st.sidebar.multiselect(
    "Select Genders",
    options=genders,
    default=genders
)

# Exercise Level filter
exercise_levels = sorted(df["Exercise Level"].unique())
selected_exercise_levels = st.sidebar.multiselect(
    "Select Exercise Levels",
    options=exercise_levels,
    default=exercise_levels
)

# Diet Type filter
diet_types = sorted(df["Diet Type"].unique())
selected_diet_types = st.sidebar.multiselect(
    "Select Diet Types",
    options=diet_types,
    default=diet_types
)

# Mental Health Condition filter
mental_health_conditions = sorted(df["Mental Health Condition"].unique())
selected_mental_health_conditions = st.sidebar.multiselect(
    "Select Mental Health Conditions",
    options=mental_health_conditions,
    default=mental_health_conditions
)

# Filter data based on sidebar selections
filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["Gender"].isin(selected_genders)) &
    (df["Exercise Level"].isin(selected_exercise_levels)) &
    (df["Diet Type"].isin(selected_diet_types)) &
    (df["Mental Health Condition"].isin(selected_mental_health_conditions))
]

# Show filter summary
st.sidebar.markdown("---")
st.sidebar.write(f"Displaying data for {len(filtered_df)} out of {len(df)} individuals")

# Display error if no data after filtering
if filtered_df.empty:
    st.error("No data matches your filter criteria. Please adjust your selections.")
    st.stop()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🧠 Mental Health", "💪 Lifestyle", "🔄 Correlations"])

# TAB 1: OVERVIEW
with tab1:
    st.header("Overview")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Map showing average happiness score by country
        st.subheader("Global Happiness Scores")
        
        country_happiness = filtered_df.groupby("Country")["Happiness Score"].mean().reset_index()
        fig_map = px.choropleth(
            country_happiness, 
            locations="Country",
            locationmode="country names",
            color="Happiness Score",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Viridis,
            title="Average Happiness Score by Country",
            range_color=[1, 10]
        )
        fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_map, use_container_width=True)
        
    with col2:
        # Summary statistics
        st.subheader("Quick Stats")
        
        # Calculate overall average scores
        avg_happiness = filtered_df["Happiness Score"].mean()
        avg_stress = filtered_df["Stress Level Numeric"].mean()
        avg_social = filtered_df["Social Interaction Score"].mean()
        avg_sleep = filtered_df["Sleep Hours"].mean()
        
        # Display metrics
        st.metric("Average Happiness", f"{avg_happiness:.2f}/10")
        st.metric("Average Stress Level", f"{avg_stress:.2f}/3")
        st.metric("Social Interaction", f"{avg_social:.2f}/10")
        st.metric("Sleep Hours", f"{avg_sleep:.2f} hrs")
    
    # Distribution charts
    st.subheader("Demographic and Lifestyle Distributions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        gender_counts = filtered_df["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        
        fig_gender = px.pie(
            gender_counts, 
            values="Count", 
            names="Gender",
            title="Gender Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        fig_gender.update_layout(height=350)
        st.plotly_chart(fig_gender, use_container_width=True)
        
        # Diet Type distribution
        diet_counts = filtered_df["Diet Type"].value_counts().reset_index()
        diet_counts.columns = ["Diet Type", "Count"]
        
        fig_diet = px.bar(
            diet_counts,
            x="Diet Type",
            y="Count",
            color="Diet Type",
            title="Diet Type Distribution",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_diet.update_layout(height=350, xaxis_title="", yaxis_title="Number of People")
        st.plotly_chart(fig_diet, use_container_width=True)
        
    with col2:
        # Exercise Level distribution
        exercise_counts = filtered_df["Exercise Level"].value_counts().reset_index()
        exercise_counts.columns = ["Exercise Level", "Count"]
        
        fig_exercise = px.bar(
            exercise_counts,
            x="Exercise Level",
            y="Count",
            color="Exercise Level",
            title="Exercise Level Distribution",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_exercise.update_layout(height=350, xaxis_title="", yaxis_title="Number of People")
        st.plotly_chart(fig_exercise, use_container_width=True)
        
        # Mental Health Condition distribution
        mh_counts = filtered_df["Mental Health Condition"].value_counts().reset_index()
        mh_counts.columns = ["Mental Health Condition", "Count"]
        
        fig_mh = px.bar(
            mh_counts,
            x="Mental Health Condition",
            y="Count",
            color="Mental Health Condition",
            title="Mental Health Condition Distribution",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_mh.update_layout(height=350, xaxis_title="", yaxis_title="Number of People")
        st.plotly_chart(fig_mh, use_container_width=True)

# TAB 2: MENTAL HEALTH
with tab2:
    st.header("Mental Health Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Mental Health Conditions by Country
        st.subheader("Mental Health Conditions by Country")
        
        # Choose a visualization type
        viz_type = st.radio(
            "Select visualization type:",
            ["Stacked Bar Chart", "Grouped Bar Chart"],
            horizontal=True
        )
        
        mh_by_country = pd.crosstab(
            filtered_df["Country"], 
            filtered_df["Mental Health Condition"],
            normalize="index"
        ) * 100
        
        mh_by_country_long = mh_by_country.reset_index().melt(
            id_vars=["Country"],
            var_name="Mental Health Condition",
            value_name="Percentage"
        )
        
        if viz_type == "Stacked Bar Chart":
            fig_mh_country = px.bar(
                mh_by_country_long,
                x="Country",
                y="Percentage",
                color="Mental Health Condition",
                title="Mental Health Conditions Distribution by Country (%)",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
        else:  # Grouped Bar Chart
            fig_mh_country = px.bar(
                mh_by_country_long,
                x="Country",
                y="Percentage",
                color="Mental Health Condition",
                barmode="group",
                title="Mental Health Conditions Distribution by Country (%)",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
        fig_mh_country.update_layout(height=500, yaxis_title="Percentage (%)")
        st.plotly_chart(fig_mh_country, use_container_width=True)
    
    with col2:
        # Mental Health Conditions by Gender
        st.subheader("Mental Health Conditions by Gender")
        
        mh_by_gender = pd.crosstab(
            filtered_df["Gender"], 
            filtered_df["Mental Health Condition"],
            normalize="index"
        ) * 100
        
        mh_by_gender_long = mh_by_gender.reset_index().melt(
            id_vars=["Gender"],
            var_name="Mental Health Condition",
            value_name="Percentage"
        )
        
        fig_mh_gender = px.bar(
            mh_by_gender_long,
            x="Gender",
            y="Percentage",
            color="Mental Health Condition",
            title="Mental Health Conditions Distribution by Gender (%)",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig_mh_gender.update_layout(height=500, yaxis_title="Percentage (%)")
        st.plotly_chart(fig_mh_gender, use_container_width=True)
    
    # Stress Level vs Happiness Score
    st.subheader("Stress Level vs Happiness Score")
    
    # Add jitter to avoid overlapping points
    filtered_df["Happiness Jitter"] = filtered_df["Happiness Score"] + np.random.normal(0, 0.1, size=len(filtered_df))
    
    fig_stress_happiness = px.scatter(
        filtered_df,
        x="Stress Level",
        y="Happiness Jitter",
        color="Mental Health Condition",
        size="Social Interaction Score",
        hover_name="Country",
        hover_data=["Age", "Gender", "Sleep Hours"],
        title="Relationship between Stress Level and Happiness Score",
        color_discrete_sequence=px.colors.qualitative.G10,
        size_max=15,
        opacity=0.7
    )
    
    fig_stress_happiness.update_layout(
        height=600,
        yaxis_title="Happiness Score",
        xaxis_title="Stress Level",
        yaxis=dict(range=[0, 11])
    )
    
    st.plotly_chart(fig_stress_happiness, use_container_width=True)
    
    # Mental Health by Age Group
    st.subheader("Mental Health by Age Group")
    
    # Create age groups
    bins = [15, 25, 35, 45, 55, 65]
    labels = ["18-25", "26-35", "36-45", "46-55", "56-65"]
    filtered_df["Age Group"] = pd.cut(filtered_df["Age"], bins=bins, labels=labels, right=False)
    
    # Mental health conditions by age group
    mh_by_age = pd.crosstab(
        filtered_df["Age Group"], 
        filtered_df["Mental Health Condition"],
        normalize="index"
    ) * 100
    
    mh_by_age_long = mh_by_age.reset_index().melt(
        id_vars=["Age Group"],
        var_name="Mental Health Condition",
        value_name="Percentage"
    )
    
    fig_mh_age = px.bar(
        mh_by_age_long,
        x="Age Group",
        y="Percentage",
        color="Mental Health Condition",
        title="Mental Health Conditions Distribution by Age Group (%)",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    
    fig_mh_age.update_layout(height=500, yaxis_title="Percentage (%)")
    st.plotly_chart(fig_mh_age, use_container_width=True)

# TAB 3: LIFESTYLE
with tab3:
    st.header("Lifestyle Factors Analysis")
    
    # Select what to compare lifestyle factors against
    compare_by = st.selectbox(
        "Compare lifestyle factors by:",
        ["Mental Health Condition", "Exercise Level", "Stress Level", "Diet Type"]
    )
    
    # Sleep Hours, Screen Time, and Social Interaction boxplots
    st.subheader(f"Lifestyle Metrics by {compare_by}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sleep Hours box plot
        fig_sleep = px.box(
            filtered_df, 
            x=compare_by, 
            y="Sleep Hours",
            color=compare_by,
            title=f"Sleep Hours Distribution by {compare_by}",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_sleep.update_layout(height=400, xaxis_title="", yaxis_title="Sleep Hours")
        st.plotly_chart(fig_sleep, use_container_width=True)
        
        # Social Interaction box plot
        fig_social = px.box(
            filtered_df, 
            x=compare_by, 
            y="Social Interaction Score",
            color=compare_by,
            title=f"Social Interaction Score Distribution by {compare_by}",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_social.update_layout(height=400, xaxis_title="", yaxis_title="Social Interaction Score")
        st.plotly_chart(fig_social, use_container_width=True)
    
    with col2:
        # Screen Time box plot
        fig_screen = px.box(
            filtered_df, 
            x=compare_by, 
            y="Screen Time per Day (Hours)",
            color=compare_by,
            title=f"Screen Time Distribution by {compare_by}",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_screen.update_layout(height=400, xaxis_title="", yaxis_title="Screen Time (Hours)")
        st.plotly_chart(fig_screen, use_container_width=True)
        
        # Work Hours box plot
        fig_work = px.box(
            filtered_df, 
            x=compare_by, 
            y="Work Hours per Week",
            color=compare_by,
            title=f"Work Hours Distribution by {compare_by}",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_work.update_layout(height=400, xaxis_title="", yaxis_title="Work Hours per Week")
        st.plotly_chart(fig_work, use_container_width=True)
    
    # Happiness Score by Lifestyle Factors
    st.subheader("Happiness Score by Lifestyle Factors")
    
    # Create a figure with subplots
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("By Exercise Level", "By Diet Type", "By Sleep Hours"),
        shared_yaxes=True
    )
    
    # Happiness by Exercise Level
    exercise_happiness = filtered_df.groupby("Exercise Level")["Happiness Score"].mean().reset_index()
    fig.add_trace(
        go.Bar(
            x=exercise_happiness["Exercise Level"],
            y=exercise_happiness["Happiness Score"],
            marker_color=px.colors.qualitative.Vivid[:3],
            name="Exercise Level"
        ),
        row=1, col=1
    )
    
    # Happiness by Diet Type
    diet_happiness = filtered_df.groupby("Diet Type")["Happiness Score"].mean().reset_index()
    fig.add_trace(
        go.Bar(
            x=diet_happiness["Diet Type"],
            y=diet_happiness["Happiness Score"],
            marker_color=px.colors.qualitative.Bold[:5],
            name="Diet Type"
        ),
        row=1, col=2
    )
    
    # Happiness by Sleep Hours (binned)
    filtered_df["Sleep Bin"] = pd.cut(
        filtered_df["Sleep Hours"],
        bins=[0, 4, 6, 8, 12],
        labels=["<4 hrs", "4-6 hrs", "6-8 hrs", ">8 hrs"]
    )
    sleep_happiness = filtered_df.groupby("Sleep Bin")["Happiness Score"].mean().reset_index()
    fig.add_trace(
        go.Bar(
            x=sleep_happiness["Sleep Bin"],
            y=sleep_happiness["Happiness Score"],
            marker_color=px.colors.sequential.Viridis[:4],
            name="Sleep Hours"
        ),
        row=1, col=3
    )
    
    # Update layout
    fig.update_layout(
        height=500,
        showlegend=False,
        title_text="Average Happiness Score by Different Lifestyle Factors",
        yaxis_title="Avg. Happiness Score",
        yaxis=dict(range=[0, 10])
    )
    
    # Display the figure
    st.plotly_chart(fig, use_container_width=True)

# TAB 4: CORRELATIONS
with tab4:
    st.header("Correlation Analysis")
    
    # Create a correlation matrix
    numeric_cols = [
        "Age", "Sleep Hours", "Work Hours per Week", 
        "Screen Time per Day (Hours)", "Social Interaction Score", 
        "Happiness Score", "Stress Level Numeric"
    ]
    
    corr_matrix = filtered_df[numeric_cols].corr()
    
    # Create heatmap
    st.subheader("Correlation Heatmap")
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=px.colors.diverging.RdBu_r,
        color_continuous_midpoint=0,
        title="Correlation between Numeric Variables"
    )
    
    fig_corr.update_layout(height=600)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Scatter plot matrix
    st.subheader("Scatter Plot Matrix")
    
    selected_vars = st.multiselect(
        "Select variables to include in the scatter plot matrix:",
        options=numeric_cols,
        default=["Sleep Hours", "Social Interaction Score", "Happiness Score", "Stress Level Numeric"]
    )
    
    if len(selected_vars) > 1:
        fig_scatter_matrix = px.scatter_matrix(
            filtered_df,
            dimensions=selected_vars,
            color="Mental Health Condition",
            opacity=0.6,
            title="Scatter Plot Matrix of Selected Variables",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig_scatter_matrix.update_layout(
            height=800,
            width=800
        )
        
        fig_scatter_matrix.update_traces(diagonal_visible=False)
        st.plotly_chart(fig_scatter_matrix, use_container_width=True)
    else:
        st.warning("Please select at least 2 variables for the scatter plot matrix.")
    
    # Linear regression analysis
    st.subheader("Relationship Explorer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_var = st.selectbox("Select X variable:", numeric_cols)
    
    with col2:
        y_var = st.selectbox(
            "Select Y variable:", 
            [col for col in numeric_cols if col != x_var],
            index=numeric_cols.index("Happiness Score") if x_var != "Happiness Score" else 0
        )
    
    color_var = st.radio(
        "Color points by:",
        ["Mental Health Condition", "Exercise Level", "Diet Type", "Country", "Gender"],
        horizontal=True
    )
    
    # Create the scatter plot with trendline
    fig_regression = px.scatter(
        filtered_df,
        x=x_var,
        y=y_var,
        color=color_var,
        trendline="ols",
        trendline_color_override="black",
        title=f"Relationship between {x_var} and {y_var}",
        color_discrete_sequence=px.colors.qualitative.Bold,
        opacity=0.7
    )
    
    fig_regression.update_layout(height=600)
    st.plotly_chart(fig_regression, use_container_width=True)
    
    # Show trendline formula and R-squared
    import statsmodels.api as sm
    
    X = filtered_df[x_var]
    X = sm.add_constant(X)
    y = filtered_df[y_var]
    
    model = sm.OLS(y, X).fit()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Correlation Coefficient", f"{filtered_df[x_var].corr(filtered_df[y_var]):.3f}")
    
    with col2:
        st.metric("R-squared", f"{model.rsquared:.3f}")
    
    with st.expander("View Regression Details"):
        st.code(model.summary())

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>Mental Health & Lifestyle Dashboard | Created with Streamlit and Plotly</p>
    </div>
    """,
    unsafe_allow_html=True
)
