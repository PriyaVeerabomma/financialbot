import streamlit as st
import pandas as pd
import requests
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import time
import re
import yfinance as yf


# Page configuration
st.set_page_config(
    page_title="FinanceBot 💰",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Setup ---
load_dotenv()

# GitHub models setup
token = os.environ.get("GITHUB_TOKEN")
if not token:
    st.error("GITHUB_TOKEN not found in environment variables!")
    st.stop()
    
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"


coingecko_api_url = os.environ.get("COINGECKO_API_URL")

if not token:
    st.error("GITHUB_TOKEN not found in environment variables!")
    st.stop()
    
if not coingecko_api_url:
    st.warning("COINGECKO_API_URL not found in environment variables, using default")
    coingecko_api_url = "https://api.coingecko.com/api/v3/simple/price"





# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI(
        base_url=endpoint,
        api_key=token,
    )

client = get_openai_client()

# Initialize session state
if "user_data" not in st.session_state:
    st.session_state.user_data = {"name": "", "email": "", "income": 0}
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount", "Date"])
if "convo_active" not in st.session_state:
    st.session_state.convo_active = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "message" not in st.session_state:
    st.session_state.message = ""
if "consent" not in st.session_state:
    st.session_state.consent = None
if "error_count" not in st.session_state:
    st.session_state.error_count = 0

# --- Helper function to use GitHub's model ---
def get_ai_response(prompt, system_instruction="You are a helpful financial assistant."):
    try:
        with st.status("Processing your request...", expanded=False) as status:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=300,
                model=model_name
            )
            status.update(label="Response ready!", state="complete", expanded=False)
            return response.choices[0].message.content
    except Exception as e:
        st.error(f"Sorry, I encountered an issue: {str(e)}")
        return "I apologize, but I'm having trouble processing your request right now. Could you try again or ask me something else?"




def is_valid_email(email):
    # Basic regex pattern for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_income(income):
    try:
        # Convert to float in case it's entered as a string
        income_value = float(income)
        return income_value > 0
    except (ValueError, TypeError):
        return False


# # Callback for when user submits their info

def submit_user_info():
    valid_email = is_valid_email(st.session_state.email_input) if st.session_state.email_input else False
    valid_income = is_valid_income(st.session_state.income_input) if st.session_state.income_input else False
    
    if st.session_state.name_input and valid_email and valid_income:
        st.session_state.user_data = {
            "name": st.session_state.name_input, 
            "email": st.session_state.email_input,
            "income": float(st.session_state.income_input)
        }
        st.session_state.convo_active = True
        st.rerun()
    else:
        if not st.session_state.name_input:
            st.error("Please enter your name.")
        elif not valid_email:
            st.error("Please enter a valid email address (e.g. name@example.com).")
        elif not valid_income:
            st.error("Please enter a valid positive number for income.")
            
            

# Callback for when user submits a message
def submit_message():
    if st.session_state.message:
        user_input = st.session_state.message
        st.session_state.message = ""  # Clear the input
        
        # Add message to chat history
        try:
            intent = classify_intent(user_input)
            st.session_state.current_message = user_input
            st.session_state.current_intent = intent
            st.session_state.error_count = 0  # Reset error count on successful processing
        except Exception as e:
            st.error("I'm having trouble understanding your request. Could you try rephrasing?")
            st.session_state.error_count += 1
            
            # If multiple errors in a row, provide more guidance
            if st.session_state.error_count >= 3:
                st.info("Try asking about budgeting, expenses, investments, or type 'help' for suggestions.")
                
        st.rerun()

# Set user consent
def set_consent(value):
    st.session_state.consent = value
    if value:
        st.success("Thank you for your consent! I'll send you occasional financial tips.")
    else:
        st.info("No problem! I won't send any marketing emails.")
    time.sleep(1.5)
    st.rerun()

# --- Intent Recognition ---
def classify_intent(query):
    prompt = f"""Classify this finance-related query into one of:
    - budget_setup: Setting or adjusting budgets.
    - add_expense: Logging expenses or tracking spending.
    - investment_tips: Advice on stocks, crypto, retirement or any investments.
    - view_report: Summary of expenses/budgets or financial reports.
    - help: User needs assistance or examples of what they can ask.
    - goodbye: Ending the chat or expressing thanks/farewell.
    - other: Queries not clearly matching the above categories.

    User query: {query}
    Intent:"""
    
    intent = get_ai_response(
        prompt, 
        "You are a finance intent classifier. Respond with only the intent label in lowercase, no explanation."
    ).strip().lower()
    
    return intent

