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


# Node class to construct lattice
class node:
    def __init__(self, word, leftID, rightID, cost, prevNode, pos, lemma):
        self.word = word
        self.leftID = leftID
        self.rightID = rightID
        self.cost = cost
        self.prevNode = prevNode
        self.pos = pos
        self.lemma = lemma


# lattice[0] = [nodea, nodeb, ...] for words starting at position i
# lattice[1] = [nodea, nodeb, ...] for words ending at position i-1
def generate_lattice(text, words):
    lattice = [[[] for _ in range(len(text) + 1)], [[] for _ in range(len(text) + 1)]]
    for i in range(len(text)):
        char = text[i]
        if char in words:
            for word_info in words[char]:
                word = word_info[0]
                leftId = word_info[1]
                rightId = word_info[2]
                cost = word_info[3]
                part_of_speech = word_info[4]
                lemma = word_info[5]
                word_node = node(
                    word, leftId, rightId, cost, None, part_of_speech, lemma
                )
                if text[i : i + len(word)] == word:
                    lattice[0][i].append(word_node)
                    lattice[1][i + len(word)].append(word_node)
    return lattice


# best_path = parse of the best path for the given lattice
def best_path(lattice, matrix):
    # Iterate through each position in the lattice
    for i in range(len(lattice[0])):
        # If there are no paths at this position, skip
        if not lattice[0][i]:
            continue
        # Iterate through each path at this position
        for path in lattice[0][i]:
            # Handle special start node
            if i == 0:
                path.cost = path.cost + matrix[(0, path.leftID)]
                continue
            # Check costs to every node that ends at i-1
            best_cost = float("inf")
            prevNode = None
            for node in lattice[1][i]:
                if node.cost == float("inf"):
                    continue
                total_cost = path.cost + matrix[(node.rightID, path.leftID)]
                if total_cost < best_cost:
                    best_cost = total_cost
                    prevNode = node
            path.cost = best_cost
            path.prevNode = prevNode
    # Find optimal cost to end
    final_cost = float("inf")
    final_node = None
    for last_node in lattice[1][len(lattice[1]) - 1]:
        if last_node.cost == float("inf"):
            continue
        total_cost = last_node.cost + matrix[(last_node.rightID, 0)]
        if total_cost < final_cost:
            final_cost = total_cost
            final_node = last_node
    # Return best path
    output = []
    while final_node is not None:
        output.append(final_node)
        final_node = final_node.prevNode
    output = output[::-1]
    return output


def read_sentences():
    filename = "sentences.txt"
    sentences = ["東京都に住む人々。"]
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
            print(token.word + " " + token.pos + " " + token.lemma)


if __name__ == "__main__":
    main()
