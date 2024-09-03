import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from functools import reduce

# Define prior probabilities
prior_burnout_strong = 0.3
prior_burnout_weak = 0.7

# Function to map responses to likelihood scores
def map_response_to_likelihood(response, burnout_type):
    likelihoods = {
        "strong": {
            "Never": 0.1, "Rarely": 0.2, "Sometimes": 0.4, "Often": 0.7, "Always": 0.9,
            "Not at all": 0.1, "Slightly": 0.3, "Moderately": 0.5, "Very": 0.7, "Extremely": 0.9,
            "Poor": 0.8, "Fair": 0.6, "Good": 0.4, "Very Good": 0.2, "Excellent": 0.1,
            "Yes": 0.9, "No": 0.1, "Positive": 0.1, "Neutral": 0.5, "Negative": 0.8
        },
        "weak": {
            "Never": 0.7, "Rarely": 0.6, "Sometimes": 0.4, "Often": 0.2, "Always": 0.1,
            "Not at all": 0.8, "Slightly": 0.6, "Moderately": 0.4, "Very": 0.3, "Extremely": 0.1,
            "Poor": 0.2, "Fair": 0.4, "Good": 0.6, "Very Good": 0.8, "Excellent": 0.9,
            "Yes": 0.1, "No": 0.9, "Positive": 0.9, "Neutral": 0.5, "Negative": 0.2
        }
    }
    return likelihoods.get(burnout_type, {}).get(response, 0.5)

# Function to calculate combined likelihood
def calculate_likelihood(responses, burnout_type):
    try:
        likelihood = reduce(lambda x, y: x * y, [map_response_to_likelihood(resp, burnout_type) for resp in responses])
        return likelihood
    except Exception as e:
        st.error(f"An error occurred in calculating likelihood: {e}")
        return 1  # Default value to prevent crashing

# Function to apply Bayes' Theorem
def apply_bayes(likelihood_strong, likelihood_weak):
    try:
        posterior_strong = (likelihood_strong * prior_burnout_strong) / (
                (likelihood_strong * prior_burnout_strong) + (likelihood_weak * prior_burnout_weak)
        )
        posterior_weak = 1 - posterior_strong
        return posterior_strong, posterior_weak
    except ZeroDivisionError:
        st.error("Division by zero occurred while calculating probabilities.")
        return 0.5, 0.5  # Neutral probabilities to handle the error gracefully

# Function to display results and recommendations
def display_results(posterior_strong, posterior_weak):
    st.subheader("Assessment Results")
    if posterior_strong > 0.5:
        st.warning(f"Probability of strong burnout: {posterior_strong:.2f}. It is recommended to seek professional help.")
    else:
        st.info(f"Probability of weak burnout: {posterior_weak:.2f}. Consider taking a break, improving your diet, and getting more sleep.")

# Function to plot burnout probabilities with customized colors
def plot_probabilities(strong, weak):
    # Define color palette based on the probabilities
    if strong > 0.5:
        colors = ["#FF6F61", "#FFD700"]  # Smooth Red for Strong, Smooth Yellow for Weak
    elif weak > 0.5:
        colors = ["#FFD700", "#98FB98"]  # Smooth Yellow for Weak, Smooth Green for Minimal
    else:
        colors = ["#98FB98", "#FFD700"]  # Smooth Green for Minimal, Smooth Yellow for Weak

    labels = ['Strong Burnout', 'Weak Burnout']
    probabilities = [strong, weak]

    plt.figure(figsize=(8, 5))
    sns.barplot(x=labels, y=probabilities, palette=colors)
    plt.ylim(0, 1)
    plt.ylabel('Probability')
    plt.title('Burnout Probability Assessment')
    st.pyplot(plt)

