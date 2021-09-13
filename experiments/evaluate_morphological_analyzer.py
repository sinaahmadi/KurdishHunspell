#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	Sina Ahmadi (ahmadi.sina@outlook.com)
	Evaluation script for the paper entitled "Hunspell for Sorani Kurdish Spell Checking and Morphological Analysis"
	This script evaluates the performance of a morphological analyzer in comparison to a gold-standard.
	The gold-standard file should be a tab-separated file (.tsv) with the following columns in order:
		- word
		- lemma
		- pos
		- stem
		- prefixes
		- base
		- suffixes
		- description

	Kurdish Hunspell Project: https://github.com/sinaahmadi/KurdishHunspell
	2020-2021
	Last updated on September 13, 2021
"""
import json 
from klpt.stem import Stem

def extract_prefix_suffix(word_form, base):
	# given a substring, find the preceding and succeeding characters as prefix and suffix, respectively
	if word_form == base:
		return '', word_form, ''
	elif len(word_form) > len(base):
		for i in range(len(word_form)):
			if i + len(base) < len(word_form) and word_form[i: i+len(base)] == base:
				return word_form[0:i], base, word_form[i + len(base):]


if __name__ == "__main__":
	# evaluation
	stemmer = Stem("Sorani", "Arabic")

	# calculate coverage
	if False:
		analyzed = 0
		with open("ALL_ckb_frequency_10_cleaned_sorted.txt", "r") as f:
			all_corpus = f.read().split("\n")
			for i in all_corpus:
				if len(stemmer.analyze(i.split("\t")[0])):
					analyzed += 1
		print("Coverage is ", (analyzed * 100) /len(all_corpus))

	correct_segmentation, correct_pos, correct_verb_stemming = 0, 0, 0
	verb_counter = 0
	with open("KurdishHunspell_Evaluation - morphological_analysis_testset.tsv", "r") as f:
		test_set = f.read().split("\n")[5:]
		for i in test_set:
			i = i.split("\t")
			analysis = stemmer.analyze(i[0])
			
			if len(analysis):
				for a in analysis:
					analysis_pfx_sfx = extract_prefix_suffix(i[0], a["base"])

					if (i[4], i[5], i[6]) == analysis_pfx_sfx:
						correct_segmentation += 1
					
					# for pos in i[2].split("|"):
					if a["pos"] in i[2]:
						correct_pos += 1
					else:
						pass
						# print(a["pos"], i, a)

					if "verb" in i[2] and '|' not in i[2]:
						verb_counter += 1
						if "stem" in a:
							if i[3] == a["stem"]:
								correct_verb_stemming += 1
						# else:
						# 	print(i)
			else: 
				pass
				# print(i)

		print("segmentation score: ", correct_segmentation * 100 / (len(test_set)-5))
		print("POS score: ", correct_pos * 100 / (len(test_set)-5))
		print("stemming score: ", correct_verb_stemming * 100 / verb_counter)
