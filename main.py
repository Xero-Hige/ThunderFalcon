# coding=utf-8
import random

from normalizationTools import normalize

__author__ = 'hige'

NGRAM = 2
STOPCHARS = "\n\t '\"?()¡¿[]{}=.:,;"


def main():
    texts = []
    """ with open("/home/hige/Okami/ex1.html") as fle:
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
                    filo.writelines(normalized + "\n") """

    with open("train.xp") as train:
        for line in train:
            text = line[2:]
            text = normalize(text)
            label = int(line[0])
            texts.append([text, label])
    print "Loaded file"
    total_features = {}
    for values_text in texts:
        text = values_text[0]
        features = extract_features(text)
        values_text[0] = features

        for feature in features:
            total_features[feature] = total_features.get(feature, 0) + 1

    print "Loaded features"
    chosen_features = choose_features(total_features, len(texts))
    # vectors = vectorize([text], chosen_features)
    print "Chosen features"
    # for count, feature in chosen_features:
    #    print feature, "-", count, "\n"

    for line in texts:
        for feature in line[0]:
            # print feature
            if feature not in chosen_features:
                line[0].pop(feature)
        line[1] = [1 if x == line[1] else -1 for x in xrange(1, 5)]

    print "Loaded train data"

    perceptron = Perceptron(chosen_features)

    perceptron.train(texts)

    _input = raw_input("Tweet: ")
    while _input:
        features = extract_features(_input)
        selected = {}
        for feature in features:
            if feature in chosen_features:
                selected[feature] = 1

        print perceptron.responses(selected)
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
        if float(count) / n > threshold:
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


class Perceptron(object):
    def __init__(self, features):
        self.features = features
        self.langs = ["english", "spanish", "another", "unknown"]

        classes = {}

        for lang in self.langs:
            classes[lang] = {}

        self.learning_rate = 0.1

        for feature in features:
            for class_name, _class in classes.items():
                _class[feature] = ((random.random() - 0.5) * 2) / len(features)  # .randrange(-1.0, 1.0)

        self.classes = classes

    def response(self, _input, class_name):
        result = 0
        _class = self.classes[class_name]
        for feature in self.features:
            result += _class[feature] * _input.get(feature, 0)
        return result

    def responses(self, _input):
        response = []
        for class_name in self.langs:
            result = self.response(_input, class_name)

            print class_name, " - ", result
            if result > 0:
                response.append(class_name)

        return response

    def train(self, train_data):
        it = 0
        prev = 0.0
        while True:
            global_error = 0.0
            random.shuffle(train_data)
            for data in train_data:
                errors = []
                for i in xrange(len(self.langs)):
                    name = self.langs[i]
                    result = self.response(data[0], name)
                    expected = data[1][i]

                    error = expected - result

                    if error != 0.0:
                        vector = self.classes[name]
                        self.update_vectors(data[0], vector, error)

                    errors.append(error)

                global_error += abs(max(errors))
            it += 1
            if it > 100 or global_error == 0.0:  # je or global_error - prev < 0.3:
                print "Learned in ", it, " iterations: (", global_error, ")"
                break
            else:
                print "No aprendi un carajo vieja (", it, ") Error -", global_error, "-"
                prev = global_error

    def update_vectors(self, data, vector, error):
        coordinates = sorted(vector.keys())
        factor = len(data.keys())
        for coordinate in coordinates:
            if coordinate in data:
                # print data
                vector[coordinate] += ((data[coordinate] * error) / factor)


main()
