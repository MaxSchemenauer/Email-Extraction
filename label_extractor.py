import pandas as pd
import csv

"""xls = pd.ExcelFile("Conference_Email_labels.xlsx")
df = pd.DataFrame(columns=["ID", "Event Name", "Event location", "Date (Month Day, Year \"January 17, 2021\")", "Submission deadline", "Notification deadline"])
for sheet in xls.sheet_names:
    if sheet != "Sheet1":
        current = pd.read_excel(xls, sheet_name=sheet)
        current = current.drop(columns=current.columns[0])
        df = pd.concat([df, current], ignore_index=True)

df.to_csv(f"labels.csv", index=False)"""

"""with open("labels.csv", "r") as infile, open("cleaned_labels.csv", "w", newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # Remove trailing empty entries
        cleaned_row = [item for item in row if item]
        writer.writerow(cleaned_row)"""

with open("cleaned_labels.csv", "r") as infile, open("complete_labels.csv", "w", newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    count = 0
    count_total = 0
    for row in reader:
        # Remove trailing empty entries
        count_total += 1
        if len(row) >= 6:
            #count += 1
            cleaned_row = [item for item in row if len(item.split(',')) < 6]
            writer.writerow(cleaned_row)
    print(count_total)
