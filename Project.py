# 24504922
# author- Fariya Zehrin
# This program analyzes Amazon products and sales data

def main(CSVfile, TXTfile, category):
    
# Read data from CSV file
    headers, data = read_csv(CSVfile)

# Filter data based on category
    filtered_data = filter_cat(data, category)
    
# Identifying product IDs with highest and lowest discounted prices
    high_id, low_id = extr_prices(filtered_data)
    
# Calculate statistical measures for filtered data
    mean, median, mad = statistics(filtered_data)
    
# Calculate standard deviations of discount percentages
    std_devs = std_dev_disc(data)
    
# Reading sales data from TXT file for correlation calculation
    sales_data = read_txt(TXTfile)
    
# Calculate correlation between sales of highest and lowest discounted products
    correlation = correlate_sales_data(sales_data, [high_id, low_id])
    
# Store product IDs with extreme discounts
    discount = [high_id, low_id]
    
# Return product IDs and calculated statistics
    return discount, [round(mean, 4), round(median, 4), round(mad, 4)], sorted(std_devs, reverse=True), round(correlation, 4)

# Reading the CSV file
def read_csv(CSVfile):
    with open(CSVfile, 'r') as f:
        headers = f.readline().strip().split(",")
        data = [line.strip().split(",") for line in f]
    return headers, data

# Filtering categories
def filter_cat(data, category):
    filtered = []
    
    for row in data:
        if row[2].strip().lower() == category.strip().lower():
# Ensuring case-insensitive match
            filtered.append(row)
    return filtered

#Task 1: Identify Extreme Discount Prices

# Identifying high and low prices for discounts
def extr_prices(filtered_data):
    high_price = -1
    low_price = float('inf')
    high_id = ""
    low_id = ""

    for row in filtered_data:
        discounted_price = float(row[4])
# Assuming discounted price is in column 4

        product_id = row[0]

        if discounted_price > high_price:
            high_price = float(discounted_price)
            high_id = product_id
            
        elif discounted_price == high_price:
# Tie-breaker by Product ID
            high_id = min(high_id, product_id)

        if discounted_price < low_price:
            low_price = discounted_price
            low_id = product_id
            
        elif discounted_price == low_price:
# Tie-breaker by Product ID
            low_id = min(low_id, product_id)

# Return product IDs in lowercase to handle case sensitivity
    return high_id.lower(), low_id.lower()

# Task 2: Summarize Price Distribution

def statistics(filtered_data):
# Assuming actual prices are in column 5, rating count in column 7
    prices = [float(row[4]) for row in filtered_data if int(row[7]) > 1000] 
            
    if not prices:
        return 0, 0, 0
    
# Calculating mean
    mean = sum(prices) / len(prices)
    
# Calculating median
    sort = sorted(prices)
    n = len(sort)
    
    if n % 2 == 0:
        median = (sort[n // 2 - 1] + sort[n // 2]) / 2
    else:
        median = sort[(n // 2)] 

# Calculating Mean absolute deviation
    mad = sum(abs(x - mean) for x in prices) / len(prices)
    
# Return rounded results
    return mean, median, mad

# Task 3: Calculate Standard Deviation of Discounted Percentages
def std_dev_disc(data):
    disc_perc = {}
    
    for row in data:
        category=row[2].strip().lower()
        rating = float(row[6])
        discounted_price = float(row[3])
        actual_price = float(row[4])
        
        if (3.3 <= rating <= 4.3):
            discount = (actual_price - discounted_price) / actual_price * 100
    
            if category not in disc_perc:
                disc_perc[category]=[]
                
        disc_perc[category].append(discount)
    std_dev_list=[]

#Calculate standard deviation for each category
    for category,discounts in disc_perc.items():
        
        if not discounts:
            continue
        
#calculating for each category    
        mean = sum(discounts) / len(discounts)
        sqr_diff = [(x - mean) ** 2 for x in discounts]
        
        variance = sum(sqr_diff) / (len(discounts) - 1)
        std_dev = variance ** 0.5
        std_dev_list.append(round(std_dev,4))
    
    return std_dev_list

# Read the sales data from TXT file
def read_txt(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    data = {}
    for line in lines:
        parts = line.split(',')
        year = parts[0].split(': ')[1]
        sales = {}
        for part in parts[1:]:
            product_id, units_sold = part.split(': ')
            sales[product_id.strip().lower()] = int(units_sold.strip())
            
# Ensure product_id is lowercase
        data[year] = sales
    
    return data

# Task 4: Correlate Sales Data
def correlate_sales_data(sales_data, extreme_discount_products):
    high_id, low_id = extreme_discount_products
    high_sales = []
    low_sales = []

    for year, sales in sales_data.items():
        high_sales.append(sales.get(high_id, 0))
        low_sales.append(sales.get(low_id, 0))

    if not high_sales or not low_sales:
        return 0
# Return if no data meets criteria

    mean_high = sum(high_sales) / len(high_sales)
    mean_low = sum(low_sales) / len(low_sales)

# Calculate covariance, standard deviations, and correlation

    covariance = sum((high_sales[i] - mean_high) * (low_sales[i] - mean_low) for i in range(len(high_sales)))
    std_dev_high = sum((sale - mean_high) ** 2 for sale in high_sales)
    std_dev_low = sum((sale - mean_low) ** 2 for sale in low_sales)

    if std_dev_high == 0 or std_dev_low == 0:
        return 0
# Return if division by zero

    correlation = covariance / ((std_dev_high**0.5) * (std_dev_low)**0.5)

    return correlation

