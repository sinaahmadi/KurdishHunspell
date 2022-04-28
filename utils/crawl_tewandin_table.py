#!/usr/bin/python3

"""
This script extracts the following information from the conjugation pages (Tewandin) of WikiFerheng--the Kurdish Wiktionary (https://ku.wiktionary.org/wiki/Kategor%C3%AE:Tewandin:l%C3%AAker%C3%AAn_xwer%C3%BB_(kurd%C3%AE)):
	- lemma
	- transitivity
	- past and present stems

Sina Ahmadi (2022)
"""

import requests
from bs4 import BeautifulSoup

with open("tewandin_links.txt", "r") as f:
	links = f.read().split("\n")

for link in links:
	is_transitive = True
	page = requests.get(link)
	page.encoding = page.apparent_encoding
	soup = BeautifulSoup(page.text, 'html.parser')

	lemma = soup.title.string.replace("Tewandin:", "").replace(" - Wîkîferheng", "")
	if "negerguhêz" in page.text:
		is_transitive = False
		print(lemma, "\tXN\tverb\tinfinitive_intransitive_active\t\t"+lemma)
	else:
		print(lemma, "\tXN\tverb\tinfinitive_transitive_active\t\t"+lemma)	
	
	tables = soup.findChildren('table')
	rows = tables[0].findChildren(['th', 'tr'])
	flag = True
	for row in rows:
		cells = row.findChildren('td')
		for cell in cells:
			value = cell.string
			if value and "–" in value:
				if flag: # present stem
					if is_transitive:
						print(value.replace("–", "").replace("\n", ""), "\tV\tverb\tpresent_stem_transitive_active\t\t"+lemma)
					else:
						print(value.replace("–", "").replace("\n", ""), "\tV\tverb\tpresent_stem_intransitive_active\t\t"+lemma)
					flag = False
				else: # past stem
					if is_transitive:
						print(value.replace("–", "").replace("\n", ""), "\tT\tverb\tpast_stem_transitive_active\t\t"+lemma)
					else:
						print(value.replace("–", "").replace("\n", ""), "\tI\tverb\tpast_stem_intransitive_active\t\t"+lemma)

	print()