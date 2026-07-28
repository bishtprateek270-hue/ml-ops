import pandas as pd
import random
from faker import Faker

# Initialize Faker with Indian locale (matching the project's names)
fake = Faker('en_IN')

# Define list to store rows
data = []
num_records = 500

for _ in range(num_records):
    name = fake.first_name()
    
    # Introduce some missing values (NaN) in Age to simulate data quality issues
    if random.random() < 0.15:  # 15% probability of being missing
        age = None
    else:
        age = float(random.randint(18, 65))
        
    salary = random.randint(20000, 150000)
    
    # Purchased flag depends slightly on Salary/Age to make it realistic
    if salary > 80000 or (age and age > 45):
        purchased = "Yes" if random.random() < 0.8 else "No"
    else:
        purchased = "Yes" if random.random() < 0.3 else "No"
        
    data.append({
        "Name": name,
        "Age": age,
        "Salary": salary,
        "Purchased": purchased
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to data/raw_fake.csv
output_path = "data/raw_fake.csv"
df.to_csv(output_path, index=False)

print(f"Generated {num_records} sample records using Faker.")
print(f"Saved to: {output_path}")
print("\nFirst 10 rows:")
print(df.head(10))
