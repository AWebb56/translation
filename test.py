import pandas

def csv_to_dict(csv_filename):
    dt = pandas.read_csv(csv_filename, header=None)
    data = {}
    for row in dt.iterrows():
        row = row[1].tolist()
        char = str(row[0])[0]
        if char in data:
            data[char].append(row)
        else:
            data[char] = [row]
    return data

def main():
    filenames = ["Noun.csv", "Verb.csv", "Adj.csv", "Adverb.csv", "Symbol.csv"]
    noun, verb, adj, adv, symbol = [csv_to_dict(filename) for filename in filenames]

if __name__ == "__main__":
    main()