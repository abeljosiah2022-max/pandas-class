#Working on Dashboard using Streamlit

#1. Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px


#2. Set page configuration
st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="👤",
    layout="wide"
)


@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/employee_clean_data.csv")
        return df
    except FileExistsError as e:
        st.warning(f'An Error Occured: {e}')


def create_sidebar_filters(df):
    st.sidebar.header("Employee Filter")

    department = st.sidebar.multiselect(
        "Select Department(s)",
        options=df['department'].unique(),
        default=df['department'].unique()
    )

    location = st.sidebar.multiselect(
        "Select Location(s)",
        options=df['office_location'].unique(),
        default=df['office_location'].unique()
    )

    remote = st.sidebar.radio(
        "Select Remote(s)",
        options=['All', 'Yes', 'No'],
        index=0
    )

    return department, location, remote

#Create filter connection
def filter_data(df, department, location, remote):
    filtered_df = df[df['department'].isin(department) & df['office_location'].isin(location)]
    if remote != "All":
        filtered_df = filtered_df[filtered_df['remote'] == remote]
    return filtered_df


#Create KPI
def display_metrics(filtered_df):
    col1, col2, col3, col4 = st.columns(4)


    #What the KPI should display
    with col1:
        st.metric('👤 Total Employee', len(filtered_df))

    with col2:
        avg_salary = filtered_df['salary'].mean() if len(filtered_df) > 0 else 0
        st.metric("💰Average Salary", f'${avg_salary:,.2f}')

    with col3:
        avg_performance = filtered_df['performance'].mean() if len(filtered_df) > 0 else 0
        st.metric("📈 Average Performance", f'{avg_performance:.1f}')

    with col4:
        remote_pct = (filtered_df['remote'] == "Yes").sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.metric("👷 Remote Worker", f"{remote_pct:.1f}%")

#Creating Charts
def display_charts(filtered_df):
    if len(filtered_df) == 0:
        st.warning('No Filter Data Display. Please Adjust Selection')
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Employee Distribution By Department')
        dept_count = filtered_df['department'].value_counts()
        fig1 =px.pie(
            values=dept_count.values,
            names=dept_count.index,
        hole=0.4
        )
        st.plotly_chart(fig1, width='stretch')
    
    with col2:
        st.subheader('Average Salary By Department')
        avg_salary = filtered_df.groupby('department')['salary'].mean().sort_values(ascending=False)
        fig2 = px.bar(
            x=avg_salary.values,
            y=avg_salary.index,
        )
        fig2.update_layout(
            xaxis_title='Salary',
            yaxis_title='Finance'
        )
        st.plotly_chart(fig2, width='stretch')
    
    col3, col4 = st.columns(2)

    with col3:
        st.subheader('Performance Distribution')
        fig3 =px.histogram(
            filtered_df, x='performance', nbins=6
        )
        fig3.update_traces(
            marker_line_color='white',
            marker_line_width=1
        )

        fig3.update_layout(
            xaxis_title='Performance',
            yaxis_title='Count'
        )
        st.plotly_chart(fig3, width='stretch')
    
    with col4:
        st.subheader('Employee By Location')
        location_count = filtered_df['office_location'].value_counts()
        fig4 = px.bar(
            x=location_count.index,
            y=location_count.values
        )
        fig4.update_layout(
            xaxis_title='Office Location',
            yaxis_title='Count'
        )
        st.plotly_chart(fig4, width='stretch')

#Display Table
def display_table_data(filtered_df):
    if len(filtered_df) > 0:
        st.dataframe(filtered_df, width='stretch', height=300)
    else:
        st.warning('No Employee Data To Display')

#Create control
def main():
    #load data
    df = load_data()

    #sidebar call
    department, location, remote = create_sidebar_filters(df)

    #Filtered Data
    filtered_df = filter_data(df, department, location, remote)

    st.title('Employee Dashboard')
    st.markdown('---')

    #call filter
    display_metrics(filtered_df)

    #Display Chart
    st.markdown("---")
    display_charts(filtered_df)

    #Display dataframe
    st.markdown("---")
    display_table_data(filtered_df)


main()


