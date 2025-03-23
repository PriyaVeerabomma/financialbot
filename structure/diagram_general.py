from diagrams import Cluster, Diagram
from diagrams.programming.language import Python
from diagrams.onprem.client import Users
from diagrams.custom import Custom
from diagrams.generic.compute import Rack

with Diagram("FinanceBot Full Architecture (GPT-4o Enhanced)", show=False, direction="TB"):
    user = Users("User")

    with Cluster("Frontend Layer"):
        ui = Python("Streamlit UI")
        with Cluster("UI Components"):
            onboarding = Python("Onboarding")
            chat = Python("Chat Interface")
            expenses = Python("Expense Form")
            reports = Python("Reports View")

    with Cluster("Intent Classifier\n(uses GPT-4o)"):
        classifier = Python("Intent Classifier")
        budget_intent = Python("budget_setup")
        expense_intent = Python("add_expense")
        investment_intent = Python("investment_tips")
        report_intent = Python("view_report")
        help_intent = Python("help")
        goodbye_intent = Python("goodbye")
        other_intent = Python("other")

    with Cluster("Processing Layer"):
        budget_engine = Python("Budget Engine")
        expense_tracker = Python("Expense Tracker")
        report_generator = Python("Report Generator")

    with Cluster("External Services"):
        gpt_api = Custom("GPT-4o API", "./chatgpt.png")
        coingecko_api = Custom("CoinGecko API", "./coingeck.png")

    with Cluster("Data Layer"):
        session_state = Rack("Session State\n(Streamlit)")

    # User interface flow
    user >> ui
    ui >> onboarding
    ui >> chat >> classifier
    ui >> expenses
    ui >> reports

    # Intent classification paths
    classifier >> gpt_api
    classifier >> budget_intent
    classifier >> expense_intent
    classifier >> investment_intent
    classifier >> report_intent
    classifier >> help_intent
    classifier >> goodbye_intent
    classifier >> other_intent

    # Processing paths
    budget_intent >> budget_engine >> session_state
    expense_intent >> expense_tracker >> session_state
    report_intent >> report_generator << session_state

    # Additional GPT-4o logic
    expense_intent >> gpt_api  # Natural language expense input
    help_intent >> gpt_api
    goodbye_intent >> gpt_api
    other_intent >> gpt_api
    investment_intent >> gpt_api >> coingecko_api