# --- Handle Finance-Specific Logic ---
def handle_expenses():
    if st.session_state.expense_category and st.session_state.expense_amount > 0:
        # Get current date in string format
        current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
        
        new_expense = pd.DataFrame([[
            st.session_state.expense_category, 
            st.session_state.expense_amount,
            current_date
        ]], columns=["Category", "Amount", "Date"])
        
        st.session_state.expenses = pd.concat(
            [st.session_state.expenses, new_expense], 
            ignore_index=True
        )
        
        response = f"✅ Added ${st.session_state.expense_amount:.2f} to {st.session_state.expense_category}."
        st.session_state.chat_history.append((
            st.session_state.current_message, 
            response
        ))
        
        # Clear form
        st.session_state.expense_category = ""
        st.session_state.expense_amount = 0
        
        # Clear current message
        st.session_state.current_message = None
        st.session_state.current_intent = None

# --- Generate budget recommendation based on income ---
def generate_budget_recommendation(income):
    # 50/30/20 rule
    needs = income * 0.5
    wants = income * 0.3
    savings = income * 0.2
    
    return {
        "Needs": {
            "Housing": needs * 0.5,
            "Utilities": needs * 0.2,
            "Groceries": needs * 0.2,
            "Transportation": needs * 0.1
        },
        "Wants": {
            "Entertainment": wants * 0.4,
            "Dining Out": wants * 0.3,
            "Shopping": wants * 0.3
        },
        "Savings": {
            "Emergency Fund": savings * 0.5,
            "Retirement": savings * 0.3,
            "Other Goals": savings * 0.2
        }
    }

