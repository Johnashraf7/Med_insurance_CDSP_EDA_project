import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Medical Insurance Analysis", layout="wide")
st.image("basic-health-insurance-not-enough-for-medical-emergencies.jpg")


df = pd.read_csv("medical_insurance_cleaned.csv")


st.sidebar.title("Navigation")

page = st.sidebar.selectbox("Go to page",["About the data", "Demographics & Risk", "Chronic Conditions & Diabetes","Utilization","Plans & Costs"])


if page == "About the data":
    st.title("About the dataset")
    st.markdown('''
| Column name | Explanation |
| --- | --- |
| person_id | Unique identifier for each insured individual in the dataset. |
| age | Age of the person in years at the time of the policy or data snapshot. |
| sex | Biological sex of the person (e.g., Male, Female).  |
| region | Geographic region of residence for the policyholder (e.g., North, Central).  |
| urban_rural | Type of area where the person lives, such as Urban, Suburban, or Rural.  |
| income | Annual income of the individual or household in monetary units.  |
| education | Highest level of education attained (e.g., No HS, HS, Some College, Doctorate).  |
| marital_status | Marital status of the person (e.g., Married, Single, Divorced).  |
| employment_status | Current employment situation (e.g., Employed, Retired, Self-employed, Unemployed).  |
| household_size | Total number of people living in the same household as the insured person.  |
| dependents | Number of dependents financially supported by the insured (often children or other dependents).  |
| bmi | Body Mass Index of the person, a measure of weight relative to height.  |
| smoker | Smoking status category for the person (e.g., Never, Former, Current).  |
| alcohol_freq | Frequency of alcohol consumption (e.g., Daily, Weekly, or blank for none/unknown).  |
| visits_last_year | Number of outpatient or clinic visits the person had in the last 12 months.  |
| hospitalizations_last_3yrs | Count of hospital admissions over the last three years.  |
| days_hospitalized_last_3yrs | Total number of days spent in hospital over the last three years.  |
| medication_count | Number of ongoing prescription medications the person is currently taking.  |
| systolic_bp | Systolic blood pressure value (upper number in a blood pressure reading, in mmHg).  |
| diastolic_bp | Diastolic blood pressure value (lower number in a blood pressure reading, in mmHg).  |
| ldl | Low-density lipoprotein cholesterol level (often called “bad” cholesterol). [1] |
| hba1c | Hemoglobin A1c percentage, indicating average blood glucose level over the past 2–3 months.  |
| plan_type | Type of health insurance plan (e.g., HMO, PPO, POS). [1] |
| network_tier | Benefit or metal tier of the plan’s network (e.g., Bronze, Silver, Gold, Platinum).  |
| deductible | Amount the member must pay out of pocket before the insurance starts covering services.  |
| copay | Fixed amount paid by the insured for each visit or service (e.g., office visit copay).  |
| policy_term_years | Duration of the insurance policy term in years.  |
| policy_changes_last_2yrs | Number of times the policyholder has changed or modified their policy in the last two years.  |
| provider_quality | Summary score capturing the quality rating of the main healthcare provider or network.  |
| risk_score | Composite health risk score summarizing expected medical risk and cost for the person.  |
| annual_medical_cost | Total annual medical cost associated with the person (e.g., allowed or incurred cost).  |
| annual_premium | Total insurance premium charged for the person’s coverage over a year.  |
| monthly_premium | Monthly insurance premium amount derived from or related to the annual premium.  |
| claims_count | Number of insurance claims submitted or processed for the person in the year.  |
| avg_claim_amount | Average monetary amount paid per claim for that person.  |
| total_claims_paid | Total amount paid by the insurer for all claims for that individual.  |
| chronic_count | Number of chronic health conditions the person has (e.g., hypertension, diabetes).  |
| hypertension | Indicator (0/1) showing whether the person has diagnosed high blood pressure.  |
| diabetes | Indicator (0/1) for diagnosed diabetes.  |
| asthma | Indicator (0/1) for diagnosed asthma.  |
| copd | Indicator (0/1) for chronic obstructive pulmonary disease.  |
| cardiovascular_disease | Indicator (0/1) for any cardiovascular disease (e.g., coronary artery disease).  |
| cancer_history | Indicator (0/1) showing whether the person has a past or current history of cancer.   |
| kidney_disease | Indicator (0/1) for chronic kidney disease or significant kidney impairment.  |
| liver_disease | Indicator (0/1) for chronic liver disease or significant liver dysfunction.  |
| arthritis | Indicator (0/1) for arthritis or related joint disease.  |
| mental_health | Indicator (0/1) for a diagnosed mental health condition (e.g., depression, anxiety).  |
| proc_imaging_count | Number of imaging procedures (e.g., X-ray, CT, MRI) performed for the person.  |
| proc_surgery_count | Number of surgical procedures the person has undergone.  |
| proc_physio_count | Number of physiotherapy or physical therapy sessions received.  |
| proc_consult_count | Number of specialist or physician consultation visits.  |
| proc_lab_count | Number of laboratory tests or lab panels done for the person.  |
| is_high_risk | Flag (0/1) indicating whether the person is classified as high risk based on clinical and utilization data.  |
| had_major_procedure | Flag (0/1) showing whether the person has had at least one major medical procedure or surgery.  |
    ''')

    st.subheader("Preview of the data")
    st.write("First few rows of the cleaned dataset. Use the button to display all rows.")

    st.dataframe(df.head())

    if st.button("Show all data"):
        st.dataframe(df)

    st.markdown("---")

    st.subheader("Data understanding table")
    st.write("Summary of each column: data type, missing values, unique values, and an example entry.")



    summary_rows = []
    n_rows = len(df)

    for col in df.columns:
        col_data = df[col]
        missing = col_data.isna().sum()
        missing_pct = (missing / n_rows) * 100 if n_rows > 0 else 0
        nunique = col_data.nunique(dropna=True)
        example = col_data.dropna().iloc[0] if col_data.dropna().shape[0] > 0 else None

        summary_rows.append({
            "column": col,
            "dtype": str(col_data.dtype),
            "missing_count": int(missing),
            "missing_pct": round(missing_pct, 2),
            "n_unique": int(nunique),
            "example_value": example
        })

    summary_df = pd.DataFrame(summary_rows)
    st.dataframe(summary_df, use_container_width=True)



