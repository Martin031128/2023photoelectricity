import csv

with open('test1.csv', newline='',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    #next(reader)  # 跳过第一行
    rows = []
    for row in reader:
        rows.append(tuple(map(int, row)))

def coordinate_call():
    return rows

def mixed_rows(rows):
    for i in range(len(rows)):
        rows[i] = (rows[i][1], rows[i][0])
    return rows


if __name__ == "__main__":
    print(rows)
    print(mixed_rows(rows))
