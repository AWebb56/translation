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
    filenames = [
        "adj",
        "adnominal",
        "adverb",
        "auxil",
        "conjunction",
        "filler",
        "interjection",
        "noun.adjv",
        "noun.adverbal",
        "noun",
        "noun.demonst",
        "noun.nai",
        "noun.name",
        "noun.number",
        "noun.org",
        "noun.others" "noun.place",
        "noun.proper",
        "noun.verbal",
        "others",
        "postp-col",
        "postp",
        "prefix",
        "suffix",
        "symbol",
        "verb",
    ]
    words = {}
    for part_of_speech in filenames:
        words[part_of_speech] = csv_to_dict(f"{part_of_speech.capitalize()}.csv")


if __name__ == "__main__":
    main()
