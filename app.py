import streamlit as st

# --------------------------------
# PAGE SETUP
# --------------------------------

st.set_page_config(
    page_title="Project Budget Tracker",
    page_icon="💰",
    layout="wide"
)

# --------------------------------
# STORE EXPENSES
# --------------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Default category budgets
if "category_budgets" not in st.session_state:
    st.session_state.category_budgets = {
        "Labor": 35000.0,
        "Materials": 45000.0,
        "Equipment": 15000.0,
        "Subcontractors": 15000.0,
        "Permits": 5000.0,
        "Other": 5000.0
    }

# --------------------------------
# APP TITLE
# --------------------------------

st.title("💰 Project Budget Tracker")
st.write(
    "Track your project budget, expenses, and financial performance."
)

st.divider()

# --------------------------------
# PROJECT INFORMATION
# --------------------------------

st.subheader("Project Information")

project_name = st.text_input(
    "Project Name",
    value="Office Renovation"
)

total_budget = st.number_input(
    "Total Project Budget ($)",
    min_value=0.0,
    value=120000.0,
    step=1000.0
)

# --------------------------------
# CALCULATIONS
# --------------------------------

total_spent = sum(
    expense["Amount"]
    for expense in st.session_state.expenses
)

remaining_budget = total_budget - total_spent

if total_budget > 0:
    percent_used = (total_spent / total_budget) * 100
else:
    percent_used = 0

# --------------------------------
# BUDGET DASHBOARD
# --------------------------------

st.divider()

st.subheader("Budget Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Budget",
        f"${total_budget:,.2f}"
    )

with col2:
    st.metric(
        "Total Spent",
        f"${total_spent:,.2f}"
    )

with col3:
    st.metric(
        "Remaining",
        f"${remaining_budget:,.2f}"
    )

with col4:
    st.metric(
        "Budget Used",
        f"{percent_used:.1f}%"
    )

# --------------------------------
# BUDGET STATUS
# --------------------------------

if total_spent > total_budget:
    st.error(
        f"🔴 Project is over budget by "
        f"${abs(remaining_budget):,.2f}"
    )

elif percent_used >= 90:
    st.warning(
        "🟠 Warning: More than 90% of the budget has been used."
    )

elif percent_used >= 75:
    st.warning(
        "🟡 Caution: More than 75% of the budget has been used."
    )

else:
    st.success("🟢 Project is currently within budget.")

# --------------------------------
# CATEGORY BUDGETS
# --------------------------------

st.divider()
st.subheader("Category Budgets")

st.write("Allocate the project budget across expense categories.")

for category in st.session_state.category_budgets:

    st.session_state.category_budgets[category] = st.number_input(
        f"{category} Budget ($)",
        min_value=0.0,
        value=st.session_state.category_budgets[category],
        step=500.0,
        key=f"budget_{category}"
    )

# Check category allocation
allocated_budget = sum(
    st.session_state.category_budgets.values()
)

difference = total_budget - allocated_budget

if difference == 0:
    st.success("✅ Category budgets match the total project budget.")

elif difference > 0:
    st.warning(
        f"${difference:,.2f} of the project budget has not been allocated."
    )

else:
    st.error(
        f"Category budgets exceed the project budget by "
        f"${abs(difference):,.2f}."
    )

# --------------------------------
# ADD EXPENSE
# --------------------------------

st.divider()

st.subheader("Add Expense")

category = st.selectbox(
    "Expense Category",
    [
        "Labor",
        "Materials",
        "Equipment",
        "Subcontractors",
        "Permits",
        "Other"
    ]
)

description = st.text_input(
    "Expense Description",
    placeholder="Example: Concrete delivery"
)

expense_amount = st.number_input(
    "Expense Amount ($)",
    min_value=0.0,
    value=0.0,
    step=1.0
)

expense_date = st.date_input(
    "Expense Date"
)

# --------------------------------
# ADD EXPENSE BUTTON
# --------------------------------

if st.button("Add Expense"):

    if expense_amount > 0:

        new_expense = {
            "Date": expense_date,
            "Category": category,
            "Description": description,
            "Amount": expense_amount
        }

        st.session_state.expenses.append(new_expense)

        st.rerun()

    else:

        st.warning(
            "Please enter an expense amount greater than $0."
        )

# --------------------------------
# EXPENSE HISTORY
# --------------------------------

st.divider()

# --------------------------------
# CORRECT / REVERSE EXPENSE
# --------------------------------

if len(st.session_state.expenses) > 0:

    if st.button("↩️ Delete Last Expense"):
        deleted_expense = st.session_state.expenses.pop()

        st.success(
            f"Deleted ${deleted_expense['Amount']:,.2f} "
            f"from {deleted_expense['Category']}."
        )

        st.rerun()
        
st.subheader("Expense History")

if len(st.session_state.expenses) > 0:

    st.dataframe(
        st.session_state.expenses,
        use_container_width=True
    )

else:

    st.info("No expenses have been recorded yet.")