import streamlit as st
import pandas as pd
from datetime import datetime

# Define functions for navigation and saving responses
def next_page(skip_to=None):
    if skip_to:
        st.session_state.page = skip_to
    else:
        st.session_state.page += 1

def prev_page():
    if st.session_state.page > 1:
        st.session_state.page -= 1

def save_response(question, response):
    st.session_state.responses[question] = response

# Initialize session state variables for navigation and responses
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'response_id' not in st.session_state:
    st.session_state.response_id = 0  # Initialize response ID
if 'responses' not in st.session_state:
    st.session_state.responses = {}  # Dictionary to store responses

# Main App
def main():
    st.title("Voice of the Customer Survey")
  
    # Screener Question (with Termination Logic)
    if st.session_state.page == 1:
        m1_options = {"Yes": 1, "No": 2}
        with st.form(key='form_m1'):
            M1 = st.radio("m1: Do you want to participate in the survey?", list(m1_options.keys()))
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Next"):
                    save_response("M1", m1_options[M1])
                    if M1 == "No":
                        next_page(skip_to=998)  # Skip to termination page
                    else:
                        next_page()
            with col2:
                if st.form_submit_button("Back"):
                    prev_page()

    # Q1 - 5-Point Scale for Overall Satisfaction
    elif st.session_state.page == 2:
        q1_options = {"(1) Very Dissatisfied": 1, "(2) Dissatisfied": 2, "(3) Neutral": 3, "(4) Satisfied": 4, "(5) Very Satisfied": 5}
        with st.form(key='form_x1'):
            Q1 = st.radio("x1: Overall satisfaction with the product/service:", list(q1_options.keys()))
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Next"): 
                    save_response("Q1", q1_options[Q1])
                    next_page()
            with col2:
                if st.form_submit_button("Back"):
                    prev_page()

    # Q2 - Likelihood of Continuing with the Brand
    elif st.session_state.page == 3:
        q2_options = {"(1) Definitely would NOT continue": 1, "(2) Probably would NOT continue": 2, "(3) Not sure": 3, "(4) Probably would continue": 4, "(5) Definitely would continue": 5}
        with st.form(key='form_x2'):
            Q2 = st.radio("x2: How likely are you willing to continue using our brand?", list(q2_options.keys()))
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Next"):
                    save_response("Q2", q2_options[Q2])
                    next_page()
            with col2:
                if st.form_submit_button("Back"):
                    prev_page()

        # Q3 - Reasons for Q2 Response
    elif st.session_state.page == 4:
        Q2_code = st.session_state.responses.get("Q2", None)
        with st.form(key='form_x3'):
            if Q2_code in [4, 5]:
                q3_options = {"High speed of service": 5,
                          "Always answer call quickly": 6,
                          "Solve issues quickly": 7,
                          "Others (please specify)": 8}
            elif Q2_code in [1, 2]:
                q3_options = {"Long waiting time to reach the agent": 1,
                          "Agent did not solve my problem from the first time": 2,
                          "Long time to solve my problem": 3,
                          "Call agent has lack of knowledge about the services": 4,
                          "Others (please specify)": 8}
            else:
                q3_options = {"Others (please specify)": 8}
                
            Q3 = st.multiselect("x3. Why do you say so? Multiple answers", list(q3_options.keys()))
            q3_other = ""
            if "Others (please specify)" in Q3:
                q3_other = st.text_area("Please specify others...")

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Next"):
                    # Prepare a list of selected codes
                    selected_codes = [q3_options[option] for option in Q3]
                
                    # Include 'Other' text if filled
                    if q3_other:
                        selected_codes.append(f"Other: {q3_other}")
                
                    # Save response for Q3
                    save_response("Q3", selected_codes)
                    next_page()  # Move to the next page
                
            with col2:
                if st.form_submit_button("Back"):
                    prev_page()


    # Q4 - Likelihood to Recommend with a 5-point scale
    elif st.session_state.page == 5:
        q4_options = {"(1) Definitely would NOT recommend":1, "(2) Probably would NOT recommend":2, "(3) Might or might NOT recommend":3, "(4) Probably would recommend":4, "(5) Definitely would recommend":5}
        with st.form(key='form_Q4'):
            Q4 = st.radio("x4: How likely are you to recommend our brand to your colleagues or friends?", list(q4_options.keys()))
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Next"):
                    save_response("Q4", q4_options[Q4])
                    next_page()
            with col2:
                if st.form_submit_button("Back"):
                    prev_page()

    # Q5
    elif st.session_state.page == 6:
        q5_options = {"Yes":1, "No":2}
        with st.form(key='form_Q5'):
            Q5 = st.radio("x5: Did the agent solve the problem from the first time without follow ups?", list(q5_options.keys()))
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Next"):
                    save_response("Q5", q5_options[Q5])
                    next_page()
            with col2:
                if st.form_submit_button("Back"):
                    prev_page()

    # Q6
    elif st.session_state.page == 7:
        q6_options = {"Yes":1, "No":2}
        with st.form(key='form_Q6'):
            Q6 = st.radio("x6: Can we recontact you regarding your feedback to help you more?", list(q6_options.keys()))
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Next"):
                    save_response("Q6", q6_options[Q6])
                    next_page()
            with col2:
                if st.form_submit_button("Back"):
                    prev_page()

    # Q7
    elif st.session_state.page == 8:
        with st.form(key='form_Q7'):
            Q7 = st.text_area("x7. If you have any additional comments, please write them here. OPEN ENDED, OPTIONAL")
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Submit"):
                    save_response("Q7", Q7)
                    st.session_state.page = 999  # Move to Thank You Page
            with col2:
                if st.form_submit_button("Back"):
                    prev_page()

    # Termination Thank You Page (For Non-participation or Early Exit)
    elif st.session_state.page == 998:
        st.write("Thank you for your time! Unfortunately, you do not qualify for this survey.")
        
        # Prepare responses to save terminated cases
        responses = {"ID": st.session_state.response_id + 1,  # Add unique ID, increment for each response
                     "Date and Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  # Add date and time
        
        # Add other responses
        responses.update(st.session_state.responses)

        # Save terminated cases responses to CSV
        file_name = "voc_responses.csv"
        df = pd.DataFrame([responses])
        # Check if file exists to determine if headers should be written
        df.to_csv(file_name, mode="a", header=not pd.io.common.file_exists(file_name), index=False)
        
        # Increment response ID for next submission
        st.session_state.response_id += 1
        
        # Download button for saved CSV
        with open(file_name, "rb") as file:
            st.download_button("Download Responses as CSV", file, "voc_responses.csv")

    # Thank You Page (After Completing Survey)
    elif st.session_state.page == 999:
        st.write("Thank you for completing the survey!")
        
        # Prepare responses to save completed survey
        responses = {"ID": st.session_state.response_id + 1,  # Add unique ID, increment for each response
                     "Date and Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  # Add date and time
        
        # Add other responses
        responses.update(st.session_state.responses)

        # Save responses to CSV
        file_name = "voc_responses.csv"
        df = pd.DataFrame([responses])
        # Check if file exists to determine if headers should be written
        df.to_csv(file_name, mode="a", header=not pd.io.common.file_exists(file_name), index=False)
        
        # Increment response ID for next submission
        st.session_state.response_id += 1
        
        # Download button for saved CSV
        with open(file_name, "rb") as file:
            st.download_button("Download Responses as CSV", file, "voc_responses.csv")

# Run the main application function
if __name__ == "__main__":
    main()
