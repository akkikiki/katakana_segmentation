# coding: utf-8
# TODO: Construct a Viterbi lattice with the first dimentsion is respective to i
# TODO: Then, look up its bigram feature using that the current substring and viterbi_lattice[j-1]

import json

class ViterbiLattice(object):


    def __init__(self):
        self.product_score = True
        # self.lattice_ending_at_j = [[] for j in range(len(target_word) + 1)] # x: word ending at indice x, y: list of words

        self.use_hyperparameter = False # not implemented yet
        self.lambdas = []
        self.blacklist_starting_char = [u"ー", u'ァ', u'ィ', u'ゥ', u'ェ',u'ォ', u'ヵ', u'ヶ', u'ッ', u'ャ', u'ュ', u'ョ', u'ヮ']
        self.german = False
        self.stopwords = []


        hyperparameter = 0
        for i in range(10):
            self.lambdas.append(hyperparameter)
            hyperparameter += 0.1

    def construct_lattice(self, target_word):
        """ what is needed
            1. the best word ending at indice i
            e.g. abc -> "a b c", "ab c", "a bc", "abc"
            * so for the indice 0, it is always the first character, in this case "a"
            * for 1, it is either "b" or "ab"
            * for 2, it is eiter "c", "bc" or "abc"
        """
        self.lattice_ending_at_j = [[] for j in range(len(target_word) + 1)] # x: word ending at indice x, y: list of words

        best_word_ending_at_j = [u""] * (len(target_word) + 1) # 0: none
        best_score_ending_at_j = [0] * (len(target_word) + 1) # 0: none
        best_score_ending_at_j[0] = 1 # no previous character
        for i in range(len(target_word)):
            for j in range(i+1, len(target_word) + 1):
                substring = target_word[i:j]

                # if len(target_word) != 1 and substring[0] in [u"ー", u'ァ', u'ィ', u'ゥ', u'ェ', u'ォ', u'ャ', u'ュ', u'ョ']:
                if len(target_word) != 1 and substring[0] in self.blacklist_starting_char:
                    continue

                if substring in self.stopwords or substring.lower() in self.stopwords:
                    # print("skipping %s..." % substring)
                    continue # skip stopwords

                self.lattice_ending_at_j[j].append(substring) # building the Viterbi Lattice here
                # Then, refer to all possible previous substrings that ends at j - len(substring)

                computed_score = self.compute_score(substring)

                if self.product_score:
                    current_score = 1.0 * best_score_ending_at_j[i] * computed_score
                else:
                    # use sum
                    current_score = 1.0 * best_score_ending_at_j[i] + computed_score

                # current_score = 1.0 * best_score_ending_at_j[i] + computed_score

                if current_score > best_score_ending_at_j[j]:
                    best_word_ending_at_j[j] = substring
                    best_score_ending_at_j[j] = current_score

                if self.german and len(substring) > 1:
                # if self.german:
                    capitalized_score = 1.0 * best_score_ending_at_j[i] * self.compute_score(substring.title())
                    if capitalized_score > current_score and capitalized_score > best_score_ending_at_j[j]:
                        best_word_ending_at_j[j] = substring.title()
                        best_score_ending_at_j[j] = capitalized_score

                # if self.german and len(substring) > 1 and i == 0:
                #     uncapitalized_score = 1.0 * best_score_ending_at_j[i] * self.compute_score(substring.lower())
                #     if uncapitalized_score > current_score and uncapitalized_score > best_score_ending_at_j[j]:
                #         best_word_ending_at_j[j] = substring.lower()
                #         best_score_ending_at_j[j] = uncapitalized_score

        # Backword decoding
        decoded_segment = []
        j = len(target_word)
        while j > 0:
            if best_word_ending_at_j[j] == "":
                # in case there is no char entry in the training corpus
                # e.g. BCCWJ: ㇻ exists
                best_word_ending_at_j[j] = target_word[0:j]
            decoded_segment.insert(0, best_word_ending_at_j[j])
            j -= len(best_word_ending_at_j[j])
            # print best_word_ending_at_j
            # print best_score_ending_at_j

        return decoded_segment

    def compute_score(self, substring):
        # to be overrided
        return 0

    def set_stopwords(self, filename):
        print("adding stopwords...")
        self.stopwords = json.load(filename)
        print(self.stopwords)