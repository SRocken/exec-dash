# Executive Sales Dashboard
The Executive Sales Dashboard provides insight into our Etsy store's performance for the purposes of our monthly board meetings with our investors and advisors to discuss the company's strategic direction, set priorities, and allocate resources. The dashboard provides a monthly summary report of business insights, including the aggregation of total sales and the identification of top-selling products, as well as a historical view of sales since the start of their investment.

The dashboard uses data pulled from the online platform we use to sell our products. The data is downloaded as CSV and represents all individual sales orders for that month, including date of sale, product name, price, units sold, and total sales price.

Because the report compilation process had been somewhat stressful and vulnerable to manual error, this python script was designed to automate the process. Now the only manual step is uploading the monthly CSV file into the data repository.

# Setup
In order to successfully use this dashboard, you will need to install the following modules into your python environment, as well as connect to all the CSV files included in the repository:

pip install pandas
pip install matplotlib

# Implementation and Use
Monthly Sales Dashboard Generator:
If you are looking to view sales data for each month, please use the dashboard_generator.py application. This application will prompt you to enter the Year (YYYY) and Month (MM) that you are looking to analyze, and will produce a textual summary of the data, as well as a bar chart and pie chart to show it in a visual format.

Multiple Month Dashboard Generator:
If you are looking to see the total sales each month since we launched the eCommerce platform, use the multi_month.py application. Simply running the application will produce a line plot of all since since the first month we have complete data.