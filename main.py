from normalizationTools import normalize

__author__ = 'hige'

NGRAM = 2
STOPCHARS = ["\n", "\t", " "]


def main():
    texts = []
    with open("/home/hige/Okami/ex1.html") as fle:
        with open("/home/hige/Okami/bulk1.txt", 'w') as fil:
            with open("/home/hige/Okami/bulk2.txt", 'w') as filo:
                lines = fle.readlines()
                for i in range(len(lines)):
                    if '<p id="p3">' not in lines[i]:
                        continue
                    line = ""
                    i += 1
                    while "<p>" not in lines[i]:
                        line += lines[i]
                        i += 1

                    line = line.replace("\n", " ")
                    line = line.replace("\t", "")
                    line = line.replace('<a href="', "")
                    line = line.replace('">', "")
                    line = line.replace("</a>", "")

                    normalized = normalize(line)

                    texts.append(normalized)
                    fil.writelines(line+"\n")
                    filo.writelines(normalized+"\n")

    total_features = {}
    for text in texts:
        features = extract_features(text)
        for feature in features:
            total_features[feature] = total_features.get(feature, 0) + 1

    chosen_features = choose_features(total_features, len(texts))
    # vectors = vectorize([text], chosen_features)

    for count, feature in chosen_features:
        print feature, "-", count, "\n"


def extract_features(text):
    features_accumulator = {}
    words = text.split()
    for i in range(len(words)):
        first = words[i]
        if len(first) == 1:
            continue
        if first.isdigit():
            continue
        features_accumulator[first] = ""
        for j in range(i + 1, len(words)):
            second = words[j]
            if len(second) == 1:
                continue
            if second.isdigit():
                continue
            features_accumulator[first + " " + second] = ""

    for i in xrange(len(text)):
        if text[i] in STOPCHARS or text[i].isdigit():
            continue
        features_accumulator[text[i:i + NGRAM]] = ""

    return features_accumulator.keys()


def choose_features(features, n, threshold=1):
    selected = []
    for feature, count in features.items():
        if float(count) / n > threshold or count == 1:
            continue
        selected.append((count, feature))
    selected.sort(reverse=False)
    return selected


def vectorize(texts, features):
    vectors = []
    for i in xrange(len(texts)):
        text_features = extract_features(texts[i])
        vector = {}
        for feature in features:
            if feature in text_features:
                vector[feature] = 1
        result = (i, vector)
        vectors.append(result)
    return vectors


main()