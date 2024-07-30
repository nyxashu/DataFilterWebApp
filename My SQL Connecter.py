import mysql.connector
import pandas as pd

# Read the CSV file into a DataFrame with specified encoding
df = pd.read_csv('C:/Users/Administrator/Downloads/csv3.csv', encoding='latin1', low_memory=False)

# Rename columns to match SQL schema
df.rename(columns={
    'First name': 'FirstName',
    'Last Name': 'LastName',
    'Company Name': 'CompanyName',
    'Emp Link': 'EmpLink',
    'Street address': 'StreetAddress',
    'Zip Code': 'ZipCode',
    'Contact Number': 'ContactNumber',
    'Emp Size': 'EmpSize',
    'Company Link': 'CompanyLink'
}, inplace=True)

# Print column names to verify renaming
print("Renamed column names:", df.columns)

# Replace NaN values with None
df = df.where(pd.notnull(df), None)

# Print first few rows to verify data
print(df.head())

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mwg_server"
)
cursor = db.cursor()

# Create table schema with increased column sizes
create_table_query = """
CREATE TABLE IF NOT EXISTS your_table_name (
    FirstName VARCHAR(500),
    LastName VARCHAR(500),
    Email VARCHAR(500),
    CompanyName VARCHAR(500),
    EmpLink VARCHAR(1000),  -- Increased length
    JT VARCHAR(500),
    StreetAddress VARCHAR(1000),
    City VARCHAR(500),
    State VARCHAR(500),
    ZipCode VARCHAR(20),  -- Increased length
    Country VARCHAR(500),
    ContactNumber VARCHAR(50),  -- Increased length
    Industry VARCHAR(500),
    EmpSize VARCHAR(100),
    CompanyLink VARCHAR(1000)  -- Increased length
)
"""

cursor.execute(create_table_query)

# Define the insert query with placeholders
insert_query = """
INSERT INTO your_table_name (
    FirstName, LastName, Email, CompanyName, EmpLink, JT, 
    StreetAddress, City, State, ZipCode, Country, ContactNumber, 
    Industry, EmpSize, CompanyLink
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Insert data row by row with error handling
for row in df.itertuples(index=False):
    try:
        cursor.execute(insert_query, row)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print(f"Row data: {row}")

# Commit the changes
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
