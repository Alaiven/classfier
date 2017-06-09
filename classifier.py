# coding: utf-8

import re
import math
import sys
from random import randint

class Cluster(object):
    """ Cluster """

    def __init__(self):
        self.vectors = []

    def add(self, vector):
        self.vectors.append(vector)

    def remove(self, vector):
        self.vectors.remove(vector)

    def contains(self, vector):
        return vector in self.vectors

    def get_probability(self, value, index):
        """Probability of value in vector[index] in cluster being == value """
        count = 0
        for vector in self.vectors:
            if vector[index] == value:
                count += 1
        return count / float(len(self.vectors))

    def part_cost(self, value, index):
        """ Cost for vector[index] in given cluster """
        return -math.log(
            (self.get_probability(value, index) * len(self.vectors) + 1)
            / float(len(self.vectors) + 1)
            , 2)

    def whole_cost(self, vector):
        """ Cost for the whole vector in cluster """
        cost = 0
        for idx, val in enumerate(vector.values):
            cost += self.part_cost(val, idx)
        return cost

    def __str__(self):
        return "   ----   Cluster \n" + "\n".join([str(v) for v in self.vectors])

class Vector(object):
    """Vector class"""

    def __init__(self, data, values):
        self.data = data
        self.values = values

    def __getitem__(self, key):
        return self.values[key]

    def __str__(self):
        return ' '.join(self.data)

def prepare_file(in_file):
    """ Gets file, removes all unnecessary characters, splits into lists containing sentences """
    with open(in_file, 'r') as f:

        letter_pattern = re.compile("[^A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ. ]", re.UNICODE)
        space_patern = re.compile(r"\s{2,}")

        text = f.read()
        text = text.replace("?", ".")
        text = text.replace("!", ".")
        text = text.replace(";", ".")
        text = letter_pattern.sub(" ", text)
        text = space_patern.sub(" ", text)

        text = text.split('.')
        return [list(word_generator_line(l)) for l in text]

def word_generator_line(line):
    """ Generates word list from sentence, maybe dirty list """
    words = line.split(" ")
    for word in words:
        word = word.replace(" ", "")
        if word != "":
            yield word

def word_generator(lines):
    """ Iterates over all words """
    for line in lines:
        for word in line:
            yield word

def make_dict(lines):
    """ Creates unique list with all words """
    word_dict = []
    for word in word_generator(lines):
        if word not in word_dict:
            word_dict.append(word)
    return word_dict

def count_words(line, word):
    """ Counts how many times word is present in line """
    count = 0
    for item in line:
        if item == word:
            count += 1
    return count

def make_vector(line, word_dict):
    """ Creates vector of occurances for line """
    return [count_words(line, w) for w in word_dict]


def make_vectors(lines, word_dict):
    """ Creates a list of Vector objects, containing occurances of lines """
    return [Vector(l, make_vector(l, word_dict)) for l in lines]

def initialize_random_clusters(vectors, clusters_len):
    clusters = [Cluster() for _ in range(clusters_len)]
    for vector in vectors:
        rand_int = randint(0, clusters_len - 1)
        clusters[rand_int].add(vector)
    return clusters

def Initialize_clusters(vectors, clusters_len):
    clusters = [Cluster() for _ in range(clusters_len)]
    for vector in vectors:
        option_ok = False
        while not option_ok:
            print "  --  " + str(vector)
            option = raw_input("In which cluster goes this sentence? Count from 1 to clusters length: ")
            option = int(option)
            option_ok = option > 0 and option <= clusters_len
            if option_ok:
                clusters[option - 1].add(vector)
            else:
                print "Invalid option"
    return clusters

def remove_vector(clusters, vector):
    for idx, cluster in enumerate(clusters):
        if cluster.contains(vector):
            cluster.remove(vector)
            return idx
    return -1

def get_lower_cost_index(clusters, vector):
    cost = sys.maxint
    index = -1
    print " ---  "
    for idx, cluster in enumerate(clusters):
        new_cost = cluster.whole_cost(vector)
        print "Cost: " + str(new_cost)
        if new_cost < cost:
            cost = new_cost
            index = idx
    return index

def calculate_clusters(vectors, clusters):
    shift = True

    while shift:
        shift = False
        for vector in vectors:

            old_index = remove_vector(clusters, vector)
            new_index = get_lower_cost_index(clusters, vector)
            shift = old_index != new_index
            clusters[new_index].add(vector)

    return clusters


IN_FILE = raw_input("Input file name: ")

LIST = prepare_file(IN_FILE)

WORD_DICT = make_dict(LIST)

print "dict done list: %d dict %d" % (len(LIST), len(WORD_DICT))

VECTORS = make_vectors(LIST, WORD_DICT)

CLUSTERS_NUM = raw_input("Provide the number of clusters: ")
CLUSTERS_NUM = int(CLUSTERS_NUM)

OPTION = raw_input("Initializing options: 1 - random, 2 - manual: ")
OPTION = int(OPTION)

CLUSTERS = []

if OPTION == 1:
    CLUSTERS = initialize_random_clusters(VECTORS, CLUSTERS_NUM)
elif OPTION == 2:
    CLUSTERS = Initialize_clusters(VECTORS, CLUSTERS_NUM)
else:
    print "Invalid option"

for cl in CLUSTERS:
    print cl

CLUSTERS = calculate_clusters(VECTORS, CLUSTERS)

for cl in CLUSTERS:
    print cl


