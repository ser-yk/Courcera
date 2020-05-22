import  stepik_csv, collections

with open(r"C:\Users\Уберу потом\Downloads\Crimes.csv", 'r') as data:
    reader = stepik_csv.reader(data)
    cnt = {}
    for row in reader:
        if row[5] in cnt and '2015' in row[2]:
            cnt[row[5]] += 1
        elif row[5] not in cnt and '2015' in row[2]:
            cnt[row[5]] = 1
    # print(cnt)
    print(collections.Counter(cnt))


