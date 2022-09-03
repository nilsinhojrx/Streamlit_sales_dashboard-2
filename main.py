import streamlit as st
from data import loadData, barChart

st.set_page_config(page_title="Sales Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide",
)

@st.cache
def get_data():
    data = loadData("supermarkt_sales.xlsx")
    return data
DATA = get_data()

# ----- Side Bar -------
st.sidebar.header("Filter Options")
city = st.sidebar.multiselect(
    "Select the City:",
    options=DATA["City"].unique(),
    default=DATA["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=DATA["Customer_type"].unique(),
    default=DATA["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=DATA["Gender"].unique(),
    default=DATA["Gender"].unique()
)
month = st.sidebar.multiselect(
    "Select the Month:",
    options=DATA["Month"].unique(),
    default=DATA["Month"].unique()
)
# ----- Data filtering -----
data_selection = DATA.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender & Month == @month"
)
# ----- Show the dataframe on the screen ----
#st.dataframe(data_selection)

# ----- Main Page -------
st.title(":bar_chart: Sales Dashboard")
st.markdown("#####")

#Top KPI's
left_column, middle_column, right_column = st.columns(3)
left_column2, middle_column2, right_column2 = st.columns(3)

try:
    total_sales = int(data_selection["Total"].sum())
    average_rating = round(data_selection["Rating"].mean(), 1)
    average_sales_by_transaction = round(data_selection["Total"].mean(), 2)
    star_rating = ":star:" * int(round(average_rating, 0))
    amount_sales = data_selection["Total"].count()
    profit = round(data_selection["cogs"].sum(), 2)
    best_payment = data_selection.groupby(by=["Payment"]).count()[["Quantity"]].sort_values(by="Quantity", ascending=False).index[0]

    with left_column:
        st.subheader("Total Sales:")
        st.markdown(f"<h3>US $ {total_sales:,}</h3>", unsafe_allow_html=True)
    with middle_column:
        st.subheader("Average Rating:")
        st.subheader(f"{average_rating}{star_rating}")
    with right_column:
        st.subheader("Average Sales Per Transaction:")
        st.markdown(f"<h3>US $ {average_sales_by_transaction}</h3>", unsafe_allow_html=True)
    with left_column2:
        st.subheader("Amount Sales:")
        st.markdown(f"<h3>{amount_sales}</h3>", unsafe_allow_html=True)
    with middle_column2:
        st.subheader("Total Profit:")
        st.markdown(f"<h3>US $ {profit:,}</h3>", unsafe_allow_html=True)
    with right_column2:
         st.subheader("Best Payment Type:")
         st.markdown(f"<h3>{best_payment}</h3>",unsafe_allow_html=True)
except ValueError:
    with left_column:
        st.subheader("Total Sales:")
    with middle_column:
        st.subheader("Average Rating:")
    with right_column:
        st.subheader("Average Sales Per Transaction:")
    with left_column2:
        st.subheader("Amount Sales:")
    with middle_column2:
        st.subheader("Total Profit:")
    with right_column2:
         st.subheader("Best Payment Type: ")

st.markdown("---")

# Sales by Product Line [Bar Chart]
sales_by_product_line = (
    data_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = barChart(sales_by_product_line,
    x="Total",
    y="index",
    title="Sales by Product Line",
    orientation="h",
    color="#02FFEB"
)
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False)),
    xaxis_title = "Total (US $)",
    font=dict(
        size=14,
    )
)

# Sales by Hour [Bar Chart]
sales_by_hour = (
    data_selection.groupby(by=["Hour"]).sum()[["Total"]].sort_values(by="Total")
)
fig_hour_sales = barChart(
    sales_by_hour,
    x="index",
    y="Total",
    title="Sales by Hour",
    orientation="v",
    color="#FFFB0D",
)
fig_hour_sales.update_layout(
    xaxis = dict(tickmode="linear"),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid=False)),
    yaxis_title = "Total (US $)",
    font=dict(
        size=14,
    )
)

#-- Columns to display charts
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hour_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
