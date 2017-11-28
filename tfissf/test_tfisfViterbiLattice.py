# coding: utf-8
import codecs
import sys
from segment_katakana_tfisf import TfisfViterbiLattice
import unittest
from unittest import TestCase
from sklearn.model_selection import KFold

TF_TRIE = "TF_TRIE"
ISF_TRIE = "ISF_TRIE"

class TestTfisfViterbiLattice(TestCase):

    def test_segment_hashtags(self):
        in_file = "TEST_FILE"
        test_file = codecs.open(in_file, "r", "utf-8")
        test_file_out = codecs.open(in_file + "_tfisf_result.txt", "w", "utf-8")
        self.segment_and_output(test_file, test_file_out)
        print "Finished segmenting hashtags using only tf-isf"

    # @unittest.skip("testing skipping")
    def test_segment(self):
        compound_word_candidates = [u'マイナンバー']

        tfisf_viterbi_lattice = TfisfViterbiLattice()
        tfisf_viterbi_lattice.set_tf_trie(TF_TRIE)
        tfisf_viterbi_lattice.set_isf_trie(ISF_TRIE)
        for word in compound_word_candidates:
            decoded_segments = tfisf_viterbi_lattice.construct_lattice(word)
            print word + " -> " + " ".join(decoded_segments)

    # @unittest.skip("testing skipping")
    def test_segment_bccwj(self):
        training_filename = "TRAINING_FILENAME"
        f = codecs.open(training_filename, "r", "utf-8")
        training_lines = f.readlines()
        splitted_training = []
        splitted_tests = []
        data_indice = list(range(len(training_lines)))
        f.close()
        kf = KFold(n_splits=3, shuffle=True, random_state=1)
        for train_index, test_index in kf.split(data_indice):
            print(len(train_index), len(test_index))
            splitted_training.append(train_index)
            splitted_tests.append(test_index)

        tfisf_viterbi_lattice = TfisfViterbiLattice()  # replace spaces
        tfisf_viterbi_lattice.set_tf_trie(TF_TRIE)
        tfisf_viterbi_lattice.set_isf_trie(ISF_TRIE)
        for i, splitted_test in enumerate(splitted_tests):
            test_file = []
            for test_index in splitted_test:
                print(test_index)
                test_file.append(training_lines[test_index])
            test_file_out = codecs.open(training_filename + "_tfisf_result_20151226_%i.txt" % i, "w", "utf-8")
            for katakana in test_file:
                space_deleted = katakana[:-1].replace(" ", "")
                decoded_segments = tfisf_viterbi_lattice.construct_lattice(space_deleted)
                print space_deleted + " -> " + " ".join(decoded_segments)
                test_file_out.write(" ".join(decoded_segments).rstrip() + "\n")

    def segment_and_output(self, test_file, test_file_out):
        tfisf_viterbi_lattice = TfisfViterbiLattice()
        tfisf_viterbi_lattice.set_tf_trie(TF_TRIE)
        tfisf_viterbi_lattice.set_isf_trie(ISF_TRIE)
        for katakana in test_file:
            print(katakana[:-1])

            decoded_segments = tfisf_viterbi_lattice.construct_lattice(katakana[:-1].replace(" ", ""))
            # print katakana[:-1] + " -> " + " ".join(decoded_segments)
            test_file_out.write(" ".join(decoded_segments).rstrip() + "\n")
