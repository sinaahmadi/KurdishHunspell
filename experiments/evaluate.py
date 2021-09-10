#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	Sina Ahmadi (ahmadi.sina@outlook.com)
	Evaluation script for the paper entitled "Hunspell for Sorani Kurdish Spell Checking and Morphological Analysis"
	This script evaluates the precisions of a spell checking system in comparison to a gold-standard.
	The gold-standard file should be a tab-separated file (.tsv) with the following columns in order:
		- word
		- corrected form 
	Kurdish Hunspell Project: https://github.com/sinaahmadi/KurdishHunspell
	2020-2021
	Last updated on September 7, 2021
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

def run(test_set, filename, is_baseline=True, save_file=True):
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

	if save_file:
		with open('%s_suggestions.json'%filename, 'w', encoding='utf8') as t1_json:    
		    json.dump(baseline, t1_json, indent=4)

		with open("%s_evaluation.tsv"%filename, "w") as f:
			f.write("word\tcorrected_gold\tsystem_suggestions\tin_1\tin_3\tin_above_3\n" + "\n".join(dataset_evaluated))

	return dataset_evaluated

def evaluate(experiments, calculate_PR=False):
	# given the output of the evaluation of a spell checking system, calculate performance
	# measures calculated according to http://www.puk.ac.za/opencms/export/PUK/html/fakulteite/lettere/ctext/Article.RES.VanHuyssteenxEiselenxPuttkammer2004.9.9.9.GBVH.2008-09-13.FinalxSmallx.pdf
	# lexical precision, lexical recall	
	confusion = {"TP": 0, "FP": 0, "TN":0, "FN": 0}
	performance = {
		"accuracy": 0,
		"precision": 0,
		"recall": 0,
		"F1": 0,
		"sugg_1": 0,
		"sugg_3": 0,
		"sugg>_3": 0
	}
	incorrect_cases = 0

	# true positive (TP) for correctly detected correct words.
    # false positive (FP) for incorrectly detected correct words.
    # true negative (TN) for correctly detected incorrect words.
    # false negative (FN) for incorrectly detected incorrect words.

	for i in experiments: # only the first suggestion is taken into account
		i = i.split("\t")
		if len(i[1]): # this skips the first few words of T2
			if i[2] != "detected_correct":
				if i[1] in i[2].strip().split(","):
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

		# evaluate ranking for the prediction of incorrect words
		if i[0] != i[1]:
			incorrect_cases += 1
			if i[3] == "1":
				performance["sugg_1"] += 1
			if i[4] == "1":
				performance["sugg_3"] += 1
			if i[5] == "1":
				performance["sugg>_3"] += 1
	
	performance["sugg_1"] = performance["sugg_1"] / incorrect_cases
	performance["sugg_3"] = performance["sugg_3"] / incorrect_cases
	performance["sugg>_3"] = performance["sugg>_3"] / incorrect_cases

	if calculate_PR:
		performance["precision"] = confusion["TP"] / (confusion["TP"] + confusion["FP"]) 
		performance["recall"] = confusion["TP"] / (confusion["TP"] + confusion["FN"])
		performance["F1"] = 2 * confusion["TP"] / (2 * confusion["TP"] + confusion["FP"] + confusion["FN"])
		performance["accuracy"] = (confusion["TP"] + confusion["TN"]) / (confusion["TP"] + confusion["FP"] + confusion["TN"] + confusion["FN"])

	print("Confusion matrix is: ", confusion)
	print("System performance: ", performance)

if __name__ == "__main__":
	# evaluation
	print("# =================== T1 (Amani's)")
	test_set = dict()
	with open("Kurdish-Spelling-TestSet-Amani.tsv") as f: # Amani's
		for i in f.read().split("\n")[2:]:
			test_set[i.split("\t")[0]] = i.split("\t")[1]

	print("= Evaluating baseline")
	spell_checker_output = run(test_set, "T1_baseline")
	evaluate(spell_checker_output)

	print("= Evaluating Hunspell")
	spell_checker_output = run(test_set, "T1_hunspell", is_baseline=False)
	evaluate(spell_checker_output)

	print("\n# =================== T2 (Mahmudi's)")
	test_set = dict()
	with open("Kurdish-Spelling-TestSet-NeteweNet.tsv", "r") as f:  # Mahmudi's
		for i in f.read().split("\n")[2:]:
			test_set[i.split("\t")[0]] = i.split("\t")[1]
	
	print("= Evaluating baseline")
	spell_checker_output = run(test_set, "T2_baseline")
	evaluate(spell_checker_output, calculate_PR=True)

	print("= Evaluating Hunspell")
	spell_checker_output = run(test_set, "T2_hunspell", is_baseline=False)
	evaluate(spell_checker_output, calculate_PR=True)
	print()

	print("\n# =================== T2\\space (Mahmudi's without space)")
	test_set = dict()
	with open("Kurdish-Spelling-TestSet-NeteweNet.tsv", "r") as f:  # Mahmudi's
		for i in f.read().split("\n")[2:]:
			if i.split("\t")[4] == "0":
				test_set[i.split("\t")[0]] = i.split("\t")[1]

	print("= Evaluating baseline")
	spell_checker_output = run(test_set, "T2_nospace_baseline")
	evaluate(spell_checker_output, calculate_PR=True)

	print("= Evaluating Hunspell")
	spell_checker_output = run(test_set, "T2_nospace_hunspell", is_baseline=False)
	evaluate(spell_checker_output, calculate_PR=True)
		

