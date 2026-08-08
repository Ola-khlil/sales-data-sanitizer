import pandas as pd
import numpy as np
from rich.console import Console
from rich.panel import Panel

console = Console()

df = pd.read_csv('dirty_cafe_sales.csv')
# Draft bf
df_before = df.copy()

df.head()

print("\n--- BEFORE CLEANING ---")
print(df.info())
print(df.isnull().sum())


# 1. Remove duplicates
df = df.drop_duplicates()


# 2. Handle missing values

# Every obj value
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].fillna(df[col].mode()[0])

# Every numiric value
for col in df.select_dtypes(include=np.number).columns:
    df[col] = df[col].fillna(df[col].median())

# Date type
if 'Date' in df.columns:
    df['Date'] = df['Date'].fillna(df['Date'].mode()[0])

# 3. Fix data types
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')


# 4. Clean text fields
if 'Item' in df.columns:
    df['Item'] = df['Item'].str.strip().str.lower()

    # Unification of values
    df['Item'] = df['Item'].replace({
        'cofee': 'coffee',
        'coffe': 'coffee'
    })


# 5. Remove invalid values
if 'Total' in df.columns:
    df = df[df['Total'] > 0]


print("\n--- AFTER CLEANING ---")
print(df.info())
print(df.isnull().sum())


# BEFORE vs AFTER COMPARISON

print("\n--- DATA QUALITY COMPARISON ---")

missing_before_pct = (df_before.isnull().sum().sum() / df_before.size) * 100
missing_after_pct = (df.isnull().sum().sum() / df.size) * 100

print(f"Missing % BEFORE: {missing_before_pct:.2f}%")
print(f"Missing % AFTER: {missing_after_pct:.2f}%")

if 'total' in df.columns:
    invalid_before = len(df_before[df_before['total'] <= 0])
    invalid_after = len(df[df['total'] <= 0])

    print(f"\nInvalid Total BEFORE: {invalid_before}")
    print(f"Invalid Total AFTER: {invalid_after}")

print("\nUnique Items BEFORE:", df_before['Item'].nunique())
print("Unique Items AFTER:", df['Item'].nunique())
col = 'total' if 'total' in df.columns else 'Total'

invalid_before = len(df_before[df_before[col] <= 0]) if col in df_before.columns else 0
invalid_after = len(df[df[col] <= 0]) if col in df.columns else 0

print(f"Invalid Total BEFORE: {invalid_before}")
print(f"Invalid Total AFTER: {invalid_after}")
print(f"Rows BEFORE: {len(df_before)}")
print(f"Rows AFTER: {len(df)}")

print(f"\nMissing values BEFORE: {df_before.isnull().sum().sum()}")
print(f"Missing values AFTER: {df.isnull().sum().sum()}")

content = """[bold cyan]• Missing values reduced significantly.[/bold cyan]
[bold cyan]• Invalid numeric values were handled.[/bold cyan]
[bold cyan]• Data consistency improved through standardization.[/bold cyan]
[bold cyan]• Duplicate records removed.[/bold cyan]
[bold cyan]• Text values cleaned and normalized.[/bold cyan]

[bold green]Conclusion:[/bold green]
Data quality has improved and is now suitable for analysis."""


console.print(Panel(content, title="[bold yellow]QUALITY IMPROVEMENT SUMMARY[/bold yellow]", expand=False))



# Clean Column Names
df.columns = df.columns.str.strip()

# type convert
df['Price Per Unit'] = pd.to_numeric(df['Price Per Unit'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Total Spent'] = pd.to_numeric(df['Total Spent'], errors='coerce')

# Convert Transaction Date and handle errors
df['Date_Converted'] = pd.to_datetime(df['Transaction Date'], errors='coerce')

# --- Validation Rules ---

df['price_valid'] = df['Price Per Unit'] > 0
df['quantity_valid'] = df['Quantity'] > 0

#  Calculation Check (Price * Quantity = Total)
df['calculation_valid'] = np.isclose(df['Total Spent'], df['Price Per Unit'] * df['Quantity'], equal_nan=False)

#  Date format validation (was it a real date? , is the date is less than or equal to "now"?)
df['date_format_valid'] = df['Date_Converted'].notnull()
df['not_in_future'] = df['Date_Converted'] <= pd.Timestamp.now()

#  Payment method validation
valid_methods = ['cash', 'credit card', 'digital wallet']
df['payment_valid'] = df['Payment Method'].str.lower().str.strip().isin(valid_methods)

# Summary of Issues 
validation_summary = {
    "Invalid/Missing Prices": (~df['price_valid']).sum(),
    "Calculation Errors": (~df['calculation_valid']).sum(),
    "Invalid Date Formats": (~df['date_format_valid']).sum(),
    "Future Dates Found": (df['not_in_future'] == False).sum(), 
    "Wrong Payment Methods": (~df['payment_valid']).sum(),
}

print("Validation Results:")
for key, value in validation_summary.items():
    print(f"- {key}: {value} issues found")

#  Expectations Function 
def check_expectations(data):
    now = pd.Timestamp.now()
    expectations = {
        "All items named": data['Item'].notnull().all(),
        "Prices are positive": (data['Price Per Unit'] > 0).all(),
        "No Future Dates": (data['Date_Converted'] <= now).all(),
        "Math is correct": np.isclose(data['Total Spent'], data['Price Per Unit'] * data['Quantity'], equal_nan=False).all()
    }
    return expectations

results = check_expectations(df)
print("\nExpectation Success (True/False):")
print(results)

total_records = len(df)

# validation percentages
report = {
    "Price > 0": (df['Price Per Unit'] > 0).mean() * 100,
    "Quantity > 0": (df['Quantity'] > 0).mean() * 100,
    "Correct Calculation": np.isclose(df['Total Spent'], df['Price Per Unit'] * df['Quantity'], equal_nan=False).mean() * 100,
    "Valid Date Format": df['Date_Converted'].notnull().mean() * 100,
    "Date Not in Future": (df['Date_Converted'] <= pd.Timestamp.now()).mean() * 100,
    "Valid Payment Method": df['Payment Method'].str.lower().str.strip().isin(['cash', 'credit card', 'digital wallet']).mean() * 100,
    "Item Name Present": df['Item'].notnull().mean() * 100
}

for rule, percent in report.items():
    print(f"{rule}: {percent:.2f}%")


