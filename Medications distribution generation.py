import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)

# Egyptian Governorates
governorates = [
    'Cairo', 'Giza', 'Alexandria', 'Dakahlia', 'Red Sea', 'Beheira',
    'Fayoum', 'Gharbiya', 'Ismailia', 'Menofia', 'Minya', 'Qaliubiya',
    'New Valley', 'Suez', 'Aswan', 'Assiut', 'Beni Suef', 'Port Said',
    'Damietta', 'Sharkia', 'South Sinai', 'Kafr El Sheikh', 'Matrouh',
    'Luxor', 'Qena', 'North Sinai', 'Sohag'
]

# Population data (approximate, in millions)
population_data = {
    'Cairo': 10.0, 'Giza': 9.2, 'Alexandria': 5.3, 'Dakahlia': 6.7,
    'Red Sea': 0.4, 'Beheira': 6.2, 'Fayoum': 3.7, 'Gharbiya': 5.1,
    'Ismailia': 1.3, 'Menofia': 4.3, 'Minya': 5.9, 'Qaliubiya': 5.6,
    'New Valley': 0.2, 'Suez': 0.7, 'Aswan': 1.5, 'Assiut': 4.4,
    'Beni Suef': 3.2, 'Port Said': 0.7, 'Damietta': 1.5, 'Sharkia': 7.2,
    'South Sinai': 0.1, 'Kafr El Sheikh': 3.4, 'Matrouh': 0.4,
    'Luxor': 1.3, 'Qena': 3.2, 'North Sinai': 0.4, 'Sohag': 5.0
}

# Medication categories
medication_categories = [
    'Antibiotics', 'Analgesics', 'Cardiovascular', 'Diabetes',
    'Respiratory', 'Gastrointestinal', 'Vitamins', 'Antihistamines',
    'Dermatological', 'Neurological'
]

# Common medications
medications = {
    'Antibiotics': ['Amoxicillin', 'Azithromycin', 'Ciprofloxacin', 'Cephalexin'],
    'Analgesics': ['Paracetamol', 'Ibuprofen', 'Diclofenac', 'Aspirin'],
    'Cardiovascular': ['Atenolol', 'Amlodipine', 'Enalapril', 'Losartan'],
    'Diabetes': ['Metformin', 'Glibenclamide', 'Insulin', 'Sitagliptin'],
    'Respiratory': ['Salbutamol', 'Montelukast', 'Budesonide', 'Prednisolone'],
    'Gastrointestinal': ['Omeprazole', 'Ranitidine', 'Metoclopramide', 'Loperamide'],
    'Vitamins': ['Vitamin D', 'Vitamin B12', 'Folic Acid', 'Multivitamin'],
    'Antihistamines': ['Cetirizine', 'Loratadine', 'Diphenhydramine', 'Fexofenadine'],
    'Dermatological': ['Hydrocortisone', 'Clotrimazole', 'Benzoyl Peroxide', 'Tretinoin'],
    'Neurological': ['Carbamazepine', 'Gabapentin', 'Fluoxetine', 'Sertraline']
}

# Generate dataset
records = []
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)
num_records = 50000

for _ in range(num_records):
    governorate = random.choice(governorates)
    population = population_data[governorate]

    # Create regional bias (urban areas get more, Upper Egypt gets less)
    if governorate in ['Cairo', 'Giza', 'Alexandria']:
        distribution_multiplier = np.random.uniform(1.5, 2.5)
    elif governorate in ['Aswan', 'Qena', 'Sohag', 'Luxor', 'Assiut']:
        distribution_multiplier = np.random.uniform(0.5, 0.9)
    else:
        distribution_multiplier = np.random.uniform(0.9, 1.5)

    category = random.choice(medication_categories)
    medication = random.choice(medications[category])

    # Generate quantity based on population and multiplier
    base_quantity = population * np.random.uniform(100, 500)
    quantity = int(base_quantity * distribution_multiplier)

    # Random date
    random_days = random.randint(0, (end_date - start_date).days)
    distribution_date = start_date + timedelta(days=random_days)

    # Seasonal patterns (respiratory medications increase in winter)
    month = distribution_date.month
    if category == 'Respiratory' and month in [11, 12, 1, 2]:
        quantity = int(quantity * 1.4)

    # Cost per unit (in EGP)
    cost_per_unit = np.random.uniform(5, 200)
    total_cost = quantity * cost_per_unit

    # Facility type
    facility_type = random.choice([
        'Public Hospital', 'Health Center', 'Rural Clinic',
        'Teaching Hospital', 'Specialized Center'
    ])

    # Distribution status
    status = random.choices(
        ['Delivered', 'Delayed', 'Partial'],
        weights=[0.75, 0.15, 0.10]
    )[0]

    records.append({
        'distribution_id': f'DIST-{_:06d}',
        'date': distribution_date.strftime('%Y-%m-%d'),
        'year': distribution_date.year,
        'month': distribution_date.month,
        'quarter': (distribution_date.month - 1) // 3 + 1,
        'governorate': governorate,
        'population_millions': population,
        'region': 'Upper Egypt' if governorate in ['Aswan', 'Qena', 'Sohag', 'Luxor', 'Assiut', 'Minya', 'Beni Suef']
        else 'Lower Egypt' if governorate in ['Cairo', 'Giza', 'Alexandria', 'Dakahlia', 'Beheira']
        else 'Other',
        'medication_category': category,
        'medication_name': medication,
        'quantity_units': quantity,
        'cost_per_unit_egp': round(cost_per_unit, 2),
        'total_cost_egp': round(total_cost, 2),
        'facility_type': facility_type,
        'distribution_status': status,
        'priority_level': random.choice(['High', 'Medium', 'Low']),
        'supplier': random.choice(['Supplier_A', 'Supplier_B', 'Supplier_C', 'Supplier_D'])
    })

# Create DataFrame
df = pd.DataFrame(records)

# Add calculated fields
df['per_capita_units'] = df['quantity_units'] / (df['population_millions'] * 1_000_000)
df['delivery_delay_days'] = df['distribution_status'].map({
    'Delivered': 0,
    'Delayed': np.random.randint(5, 30),
    'Partial': np.random.randint(1, 15)
})

# Sort by date
df = df.sort_values('date').reset_index(drop=True)

# Save to CSV
df.to_csv('egyptian_medication_distribution.csv', index=False)

print(f"Dataset created with {len(df)} records")
print(f"\nDataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nDataset summary:")
print(df.describe())
print(f"\nColumn types:")
print(df.dtypes)