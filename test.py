import pandas
df= pandas.read_csv("Noun.csv", header=None)
words = {}
for row in df.iterrows():
    row = row[1].tolist()
    if str(row[0])[0] in words:
        words[str(row[0])[0]].append(row)
    else:
        words[str(row[0])[0]] = [row]
