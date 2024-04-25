import pandas


def read_csv_files():
    def read_csv(csv_filename):
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
        "noun.others",
        "noun.place",
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
        words[part_of_speech] = read_csv(f"{part_of_speech.capitalize()}.csv")
    return words


def read_matrix_file():
    matrix = {}
    with open("matrix.def") as f:
        numLeftIds, numRightIds = map(int, f.readline().split())
        for _ in range(numLeftIds * numRightIds):
            leftId, rightId, cost = map(int, f.readline().split())
            matrix[(leftId, rightId)] = cost
    return matrix


# TODO
def generate_lattice(text):
    pass


# TODO
def best_path(lattice):
    pass


def main():
    words = read_csv_files()
    matrix = read_matrix_file()

    texts = ["東京都に住む", "東京都に住む人", "東京都に住む人々"]
    for i, text in enumerate(texts):
        lattice = generate_lattice(text)
        output = best_path(lattice)
        print(f"text {i+1}: {text}\n\t{output}")


if __name__ == "__main__":
    main()
