import random

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
                    fil.writelines(line + "\n")
                    filo.writelines(normalized + "\n")

    total_features = {}
    texts_features = []
    for text in texts:
        features = extract_features(text)
        texts_features.append(features)

        for feature in features:
            total_features[feature] = total_features.get(feature, 0) + 1

    chosen_features = choose_features(total_features, len(texts))
    # vectors = vectorize([text], chosen_features)

    # for count, feature in chosen_features:
    #    print feature, "-", count, "\n"

    train_data = []

    with open("train.xp") as train:
        i = 0
        for line in train:
            label = int(line[0])
            train_data.append([texts_features[i], [1 if x == label else -1 for x in xrange(1, 5)]])

    perceptron = Perceptron(chosen_features)

    perceptron.train(train_data)

    _input = raw_input("Tweet: ")
    while _input:
        features = extract_features(_input)
        selected = {}
        for feature in features:
            if feature in chosen_features:
                selected[feature] = 1

        print perceptron.response(selected)
        _input = raw_input("Tweet: ")


def extract_features(text):
    features_accumulator = {}
    words = text.split()
    for i in range(len(words)):
        first = words[i]
        if len(first) == 1:
            continue
        if first.isdigit():
            continue
        features_accumulator[first] = 1
        for j in range(i + 1, len(words)):
            second = words[j]
            if len(second) == 1:
                continue
            if second.isdigit():
                continue
            features_accumulator[first + " " + second] = 1

    for i in xrange(len(text)):
        if text[i] in STOPCHARS or text[i].isdigit():
            continue
        features_accumulator[text[i:i + NGRAM]] = 1

    return features_accumulator


def choose_features(features, n, threshold=1):
    selected = []
    for feature, count in features.items():
        if float(count) / n > threshold or count == 1:
            continue
        selected.append(feature)  # (feature,count))
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


class Perceptron():
    def __init__(self, features):
        self.features = features
        self.langs = ["english", "spanish", "another", "unknown"]

        classes = {}

        for lang in self.langs:
            classes[lang] = {}

        self.learning_rate = 0.1

        for feature in features:
            for class_name, _class in classes.items():
                _class[feature] = random.randrange(-1.0, 1.0)

        self.classes = classes

    def response(self,_input,class_name):
        result = 0
        _class = self.classes[class_name]
        for feature in self.features:
            result += _class[feature] * _input.get(feature, 0)
        return result

    def responses(self, _input):
        response = []
        for class_name in self.langs:
            result = self.response(_input,class_name)

            print class_name, " - ", result
            if result > 0:
                response.append(class_name)

        return response

    def train(self, train_data):
        it = 0
        while True:
            global_error = 0.0
            for data in train_data:
                r = self.responses(data[0])
                for i in xrange(len(self.langs)):
                    name = self.langs[i]
                    if data[1][i] == 1:
                        if name not in r:
                            vector = self.classes[name]
                            self.update_vectors(data, vector, 2)
                            global_error += 0.2
                    else:
                        if name in r:
                            vector = self.classes[name]
                            self.update_vectors(data, vector, -2)
                            global_error += 0.2
            it += 1
            if it > 20 or global_error == 0.0:
                print "Learned in ", it, " iterations: (", global_error, ")"
                break
            else:
                print "No aprendi un carajo vieja (", it, ") Error -", global_error, "-"

    def update_vectors(self, data, vector, error):
        for coordinate in vector.keys():
            vector[coordinate] += data[0].get(coordinate, 0) * self.learning_rate * error


main()
