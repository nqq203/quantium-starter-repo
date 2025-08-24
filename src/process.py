import pandas as pd
import glob
import os

# Đường dẫn tới thư mục data
data_path = os.path.join("data", "daily_sales_data_*.csv")

# Lấy danh sách file csv
files = glob.glob(data_path)

dfs = []
for file in files:
    df = pd.read_csv(file)

    # Chỉ giữ lại product = pink morsel (không phân biệt hoa thường)
    df = df[df["product"].str.lower() == "pink morsel"]

    # Chuyển price từ "$3.00" -> 3.00
    df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

    # Tính sales = price * quantity
    df["Sales"] = df["price"] * df["quantity"]

    # Chỉ giữ lại cột cần thiết
    df = df[["Sales", "date", "region"]]

    # Đổi tên cột để đúng yêu cầu
    df = df.rename(columns={"date": "Date", "region": "Region"})

    dfs.append(df)

# Gộp tất cả
final_df = pd.concat(dfs, ignore_index=True)

# Xuất ra file CSV
final_df.to_csv("output.csv", index=False)

print("✅ Done! File output.csv đã được tạo.")
