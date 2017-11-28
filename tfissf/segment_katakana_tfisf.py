# coding: utf-8

import pickle
import codecs
import math
from simple_viterbi import ViterbiLattice

data_dir = ""
TF_TRIE = "data/tf_trie_20151226.txt"
ISF_TRIE = "data/isf_trie_20151226.txt"

class TfisfViterbiLattice(ViterbiLattice):
    tf_trie = None
    isf_trie = None

    def __init__(self):
        super(TfisfViterbiLattice, self).__init__()

    def set_tf_trie(self, tf_datafile):
        tf_data = open(tf_datafile, 'rb')
        self.tf_trie = pickle.load(tf_data)

    def set_isf_trie(self, isf_datafile):
        isf_data = open(isf_datafile, 'rb')
        self.isf_trie = pickle.load(isf_data)

    def compute_score(self, substring):
        score = 0 # unknown substring
        if substring in self.tf_trie and substring in self.isf_trie:
            score = self.tf_trie[substring][0][0] * 1.0 / self.isf_trie[substring][0][0]

        return score

def extract_segmented_substrings(word):
    substrings = []
    for i in range(len(word)):
        for j in range(i+1, len(word) + 1):
            substrings.append(word[i:j])
    return substrings

if __name__ == "__main__":
    compound_word_candidates = [u"スマホケース", u"エナジードリンク"]
    tfisf_viterbi_lattice = TfisfViterbiLattice()
    data_dir = ""
    tfisf_viterbi_lattice.set_tf_trie(data_dir + TF_TRIE)
    tfisf_viterbi_lattice.set_isf_trie(data_dir + ISF_TRIE)
    for word in compound_word_candidates:
        decoded_segments = tfisf_viterbi_lattice.construct_lattice(word)
        print(word + " -> " + " ".join(decoded_segments))