elif page == "Demographics & Risk":
    st.title("Demographics & Risk")

    question = st.sidebar.radio("Demographics questions",["Average cost by age group","Average cost by age group and sex","Income vs annual cost by region"])

    if question == "Average cost by age group":
        age_cost = (
            df.groupby("age_group", as_index=False)["annual_medical_cost"].mean().sort_values("annual_medical_cost"))

        figure1 = px.bar(age_cost, x="age_group", y="annual_medical_cost", title="Average annual medical cost by age group",labels={"age_group": "Age group","annual_medical_cost": "Average annual cost"})
        st.plotly_chart(figure1, use_container_width=True)

    elif question == "Average cost by age group and sex":
        age_sex_cost = (df.groupby(["age_group", "sex"], as_index=False)["annual_medical_cost"].mean())
        figure2 = px.bar(age_sex_cost, x="age_group", y="annual_medical_cost", color="sex",barmode="group",title="Average annual medical cost by age group and sex", labels={"age_group": "Age group","annual_medical_cost": "Average annual cost","sex": "Sex"})
        st.plotly_chart(figure2, use_container_width=True)

    elif question == "Income vs annual cost by region":
        figure_3 = px.scatter(df,x="income",y="annual_medical_cost", color="region",title="Income vs annual medical cost by region",labels={"income": "Income","annual_medical_cost": "Annual medical cost","region": "Region"})
        st.plotly_chart(figure_3, use_container_width=True)



