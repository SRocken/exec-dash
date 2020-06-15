import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import os
import glob

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

filepath = os.path.join(os.path.dirname(__file__), "data", "monthly-sales")
all_files = glob.glob(filepath + "/*.csv")

csv_list = []

for filename in all_files:
    monthly_sales = pd.read_csv(filename, index_col=None, header=0)
    csv_list.append(monthly_sales)

all_sales_data = pd.concat(csv_list, axis=0, ignore_index=True)

all_sales_data.date = pd.to_datetime(all_sales_data.date).dt.strftime('%m/%Y') #Convert MM/DD/YYYY to MM/YYYY

months = all_sales_data["date"]
unique_months = months.unique()
unique_months = unique_months.tolist()

monthly_sales = []
for product_month in unique_months:
    matching_months = all_sales_data[all_sales_data["date"] == product_month]
    product_monthly_sales = matching_months["sales price"].sum()
    monthly_sales.append({"date": product_month, "monthly_sales": product_monthly_sales})

print("VISUALIZING AVAILABLE MONTHLY SALES DATA...")

plotted_sales = []
plotted_months = []
for p in monthly_sales:
    plotted_sales.append(p["monthly_sales"])
    plotted_months.append(p["date"])


fig = plt.figure(constrained_layout=True)
ax = fig.add_subplot()

plt.style.use('fivethirtyeight')

x_values = plotted_months
y_values = plotted_sales

ax.plot(plotted_months, plotted_sales)
ax.set_xlabel('Months')
ax.set_xticklabels(plotted_months, rotation=90)
formatter = ticker.FormatStrFormatter('$%1.0f')
ax.yaxis.set_major_formatter(formatter)
ax.set_ylabel('Sales (USD)')
ax.set_title("Monthly Sales Per Product Over Time")
ax.set_ylim(bottom=0,top=max(plotted_sales)+2000)

def annot_max(plotted_months,plotted_sales, ax=None):
    ymax = max(plotted_sales)
    xpos = plotted_sales.index(ymax)
    xmax = plotted_months[xpos]
    text = 'Best month: ' + to_usd(ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60", color="black")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94,0.96), **kw)
def annot_min(plotted_months,plotted_sales, ax=None):
    ymin = min(plotted_sales)
    xpos = plotted_sales.index(ymin)
    xmin = plotted_months[xpos]
    text = 'Worst month: ' + to_usd(ymin)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=120", color="black")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="bottom")
    ax.annotate(text, xy=(xmin, ymin), xytext=(0.94,0.16), **kw)
annot_max(plotted_months, plotted_sales)
annot_min(plotted_months, plotted_sales)

plt.show()