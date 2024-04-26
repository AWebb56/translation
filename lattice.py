import pandas


# words[char] = [[word, leftId, rigthId, cost, part of speech, lemma] for words starting with char]
def read_csv_files():
    def read_csv(part_of_speech, words):
        csv_filename = f"{part_of_speech.capitalize()}.csv"
        dt = pandas.read_csv(csv_filename, header=None)
        for row in dt.iterrows():
            row = row[1].tolist()
            char = str(row[0])[0]

            lemma = row[10]
            row = row[:4]
            row.append(part_of_speech)
            row.append(lemma)
            if char in words:
                words[char].append(row)
            else:
                words[char] = [row]
        return words

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
        words = read_csv(part_of_speech, words)
    return words


# matrix[(leftId, rightId)] = connection cost
def read_matrix_file():
    matrix = {}
    with open("matrix.def") as f:
        numLeftIds, numRightIds = map(int, f.readline().split())
        for _ in range(numLeftIds * numRightIds):
            leftId, rightId, cost = map(int, f.readline().split())
            matrix[(leftId, rightId)] = cost
    return matrix


# lattice[i] = [(word, leftId, rightId, cost, part of speech, lemma) for words starting at position i
def generate_lattice(text, words):
    lattice = [[] for _ in range(len(text) + 1)]

    for i in range(len(text)):
        char = text[i]
        if char in words:
            for word_info in words[char]:
                if text[i:].find(word_info[0]) != 0:
                    continue
                word = word_info[0]
                leftId = word_info[1]
                rightId = word_info[2]
                cost = word_info[3]
                part_of_speech = word_info[4]
                lemma = word_info[5]
                if text[i : i + len(word)] == word:
                    lattice[i].append(
                        (
                            word,
                            i,
                            i + len(word),
                            cost,
                            part_of_speech,
                            lemma,
                            leftId,
                            rightId,
                        )
                    )
    return lattice


# best_path = parse of the best path for the given lattice
def best_path(lattice, matrix):
    # Initialize a table to store the best paths and their costs
    best_paths = [None] * len(lattice)
    best_costs = [float("inf")] * len(lattice)

    # Set the cost of the starting position to 0
    best_costs[0] = 0

    # Iterate through each position in the lattice
    for i in range(len(lattice)):
        # If there are no paths at this position, skip
        if not lattice[i]:
            continue

        # Iterate through each path at this position
        for path in lattice[i]:
            # Calculate the cost of the path from the previous position
            prev_cost = best_costs[path[1]]
            total_cost = prev_cost + path[3]
            if i != 0 and best_paths[i - 1] is not None:
                total_cost += matrix[(path[6], best_paths[i - 1][7])]

            # Update the best path and cost for the current position
            if total_cost < best_costs[path[2]]:
                best_paths[path[2]] = path
                best_costs[path[2]] = total_cost

    # Backtrack to find the best path
    best_path = []
    i = len(lattice) - 1
    while i > 0:
        best_path.append(best_paths[i])
        i = best_paths[i][1]

    # Reverse the best path to get the correct order
    best_path.reverse()

    return best_path


def read_sentences():
    filename = "sentences.txt"
    sentences = ["東京都に住む人々"]
    with open(filename, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            sentences.append(line.strip())
    return sentences


def main():
    words = read_csv_files()
    matrix = read_matrix_file()
    sentences = read_sentences()

    for i, text in enumerate(sentences):
        if i != 0:
            print()
        lattice = generate_lattice(text, words)
        parse = best_path(lattice, matrix)
        print(f"Text {i+1}: {text}\nParse:")
        for token in parse:
            print(token)


if __name__ == "__main__":
    main()