elif page == "Chronic Conditions & Diabetes":
    st.title("Chronic Conditions & Diabetes")

    question = st.sidebar.radio("Chronic questions",["Average cost by diabetes status","Average cost by chronic count group","Average cost by specific chronic condition"])


    if "diabetes_label" not in df.columns:
        df["diabetes_label"] = df["diabetes"].map({0: "No diabetes", 1: "Diabetes"})

    if question == "Average cost by diabetes status":
        diab_cost = (df.groupby("diabetes_label", as_index=False)["annual_medical_cost"].mean())

        figure4 = px.bar(diab_cost,x="diabetes_label",y="annual_medical_cost",title="Average annual medical cost by diabetes status",labels={"diabetes_label": "Diabetes status","annual_medical_cost": "Average annual cost"})
        st.plotly_chart(figure4, use_container_width=True)

    elif question == "Average cost by chronic count group":
        def chronic_group(c):
            if c == 0:
                return "0 conditions"
            elif c == 1:
                return "1 condition"
            else:
                return "2+ conditions"

        df["chronic_group"] = df["chronic_count"].apply(chronic_group)

        chronic_cost = (
            df.groupby("chronic_group", as_index=False)["annual_medical_cost"].mean().sort_values("annual_medical_cost"))

        figure5 = px.bar(chronic_cost,x="chronic_group",y="annual_medical_cost",title="Average annual medical cost by number of chronic conditions",labels={"chronic_group": "Chronic condition group","annual_medical_cost": "Average annual cost"})
        st.plotly_chart(figure5, use_container_width=True)

    elif question == "Average cost by specific chronic condition":
        condition_cols = ["hypertension", "diabetes", "asthma", "copd","cardiovascular_disease", "cancer_history","kidney_disease", "liver_disease", "arthritis", "mental_health"]

        rows = []
        for col in condition_cols:
            tmp = df.groupby(col)["annual_medical_cost"].mean()
            if 1 in tmp.index:
                rows.append({"condition": col,"avg_cost_if_present": tmp.loc[1]})

        if rows:
            cond_df = pd.DataFrame(rows).sort_values("avg_cost_if_present", ascending=False)

            figure6 = px.bar(cond_df, x="condition",y="avg_cost_if_present",title="Average annual cost when each condition is present",labels={"condition": "Condition","avg_cost_if_present": "Average annual cost (condition = 1)"})
            st.plotly_chart(figure6, use_container_width=True)



elif page == "Utilization":
    st.title("Utilization")

    question = st.sidebar.radio("Utilization questions",["Distribution of annual medical costs","Average cost by number of hospitalizations","Total counts of procedures"])

    if question == "Distribution of annual medical costs":
        figure6 = px.histogram(df,x="annual_medical_cost",nbins=50,title="Distribution of annual medical costs",labels={"annual_medical_cost": "Annual medical cost"})
        st.plotly_chart(figure6, use_container_width=True)


    elif question == "Average cost by number of hospitalizations": 
        hosp_cost = (df.groupby("hospitalizations_last_3yrs", as_index=False)["annual_medical_cost"].mean())

        figure7 = px.bar(hosp_cost,x="hospitalizations_last_3yrs",y="annual_medical_cost",title="Average annual medical cost by hospitalizations (last 3 years)",labels={"hospitalizations_last_3yrs": "Hospitalizations (last 3 years)","annual_medical_cost": "Average annual cost"})
        st.plotly_chart(figure7, use_container_width=True)

    elif question == "Total counts of procedures":
        proc_cols = ["proc_imaging_count","proc_surgery_count","proc_physio_count","proc_consult_count","proc_lab_count"]
        proc_totals = df[proc_cols].sum().reset_index()
        proc_totals.columns = ["procedure_type", "total_count"]

        figure8 = px.bar(proc_totals, x="procedure_type",y="total_count", title="Total count of procedures across all patients",labels={"procedure_type": "Procedure type","total_count": "Total count"})
        st.plotly_chart(figure8, use_container_width=True)


elif page == "Plans & Costs":
    st.title("Plans & Costs")

    question = st.sidebar.radio( "Plan questions",["Average cost by plan type and network tier"])

    if question == "Average cost by plan type and network tier":
        plan_cost = (df.groupby(["plan_type", "network_tier"], as_index=False)["annual_medical_cost"].mean())
        
        figure_9 = px.bar(plan_cost, x="plan_type", y="annual_medical_cost", color="network_tier", barmode="group",title="Average annual medical cost by plan type and network tier",labels={"plan_type": "Plan type","network_tier": "Network tier","annual_medical_cost": "Average annual cost"})
        st.plotly_chart(figure_9, use_container_width=True)




