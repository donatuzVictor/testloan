import streamlit as st
import pickle
import numpy as np

# Load the trained model
loaded_model = pickle.load(open('model.sav', 'rb'))

def loan_prediction(input_data):
    data_as_array = np.array(input_data).reshape(1, -1)
    prediction = loaded_model.predict(data_as_array)
    if prediction[0] == 0:
        return 'You are not eligible for the loan'
    else:
        return 'You are eligible for the loan'

def main():
    st.title('Bank Loan Prediction App')

    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gender", options=["Male", "Female"])
        married = st.selectbox("Married", options=["Yes", "No"])
        education = st.selectbox("Education", options=["Graduate", "Not Graduate"])
        self_employed = st.selectbox("Self Employed", options=["Yes", "No"])

    with col2:
        dependents = st.selectbox("Dependents", options=["0", "1", "2", "3+"])
        applicant_income = st.number_input("Applicant Income", min_value=0, value=0)
        coapplicant_income = st.number_input("Coapplicant Income", min_value=0.0, value=0.0)
        loan_amount = st.number_input("Loan Amount", min_value=0.0, value=0.0)

    with col3:
        loan_amount_term = st.number_input("Loan Amount Term (days)", min_value=0.0, value=360.0)
        credit_history = st.selectbox("Credit History", options=["1.0 (Good)", "0.0 (Bad)"])
        property_area = st.selectbox("Property Area", options=["Urban", "Rural"])

    if st.button('Bank Loan Application'):
        try:
            gender_val = 1 if gender == 'Male' else 0
            married_val = 1 if married == 'Yes' else 0
            education_val = 1 if education == 'Graduate' else 0
            self_employed_val = 1 if self_employed == 'Yes' else 0
            dependents_val = 3 if dependents == '3+' else int(dependents)
            credit_history_val = 1.0 if credit_history.startswith('1') else 0.0
            rural = 1 if property_area == 'Rural' else 0
            urban = 1 if property_area == 'Urban' else 0

            input_data = [
                gender_val, married_val, education_val, self_employed_val,
                dependents_val, applicant_income, coapplicant_income,
                loan_amount, loan_amount_term,
                credit_history_val, rural, urban
            ]
            result = loan_prediction(input_data)
            st.success(result)
        except ValueError:
            st.error('Please enter a valid field')
        except Exception as e:
            st.error(f'An unexpected error occurred: {e}')

if __name__ == '__main__':
    main()