# --- Welcome & Onboarding Page ---
def onboarding_page():
    st.title("Welcome to FinanceBot! 💸")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### Your Personal Financial Assistant
        
        I'm here to help you take control of your finances! With FinanceBot, you can:
        
        -  **Create personalized budgets** based on your income
        
        -  **Track your expenses** across different categories  
        
        -  **Get investment advice** tailored to your situation
        
        -  **View financial reports** to understand your spending
        
        Let's start by setting up your profile so I can provide personalized recommendations.
        """)
    
    with col2:
        with st.form("user_info_form"):
            st.text_input("Your name:", key="name_input")
            st.text_input("Email address:", key="email_input")
            st.number_input("Monthly income ($):", min_value=0.0, key="income_input")
            st.form_submit_button("Start My Financial Journey", on_click=submit_user_info)

# --- Main Chat Interface ---
def chat_page():
    st.title(f"FinanceBot Chat 💬")
    
    # Sidebar with user info
    with st.sidebar:
        st.subheader("Your Profile")
        st.write(f"👤 Name: {st.session_state.user_data['name']}")
        st.write(f"📧 Email: {st.session_state.user_data['email']}")
        st.write(f"💵 Income: ${st.session_state.user_data['income']:.2f}/month")
        
        st.divider()
        
        # Marketing consent - conditional logic requirement
        if st.session_state.consent is None:
            st.subheader("Quick Question")
            st.write("Would you like to receive occasional financial tips via email?")
            col1, col2 = st.columns(2)
            with col1:
                st.button("Yes, please!", on_click=set_consent, args=(True,))
            with col2:
                st.button("No, thanks", on_click=set_consent, args=(False,))
        
        st.divider()
        
        # Help section
        with st.expander("💡 What can I ask?"):
            st.markdown("""
            Try asking me:
            - "Help me create a budget"
            - "I want to track an expense"
            - "What investment tips do you have?"
            - "Show me my spending report"
            - "How should I save for retirement?"
            """)
        
        if st.button("End Session"):
            st.session_state.convo_active = False
            st.rerun()
    
    # Main chat container
    chat_container = st.container()
    
    # Message input
    with st.container():
        st.text_input(
            "Type your financial question here:", 
            key="message", 
            on_change=submit_message,
            placeholder="e.g., Help me budget my money..."
        )
    
    # Display chat history
    with chat_container:
        if not st.session_state.chat_history:
            # Initial welcome message
            with st.chat_message("assistant"):
                st.write(f"👋 Hello {st.session_state.user_data['name']}! I'm your personal FinanceBot assistant.")
                st.write("How can I help with your finances today? You can ask about budgeting, expense tracking, investment tips, or viewing reports.")
        
        for user_msg, bot_msg in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(user_msg)
            with st.chat_message("assistant"):
                st.write(bot_msg)
    
    # Handle current message if exists
    if hasattr(st.session_state, 'current_message') and st.session_state.current_message:
        with chat_container:
            with st.chat_message("user"):
                st.write(st.session_state.current_message)
            
            with st.chat_message("assistant"):
                intent = st.session_state.current_intent
                
                # Budget Setup Intent
                if "budget" in intent:
                    name = st.session_state.user_data["name"]
                    income = st.session_state.user_data["income"]
                    
                    budget_rec = generate_budget_recommendation(income)
                    
                    st.write(f"I've created a personalized monthly budget for you, {name}!")
                    st.write("Based on the 50/30/20 rule (50% needs, 30% wants, 20% savings), here's my recommendation:")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("Needs (50%)")
                        for category, amount in budget_rec["Needs"].items():
                            st.write(f"• {category}: ${amount:.2f}")
                    
                    with col2:
                        st.subheader("Wants (30%)")
                        for category, amount in budget_rec["Wants"].items():
                            st.write(f"• {category}: ${amount:.2f}")
                    
                    with col3:
                        st.subheader("Savings (20%)")
                        for category, amount in budget_rec["Savings"].items():
                            st.write(f"• {category}: ${amount:.2f}")
                    
                    response = f"I've created a personalized budget for you based on your monthly income of ${income:.2f}. It follows the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings. Would you like me to adjust any category?"
                    
                    st.session_state.chat_history.append((
                        st.session_state.current_message, 
                        response
                    ))
                
                # Expense Tracking Intent
                elif "expense" in intent:
                    st.subheader("Add an Expense")
                    with st.form(key="expense_form"):
                        st.selectbox(
                            "Category:", 
                            ["Housing", "Utilities", "Groceries", "Transportation", 
                             "Entertainment", "Dining Out", "Shopping", "Other"],
                            key="expense_category"
                        )
                        st.number_input("Amount ($):", min_value=0.0, key="expense_amount")
                        st.form_submit_button("Add Expense", on_click=handle_expenses)
                    
                    st.write(f"Please fill out the form above to track your expense, {st.session_state.user_data['name']}.")
                    
                    if len(st.session_state.expenses) > 0:
                        st.write(f"You've tracked {len(st.session_state.expenses)} expenses so far.")
                    
                    if "current_message" not in st.session_state or not st.session_state.current_intent:
                        st.session_state.chat_history.append((
                            st.session_state.current_message, 
                            "Please add your expense using the form above."
                        ))
                
                # Investment Tips Intent
                # elif "investment" in intent:
                #     try:
                #         api_url = "htt"
                #         btc_price = requests.get(api_url).json()["bitcoin"]["ethereum"]["usd"]
                #         st.metric("Bitcoin Price", f"${btc_price}")
                #         # st.metric("Ethereum Price", f"${eth_price}")

                #     except:
                #         st.warning("Could not fetch current Bitcoin price.")
                    
                #     name = st.session_state.user_data["name"]
                #     income = st.session_state.user_data["income"]


                # Investment Tips Intent
                # Investment Tips Intent
                    elif "investment" in intent:
                        try:
                            # Use environment variable instead of hardcoded URL
                            coingecko_api_url = os.environ.get("COINGECKO_API_URL", "https://api.coingecko.com/api/v3/simple/price")
                            api_params = "?ids=bitcoin&vs_currencies=usd"
                            
                            response = requests.get(f"{coingecko_api_url}{api_params}")
                            btc_price = response.json()["bitcoin"]["usd"]  # Correct access path
                            st.metric("Bitcoin Price", f"${btc_price}")
                            
                        except Exception as e:
                            st.warning(f"Could not fetch current Bitcoin price: {str(e)}")
                        
                        name = st.session_state.user_data["name"]
                        income = st.session_state.user_data["income"]
                    
                    # Calculate recommended investment amount
                    monthly_investment = income * 0.15
                    
                    st.write(f"Based on your income of ${income:.2f}/month, I recommend investing about ${monthly_investment:.2f}/month.")
                    
                    investment_tips = get_ai_response(
                        f"Give {name} 3 specific investment tips based on a monthly income of ${income}, with a personal touch. Format as bullet points. Include one tip about long-term retirement planning.",
                        "You are a certified financial advisor specializing in beginner investments. Be specific and personalized."
                    )
                    st.write(investment_tips)
                    
                    st.session_state.chat_history.append((
                        st.session_state.current_message, 
                        f"Based on your income of ${income:.2f}/month, I recommend investing about ${monthly_investment:.2f}/month.\n\n{investment_tips}"
                    ))
                
                # View Report Intent
                elif "report" in intent or "view" in intent:
                    if not st.session_state.expenses.empty:
                        st.subheader("Your Expense Report")
                        
                        # Summary metrics
                        total_spent = st.session_state.expenses["Amount"].sum()
                        income = st.session_state.user_data["income"]
                        savings = income - total_spent if income > total_spent else 0
                        savings_percentage = (savings / income * 100) if income > 0 else 0
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Monthly Income", f"${income:.2f}")
                        col2.metric("Total Expenses", f"${total_spent:.2f}")
                        col3.metric("Savings", f"${savings:.2f} ({savings_percentage:.1f}%)")
                        
                        # Chart
                        st.subheader("Spending by Category")
                        expense_by_category = st.session_state.expenses.groupby("Category").sum().reset_index()
                        st.bar_chart(expense_by_category, x="Category", y="Amount")
                        
                        # Data table
                        st.subheader("Expense Details")
                        st.dataframe(st.session_state.expenses)
                        
                        response = f"Here's your financial report, {st.session_state.user_data['name']}. You've spent ${total_spent:.2f} of your ${income:.2f} monthly income, saving ${savings:.2f} ({savings_percentage:.1f}% of income). Would you like any specific analysis of your spending habits?"
                    else:
                        response = f"You don't have any expenses logged yet, {st.session_state.user_data['name']}. Try adding some expenses first by saying 'I want to add an expense'!"
                        st.info(response)
                    
                    st.session_state.chat_history.append((
                        st.session_state.current_message, 
                        response
                    ))
                
                # Help Intent
                elif "help" in intent:
                    st.subheader("How I Can Help You")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("""
                        ### Budget & Planning
                        - "Create a budget for me"
                        - "How should I allocate my income?"
                        - "Help me plan for a big purchase"
                        
                        ### Expense Tracking
                        - "I want to log an expense"
                        - "Record my spending on groceries"
                        - "Track my recent purchase"
                        """)
                    
                    with col2:
                        st.markdown("""
                        ### Investments
                        - "What should I invest in?"
                        - "Give me retirement advice"
                        - "How much should I be saving?"
                        
                        ### Reports & Analysis
                        - "Show me my spending report"
                        - "How am I doing financially?"
                        - "Where am I spending too much?"
                        """)
                    
                    response = f"I'm here to help with your finances, {st.session_state.user_data['name']}! You can ask me about budgeting, expense tracking, investments, or financial reports. Check out the examples above for inspiration. What would you like help with today?"
                    
                    st.session_state.chat_history.append((
                        st.session_state.current_message, 
                        response
                    ))
                
                # End Conversation
                elif "goodbye" in intent or "bye" in intent:
                    message = f"Thank you for using FinanceBot, {st.session_state.user_data['name']}! I've sent a summary to {st.session_state.user_data['email']}. Feel free to come back anytime for more financial guidance. Have a wonderful day! 😊"
                    st.write(message)
                    
                    st.session_state.chat_history.append((
                        st.session_state.current_message, 
                        message
                    ))
                    
                    st.session_state.convo_active = False
                    
                    if st.button("Start New Session"):
                        # Reset specific parts but keep user data
                        st.session_state.chat_history = []
                        st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount", "Date"])
                        st.session_state.convo_active = True
                        st.rerun()
                
                # Fallback for other queries
                else:
                    # Try to provide a relevant financial response
                    response = get_ai_response(
                        f"The user {st.session_state.user_data['name']} with income ${st.session_state.user_data['income']} asked: {st.session_state.current_message}. " +
                        "Provide a helpful financial response. If the query isn't related to personal finance, politely redirect them to financial topics you can help with.",
                        "You are a knowledgeable finance assistant. Keep answers brief, focused on personal finance topics, and personalized to the user."
                    )
                    st.write(response)
                    
                    # If response seems like a fallback, add suggestions
                    if "I'm not sure" in response or "I can't" in response or "outside" in response:
                        st.write("Here are some topics I can help with:")
                        st.markdown("• Budgeting & saving money\n• Tracking expenses\n• Investment advice\n• Financial reports")
                    
                    st.session_state.chat_history.append((
                        st.session_state.current_message, 
                        response
                    ))
                
                # Clear current message
                st.session_state.current_message = None
                st.session_state.current_intent = None

# --- End Session Page ---
def end_session_page():
    st.title("Session Ended")
    st.write(f"Thank you for using FinanceBot, {st.session_state.user_data['name']}!")
    
    # Show expense summary if available
    if not st.session_state.expenses.empty:
        st.subheader("Your Financial Summary")
        
        total_spent = st.session_state.expenses["Amount"].sum()
        income = st.session_state.user_data["income"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Income", f"${income:.2f}")
            st.metric("Total Expenses", f"${total_spent:.2f}")
            st.metric("Balance", f"${income - total_spent:.2f}")
        
        with col2:
            expense_by_category = st.session_state.expenses.groupby("Category").sum()
            st.bar_chart(expense_by_category)
    
    st.markdown("""
    ### Financial Tips to Remember
    
    - Track all expenses, even small ones - they add up!
    - Follow the 50/30/20 budget rule when possible
    - Build an emergency fund of 3-6 months of expenses
    - Start investing early, even with small amounts
    """)
    
    if st.button("Start New Session", key="new_session"):
        # Reset session state
        st.session_state.chat_history = []
        st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount", "Date"])
        st.session_state.convo_active = True
        st.rerun()
    
    if st.button("Reset Completely", key="reset"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- Main app ---
def main():
    if not st.session_state.user_data["name"]:
        onboarding_page()
    elif st.session_state.convo_active:
        chat_page()
    else:
        end_session_page()

if __name__ == "__main__":
    main()




