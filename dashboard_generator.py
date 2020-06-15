# dashboard_generator.py
# I built this as if it were up-to-date on date on data although I have only imported
# data for the end of 2017 and beginning of 2018

import operator
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

# Module - all answers must be in USD format with $ and .00
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#Prompt User to enter Month and Year of Report they are seeking, and then establish file path to connect to that specific CSV 
raw_year = input("Enter Year (YYYY): ")
int_year = int(raw_year)
current_year = datetime.today().year # For real world application with up-to-date CSV files
while int_year < 2017 or int_year > 2019: # If in real world, would change 2019 to current_year variable defined above
    print("-----------------------")
    print("Thanks for using the Monthly Sales Dashboard!")
    print("It looks like you tried generating a Dashboard for a YEAR that we do not have data for.")
    print("At this time we only have access to data from October 2017 through April 2019.")
    print("Please input a different YEAR to try again.")
    print("-----------------------")
    raw_year = input("Enter Year (YYYY format): ")
    int_year = int(raw_year)
else:
    pass
    
raw_month = input("Enter Month (MM format): ")
int_month = int(raw_month)
current_month = datetime.today().month # For real world application with up-to-date CSV files (see line 37 for appropriate while loop)
#while int_month > 12 or int_year == 2017 and int_month < 10 or int_year == current_year and int_month >= current_month:
while int_month > 12 or int_year == 2017 and int_month < 10 or int_year == 2019 and int_month > 4:
    print("-----------------------")
    print("Thanks for using the Monthly Sales Dashboard!")
    print("It looks like you tried generating a Dashboard for a MONTH that we do not have data for.")
    print("At this time we only have access to data from October 2017 through April 2019.")
    print("Please input a different MONTH to try again.")
    print("-----------------------")
    raw_month = input("Enter Month (MM): ")
    int_month = int(raw_month)
else:
    pass

csv_filepath = os.path.join(os.path.dirname(__file__), "data", "monthly-sales", raw_year + raw_month + ".csv")
data = pd.read_csv(csv_filepath)

#TODO: Fill in the month based on the file selection, not hardcoded
month_name = datetime(2020, int_month, 1).strftime('%B')
print("-----------------------")
print("SALES REPORT FOR " + month_name.upper() + " " + raw_year)
print("-----------------------")
print("CRUNCHING THE DATA...")

# Print out the total sales by converting csv data into a dict and building a for loop that sums all sales
total_monthly_sales = data["sales price"].sum()
usd_monthly_sales = to_usd(total_monthly_sales)

print("-----------------------")
print("TOTAL MONTHLY SALES: " + str(usd_monthly_sales))

# Identify and print the top selling products
# Step 1: Pull out the unique products
product_names = data["product"]
unique_product_names = product_names.unique()
unique_product_names = unique_product_names.tolist()

# Step 2: Create a new list of dictionaries that is just each unique product and their total monthly sales
top_sellers = []
for product_name in unique_product_names:
    matching_rows = data[data["product"] == product_name]
    product_monthly_sales = matching_rows["sales price"].sum()
    top_sellers.append({"name": product_name, "monthly_sales": product_monthly_sales})

#Step 3: Sort the values so they are in the right order with highest monthly sales at the top of the list
top_sellers = sorted(top_sellers, key=operator.itemgetter("monthly_sales"), reverse=True)

print("-----------------------")
print("TOP SELLING PRODUCTS:")

#Step 4: Add the rank number to each product and print in USD format
rank = 1
for p in top_sellers:
    print("  " + str(rank) + ") " +
          p["name"] + ": " + to_usd(p["monthly_sales"]))
    rank = rank + 1

#Viz Time!
print("-----------------------")
print("VISUALIZING THE DATA...")

plotted_products = []
plotted_sales = []
for p in top_sellers:
    plotted_products.append(p["name"])
    plotted_sales.append(p["monthly_sales"])

dashboard_title = ("Top Selling Products: " + month_name + " " + raw_year)

#TODO: Change to USD, add numbers to bars
fig = plt.figure(constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig)

# Horizontal Bar Chart
ax1 = fig.add_subplot(spec[0,0])
ax1.barh(plotted_products, plotted_sales, color='seagreen', align='center')
# Y Axis
ax1.set_ylabel('Products')
ax1.set_yticklabels(plotted_products)
ax1.invert_yaxis()
# X Axis
formatter = ticker.FormatStrFormatter('$%1.0f')
ax1.xaxis.set_major_formatter(formatter)
ax1.set_xlabel('Sales (USD)')
ax1.set_xlim(right=10000)
# Values on Bars
for i, v in enumerate(plotted_sales):
    ax1.text(v, i, str(to_usd(v)), color='black', va='center', fontsize=8)

#ax1.text(plotted_products, plotted_sales, ha='center', va='center',
#        color='white')

# Pie Chart
ax2 = fig.add_subplot(spec[1,0])
ax2.pie(plotted_sales, autopct='%1.2f%%', textprops={'size': 'smaller', 'color': 'white'})
ax2.legend(plotted_products,
        title="Products",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1))

plt.suptitle(dashboard_title)
plt.show()