# Streamlit interface for collecting user input
def main():
    st.title("Burnout Assessment")
    st.markdown(
        """
        <style>
        .main {
            padding: 2rem;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        .stSelectbox select, .stSlider div {
            font-size: 18px;
        }
        .stMarkdown {
            font-size: 18px;
        }
        .footer {
            font-size: 12px;
            text-align: right;
            padding: 10px;
            color: #555;
            position: fixed;
            right: 0;
            bottom: 0;
            background-color: #f1f1f1;
            width: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("##### Discover if You’re on the Path to Burnout")

    # Collecting user responses with initial neutral or default values
    responses = [
        st.selectbox("How often do you feel physically and emotionally drained?", 
                     ["Select an option", "Never", "Rarely", "Sometimes", "Often", "Always"], index=0),
        st.slider("Rate your energy levels during and after work on a scale of 1-10", 1, 10, value=None),
        st.selectbox("How would you rate your sleep quality?", 
                     ["Select an option", "Poor", "Fair", "Good", "Very Good", "Excellent"], index=0),
        st.slider("On a scale of 1-10, how stressed do you feel at work?", 1, 10, value=None),
        st.selectbox("How interested are you in your daily tasks?", 
                     ["Select an option", "Not at all", "Slightly", "Moderately", "Very", "Extremely"], index=0),
        st.selectbox("How would you describe your attitude towards colleagues or clients?", 
                     ["Select an option", "Positive", "Neutral", "Negative"], index=0),
        st.selectbox("Do you feel your work lacks meaning?", 
                     ["Select an option", "Yes", "No", "Sometimes"], index=0),
        st.slider("Rate your confidence in performing your job effectively on a scale of 1-10", 1, 10, value=None),
        st.selectbox("How satisfied are you with your accomplishments at work?", 
                     ["Select an option", "Not at all", "Slightly", "Moderately", "Very", "Extremely"], index=0),
        st.selectbox("Have you noticed a decline in your productivity or efficiency?", 
                     ["Select an option", "Yes", "No"], index=0),
        st.selectbox("Do you experience physical symptoms like headaches or muscle tension frequently?", 
                     ["Select an option", "Never", "Rarely", "Sometimes", "Often", "Always"], index=0),
        st.selectbox("Do you often feel anxious or depressed?", 
                     ["Select an option", "Never", "Rarely", "Sometimes", "Often", "Always"], index=0),
        st.selectbox("How often do you take sick days or time off due to feeling overwhelmed?", 
                     ["Select an option", "Never", "Rarely", "Sometimes", "Often", "Always"], index=0),
        st.selectbox("Do you find yourself avoiding social interactions with colleagues or friends?", 
                     ["Select an option", "Never", "Rarely", "Sometimes", "Often", "Always"], index=0),
        st.selectbox("Have you started using unhealthy coping strategies (e.g., overeating, alcohol)?", 
                     ["Select an option", "Never", "Rarely", "Sometimes", "Often", "Always"], index=0),
        st.selectbox("Are you working excessive hours?", 
                     ["Select an option", "Yes", "No"], index=0),
        st.selectbox("Are your job expectations clear?", 
                     ["Select an option", "Yes", "No", "Sometimes"], index=0),
        st.selectbox("Do you have support from colleagues or supervisors?", 
                     ["Select an option", "Yes", "No", "Sometimes"], index=0),
        st.slider("Rate your work-life balance on a scale of 1-10", 1, 10, value=None),
        st.selectbox("Can you relax and recover outside of work hours?", 
                     ["Select an option", "Never", "Rarely", "Sometimes", "Often", "Always"], index=0),
    ]

    # Check if all responses have been provided
    if all([resp != "Select an option" and resp is not None for resp in responses]):
        # Calculate likelihoods
        likelihood_strong = calculate_likelihood(responses, "strong")
        likelihood_weak = calculate_likelihood(responses, "weak")
        
        # Apply Bayes' Theorem
        posterior_strong, posterior_weak = apply_bayes(likelihood_strong, likelihood_weak)
        
        # Display results and recommendations
        display_results(posterior_strong, posterior_weak)
        
        # Plot the probabilities
        plot_probabilities(posterior_strong, posterior_weak)
    else:
        st.info("Please complete all questions to see the burnout assessment results.")

    # Add Refresh button to reload the page
    if st.button("Refresh"):
        st.experimental_rerun()
   
    st.markdown(
    """
    <style>
    .footer {
        font-size: 12px;
        text-align: right;
        padding: 10px;
        color: #555;
        position: fixed;
        right: 0;
        bottom: 0;
        background-color: #f1f1f1;
        width: auto;
    }
    </style>
    <div class="footer">
        Developed by Jayron Soares
    </div>
    """,
    unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
