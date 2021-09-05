#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	Sina Ahmadi (ahmadi.sina@outlook.com)
	Evaluation script for the paper entitled "Hunspell for Sorani Kurdish Spell Checking and Morphological Analysis"
	Kurdish Hunspell Project: https://github.com/sinaahmadi/KurdishHunspell
	2020-2021
	Last update on September 5, 2021
"""
import json 
from Levenshtein import distance
from klpt.stem import Stem
from sklearn import metrics

baseline_words = list()
with open("ALL_ckb_frequency.txt", "r") as f:
	for i in f.read().split("\n")[1:]:
		if len(i.strip().split()) == 2:
			baseline_words.append(i.strip().split()[1])

def baseline_spellchecker(word):
	"""
	This baseline system, looks up the input word in the list of the 10 most frequent words which are extracted
	from the Pewan, AsoSoft and Sorani Kurdish folkloric corpora. 
	if the input word exists in that list, it is considered correct. 
	Otherwise, suggestions are provided based on the Levenshtein edit distance.
	"""
	suggestions = dict()
	if word in baseline_words:
		return True
	else:
		for i in baseline_words:
			suggestions[i] = distance(word, i)
	
	ten_suggestions = dict()
	for sugg in list({k: v for k, v in sorted(suggestions.items(), key=lambda item: item[1])}.items())[:10]:
		ten_suggestions[sugg[0]] = sugg[1]

	return ten_suggestions

def calculate_suggestion_accuracy(word, corrected_word, suggestions, n=1):
	"""
		given a word and a list of correction suggestions, calculate accuracy based on the ranking (n)
		word: potentially incorrectly spelled word
		corrected_word: gold-standard correction
	"""
	if suggestions == True:
		if word == corrected_word:
			return "1"
		else:
			return "0"
	else:
		if corrected_word in suggestions[0:n]:
			return "1"
		else:
			return "0"

def evaluate_Kurdish_hunspell(word):
	suggestions = list()
	stemmer = Stem("Sorani", "Arabic")
	if stemmer.check_spelling(word) == False:
		return stemmer.correct_spelling(word)[1]
	else:
		return True

def run(test_set, filename, is_baseline=True):
	# Evaluate the baseline system based on the given test set
	# test_set -> word: gold-standard correction
	# file_name: name of the output file containing suggestions and evaluations
	baseline = dict()
	dataset_evaluated = list()

	for entry in test_set:
		entry_eval = list() # a line in the final tsv file corresponding to the evaluation of the outputs

		word = entry # input word
		corrected_word = test_set[entry] # corrected gold-standard
		if is_baseline:
			baseline[word] = baseline_spellchecker(word)
		else:
			baseline[word] = evaluate_Kurdish_hunspell(word)

		entry_eval.append(word)
		entry_eval.append(corrected_word)
		# print(word, corrected_word, baseline[word])

		if baseline[word] != True:
			if is_baseline:
				entry_eval.append(",".join(list(baseline[word].keys())))
			else:
				entry_eval.append(",".join(baseline[word]))
		else:
			entry_eval.append("detected_correct")

		for rank in [1, 3, -1]: # checking correction suggestions based on the ranking
			if baseline[word] != True:
				if is_baseline:
					entry_eval.append(calculate_suggestion_accuracy(word, corrected_word, list(baseline[word].keys()), rank))
				else:
					entry_eval.append(calculate_suggestion_accuracy(word, corrected_word, baseline[word], rank))
			else:
				entry_eval.append(calculate_suggestion_accuracy(word, corrected_word, baseline[word], rank))

		dataset_evaluated.append("\t".join(entry_eval))


	# with open('%s_baseline_suggestions.json'%filename, 'w', encoding='utf8') as t1_json:    
	#     json.dump(baseline, t1_json, indent=4)

	# with open("%s_dataset_evaluation.tsv"%filename, "w") as f:
	# 	f.write("word\tcorrected_gold\tsystem_suggestions\tin_1\tin_3\tin_above_3\n" + "\n".join(dataset_evaluated))

	return dataset_evaluated

def evaluate(experiments):
	# given the output of the evaluation of a spell checking system, calculate performance
	performance = {
		"accuracy": "",
		"precision": "",
		"recall": "",
		"F1": "",
		"sugg_1": "",
		"sugg_3": "",
		"sugg>_3": ""
	}

	confusion = {"TP": 0, "FP": 0, "TN":0, "FN": 0}
	# true positive (TP) for correctly detected correct words.
    # false positive (FP) for incorrectly detected correct words.
    # true negative (TN) for correctly detected incorrect words.
    # false negative (FN) for incorrectly detected incorrect words.

	for i in experiments: # only the first suggestion is taken into account
		print(i)
		i = i.split("\t")
		if i[2] != "detected_correct":
			if i[1] in i[2].split(","):
				if i[0] == i[1]:
					confusion["FP"] += 1
				else:
					confusion["TN"] += 1
			else:
				if i[0] == i[1]:
					confusion["FP"] += 1
				else:
					confusion["FN"] += 1

		else: #detected_correct
			if i[0] == i[1]:
				confusion["TP"] += 1
			else:
				confusion["FN"] += 1

	
	print(confusion)
	performance["precision"] = confusion["TP"] / (confusion["TP"] + confusion["FP"]) 
	performance["recall"] = confusion["TP"] / (confusion["TP"] + confusion["FN"])
	performance["F1"] = 2 * confusion["TP"] / (2 * confusion["TP"] + confusion["FP"] + confusion["FN"])
	performance["accuracy"] = (confusion["TP"] + confusion["TN"]) / (confusion["TP"] + confusion["FP"] + confusion["TN"] + confusion["FN"])

	# "\t".join(list(confusion.values())) + 
	print(performance)


	# for i in experiments:
	# 	for sugg in {1:3, 3:4, 4:5}
	# 	i.split("\t")



if __name__ == "__main__":
	# evaluation
	test_set = dict()
	# with open("Kurdish-Spelling-TestSet-Amani.tsv") as f: # Amani's
	# 	for i in f.read().split("\n")[2:10]:
	# 		test_set[i.split("\t")[0]] = i.split("\t")[1]

	# # print("Evaluating baseline")
	# # run(test_set, "T1")
	# print("Evaluating Hunspell")
	# spell_checker_output = run(test_set, "T1_hunspell", is_baseline=False)
	# # evaluate(spell_checker_output)
	# print(spell_checker_output)

	
	test_set = dict()
	with open("Kurdish-Spelling-TestSet-NeteweNet.tsv", "r") as f:  # Mahmudi's
		for i in f.read().split("\n")[10:30]:
			test_set[i.split("\t")[0]] = i.split("\t")[1]
	# print("Evaluating baseline")
	# run(test_set, "T2")
	print("Evaluating Hunspell")
	spell_checker_output = run(test_set, "T2_hunspell", is_baseline=False)
	print(spell_checker_output)
	evaluate(spell_checker_output)
	
	# test_set = dict()
	# with open("Kurdish-Spelling-TestSet-NeteweNet.tsv", "r") as f:  # Mahmudi's
	# 	for i in f.read().split("\n")[2:]:
	# 		if i.split("\t")[4] == "0":
	# 			test_set[i.split("\t")[0]] = i.split("\t")[1]
	# print("Evaluating baseline")
	# run(test_set, "T2_nospace")
	# print("Evaluating Hunspell")
	# run(test_set, "T2_nospace_hunspell", is_baseline=False)
		

