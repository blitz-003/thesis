import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fetch the webpage
url = 'https://www.semrush.com/trending-websites/cn/all'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the table rows (<tr> tags)
rows = soup.find_all('tr')

# Extract data from each row and store it in a list of lists
data = []
for row in rows:
    # Extract text from each cell (<td> tag) within the row
    row_data = [cell.text.strip() for cell in row.find_all('td')]
    data.append(row_data)

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = 'output.xlsx'
df.to_excel(output_file, index=False, header=False)  # Set header=False to exclude column headers

print(f'Data saved to {output_file}')
