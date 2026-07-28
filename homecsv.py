from faker import Faker
import pandas as pd
import random

fake = Faker()

data = []

# Number of records
num_records = 1000

for _ in range(num_records):
    lot_area = random.randint(2000, 20000)          # sq ft
    overall_qual = random.randint(1, 10)            # Quality rating
    overall_cond = random.randint(1, 10)            # Condition rating
    year_built = random.randint(1950, 2024)
    gr_liv_area = random.randint(500, 5000)         # Living area in sq ft
    garage_cars = random.randint(0, 4)

    # Generate SalePrice with some dependency on features
    sale_price = (
        30000
        + lot_area * 3
        + gr_liv_area * 120
        + overall_qual * 25000
        + garage_cars * 12000
        + (year_built - 1950) * 800
        - overall_cond * 500
        + random.randint(-15000, 15000)  # noise
    )

    sale_price = max(50000, int(sale_price))

    data.append({
        "LotArea": lot_area,
        "OverallQual": overall_qual,
        "OverallCond": overall_cond,
        "YearBuilt": year_built,
        "GrLivArea": gr_liv_area,
        "GarageCars": garage_cars,
        "SalePrice": sale_price
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("house_prices_fake.csv", index=False)

print(df.head())
print("\nCSV file 'house_prices_fake.csv' created successfully.")
