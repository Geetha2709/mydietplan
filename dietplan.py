
import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Configure Gemini API
genai.configure(api_key=os.getenv("AIzaSyBwEhdfJX7IgSJQadMW_J12b58K2NDHqtA"))
model = genai.GenerativeModel('gemini-2.0-flash')

# App title and description
st.title("🍽️ Personalized Meal Plan Generator")
st.write("Get a customized weekly meal plan based on your dietary preferences and health goals!")

# User input section
with st.sidebar:
    st.header("Your Preferences")
    dietary_pref = st.multiselect(
        "Dietary Preferences",
        ["Vegan", "Vegetarian", "Keto", "Paleo", "Gluten-free", "Dairy-free", "Low-carb", "Mediterranean"]
    )
    
    health_goal = st.selectbox(
        "Primary Health Goal",
        ["Weight loss", "Muscle gain", "Maintenance", "Improved energy", "Athletic performance"]
    )
    
    allergies = st.text_input("Allergies or restrictions (comma separated)")
    cuisine_pref = st.multiselect(
        "Preferred Cuisines",
        ["Italian", "Mexican", "Asian", "Indian", "Mediterranean", "American", "Other"]
    )
    
    cooking_time = st.select_slider(
        "Daily cooking time availability",
        options=["<30 min", "30-60 min", "1-2 hours", "2+ hours"]
    )
    
    budget = st.select_slider(
        "Weekly grocery budget",
        options=["Budget", "Moderate", "Generous"]
    )

# Generate meal plan button
if st.button("Generate My Meal Plan"):
    with st.spinner("Creating your personalized meal plan..."):
        # Create prompt for Gemini
        prompt = f"""
        Create a detailed weekly meal plan for someone with the following preferences:
        - Dietary preferences: {', '.join(dietary_pref) if dietary_pref else 'None'}
        - Health goal: {health_goal}
        - Allergies/restrictions: {allergies if allergies else 'None'}
        - Preferred cuisines: {', '.join(cuisine_pref) if cuisine_pref else 'Any'}
        - Daily cooking time: {cooking_time}
        - Budget: {budget}
        
        Include:
        1. 7 days of meals (breakfast, lunch, dinner, and 2 snacks)
        2. Detailed recipes for each meal
        3. Nutritional information (calories, protein, carbs, fat)
        4. A comprehensive shopping list organized by category
        5. Tips for meal prep and storage
        
        Format the output clearly with headings for each section.
        """
        
        # Get response from Gemini
        response = model.generate_content(prompt)
        
        # Display meal plan
        st.subheader("Your Personalized Meal Plan")
        st.write(response.text)
        
        # Option to download
        st.download_button(
            label="Download Meal Plan",
            data=response.text,
            file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Progress tracking section
st.header("📈 Progress Tracking")
if "weight_data" not in st.session_state:
    st.session_state.weight_data = pd.DataFrame(columns=["Date", "Weight"])

col1, col2 = st.columns(2)
with col1:
    new_date = st.date_input("Date")
with col2:
    new_weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, step=0.1)

if st.button("Add Weight Entry"):
    new_entry = pd.DataFrame([[new_date, new_weight]], columns=["Date", "Weight"])
    st.session_state.weight_data = pd.concat([st.session_state.weight_data, new_entry]).sort_values("Date")
    st.success("Weight added!")

if not st.session_state.weight_data.empty:
    # Weight progress chart
    fig, ax = plt.subplots()
    ax.plot(st.session_state.weight_data["Date"], st.session_state.weight_data["Weight"], marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")
    ax.set_title("Weight Progress")
    st.pyplot(fig)
    
    # Macronutrient pie chart (example)
    if st.checkbox("Show Sample Macronutrient Distribution"):
        labels = 'Protein', 'Carbs', 'Fat'
        sizes = [30, 40, 30]  # Example values
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)
else:
    st.info("Add weight entries to track your progress")

# Additional features expander
with st.expander("Additional Features"):
    st.write("""
    **Future Enhancements:**
    - Recipe image generation
    - Meal plan customization after generation
    - Integration with grocery delivery services
    - Exercise recommendations
    - Water intake tracking
    - Community recipe sharing
    - Seasonal ingredient suggestions
    """)
