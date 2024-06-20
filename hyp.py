import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Hypertension Risk Model',
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state="auto"
)

st.title(":blue[Hypertension Risk Model in a Given Population]")
st.markdown("##")

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io='Hypertension-risk-model-main.xlsx',
        engine='openpyxl',
        sheet_name='HP-one',
        usecols='A:L',
        nrows=4241
    )
    return df
df=get_data_from_excel() 

st.button("Rerun")

st.sidebar.header('Please Filter Here:')
age=st.sidebar.multiselect(
    "Select an age range:",
    options=sorted(df["Age"].unique()),
    default=sorted(df["Age"].unique())
)

currentSmoker=st.sidebar.multiselect(
    "Individuals are current smokers",
    options=sorted(df["CurrentSmoker"].unique()),
    default=sorted(df["CurrentSmoker"].unique())
)

diabetes=st.sidebar.multiselect(
    "Individuals are diabetic patients",
    options=sorted(df["Diabetes"].unique()),
    default=sorted(df["Diabetes"].unique())
)

at_risk=st.sidebar.multiselect(
    "Individuals are at risk of hypertension",
    options=df["Risk_of_Hypertension"].unique(),
    default=df["Risk_of_Hypertension"].unique()
)

df_selection = df.query(
    "Age==@age & CurrentSmoker==@currentSmoker & Diabetes==@diabetes & Risk_of_Hypertension==@at_risk"
)

st.dataframe(df_selection)

#---AVERAGE PARAMETERS----
average_age = int(df_selection['Age'].mean())
average_BMI = round(df_selection['BMI'].mean(),1)
average_cholesterol_level = int(df_selection['totChol'].mean())

left_column,middle_column,right_column = st.columns(3)
with left_column:
    st.write(':violet[Mean of selected ages]:')
    st.write(f"{average_age} years")

with middle_column:
    st.write(':green[Average BMI]:')
    st.write(f"{average_BMI} kg per square meter")

with right_column:
    st.write(":blue[Average cholesterol level] :")
    st.write(f"{average_cholesterol_level} mg/dL")

st.markdown("---")

#--GRAPHS----
st.header(":violet[Graphs Showing the Relationships between Hypertension Risk Factors]", divider='rainbow')
st.markdown("##")

right_column, left_column = st.columns(2)

with right_column:
    chart1 = px.scatter(df_selection,x="cigsPerDay", y="sysBP", title="Cigar sticks smoked per day VRS Systolic Blood Pressure",template="ggplot2")
    st.plotly_chart(chart1)

with left_column:
    chart2=px.scatter(df_selection,x="cigsPerDay", y="heartRate", title="Cigar sticks smoked per day VRS Heart rate",template="plotly")
    st.plotly_chart(chart2)


right_column, left_column = st.columns(2)

with right_column:
    chart3 = px.scatter(df_selection,x="totChol", y="heartRate", title="Total Cholesterol VRS Heart Rate",template="ggplot2")
    st.plotly_chart(chart3)

with left_column:
    chart4=px.scatter(df_selection,x="totChol", y="sysBP", title="Total Cholesterol VRS Systolic Blood Pressure",template="plotly")
    st.plotly_chart(chart4)
