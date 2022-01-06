# Hunspell for Kurdish
## A morphological analyzer and spell checker for Kurdish in Hunspell
---
### Latest update on January 5th, 2022
- [x] Morphosyntactic tags, i.e. `po`
- [x] Inflectional tags, i.e. `is`
- [x] ✨ Stems, i.e. `st` (covering all part-of-speech tags from version 0.1.3 / verbal stems added in Version 0.1.2) 
- [x] ✨ Lemmas, i.e. `lem` 
- [x] Creating the plugin for Microsoft Office and LibreOffice (check out [extensions](extensions) folder!) 🎉🥳 
- [ ] Derivational tags, i.e. `ds`

---

[Hunspell](http://hunspell.github.io/) is a spell checker and morphological analyzer originally designed for languages with rich morphology and complex word compounding. An open-source software, it is widely used by various web browsers and text editors. This repository contains an implementation of the Kurdish morphological rules and annotated lexicon for the task of spell-checking and morphological analysis. To use these functionalities, see  [Kurdish Language Processing Toolkit (KLPT)](https://github.com/sinaahmadi/klpt). Moreover, this spell-checker is currently being added as an extension to LibreOffice and OpenOffice and therefore, can be used within many text editors and browsers as well.

Please note that the current version only contains Sorani Kurdish data. Kurmanji data will be also provided in a near future. **It should also be noted that the current project is the outcome of months of volunteer research and implementation. Please respect the terms of the license below.**


### Morphological rules

Sorani Kurdish morphology is notoriously complex. This is not only due to the number of affixes and clitics, but the way they appear and interact within a word-form. The following is an example on such a complexity for a single-word verb where the base *girt* of the verb *girtin* 'to take, to get' appears with clitics, suffixes and a verbal particle. The placement of the endoclitic *=îş* (in green boxes) and agent marker *=im* (in blue boxes) varies with respect to the base and each other in the verb form.

![alt text](example.png "Zazaki and Gorani languages within the Indo-European language family")

In order to extract morphological rules, the morphology of Sorani Kurdish is studied in a formal way in the paper entitled [ computational formalization of the Sorani Kurdish morphology](). This formalization allows various morpho-syntactic features of Sorani to be represented as rules which are presented in the [ckb-Arab.aff](ckb/ckb-Arab.aff) file. In version 0.1.0, inflectional and derivational rules regarding verbs, adjectives, adverbs and nouns are implemented. In version 0.1.2, the stem of verbs were provided. This is useful for the stemming task where given a word form, its stem can be retrieved, as in 'ڕن' → 'ڕنیبووم'. Following this, in version 0.1.3 the stem of other part-of-speech tags and the lemma form of the verbs, e.g. 'نواندن' → 'دەنوێنم', were added. Therefore, both the stemming and the lemmatization tasks are now fully operational. Next versions will focus on further enrichments of the current categories and also rectifying possible errors.


### Lexicon annotation

As a rule-based method, Hunspell needs an annotated lexicon to which the morphological rules are applied. To this end, we use the lexicographic material provided by the [FreeDict project](https://freedict.org/) and [Wîkîferheng, the Kurdish Wiktionary](https://ku.wiktionary.org/). In addition, [Wikidata](https://www.wikidata.org) is consulted to extract proper names. The transliteration of the Latin-based script of Kurdish into the Arabic-based one is carried out using [Wergor](https://github.com/sinaahmadi/wergor). Each lemma in the lexicon is manually tagged with part-of-speech, its formation type (derivational/inflectional) and further morphological properties. In addition, composing parts of compound forms are specified using a hyphen. This way, the annotated lexicon is also used within the [Kurdish Tokenization project](https://github.com/sinaahmadi/KurdishTokenization).

According to the morphological rules, lemmata in our lexicons are tagged using the following flags. If the flags don't make much sense to you, the part of speech tags, i.e. `po` flag, will hopefully do as they are provided according to the [Universal Dependency tags](https://universaldependencies.org/u/pos/index.html). The annotated lexicon is available at [ckb-Arab.dic](ckb/ckb-Arab.dic).

- `N`: Noun
- `V`: present stem of verbs
- `I`: past stem of intransitive verbs
- `T`: past stem of transitive verbs
- `A`: adjectives
- `R`: adverbs
- `E`: numerals
- `C`: conjunction
- `D`: interjection
- `B`: pronouns
- `E`: numerals
- `F`: adpositions
- `G`: particle
- `X`: infinitive
- `Z`: proper names
- `W`: irregular cases like *were* 'come.imp.2s'

The following is an example on how a few lemmata are tagged in our lexicon:

	فەوتێنرا/I po:verb is:past_stem_intransitive_passive
	فەوتێنران/XN po:verb is:infinitive_intransitive_passive
	فەوتێنرێ/V po:verb is:present_stem_intransitive_passive
	فەودە/ZN po:propn
	فەڕ/N po:noun
	فەڕاشە/N po:noun


### Cite this paper

There are two publications regarding this project which should be cited as follows ([paper 1](https://arxiv.org/ftp/arxiv/papers/2109/2109.06374.pdf), [paper 2](https://arxiv.org/ftp/arxiv/papers/2109/2109.03942.pdf)):

	@article{ahmadi2020Hunspell,
		title={{Hunspell for Sorani Kurdish Spell Checking and Morphological Analysis}},
		author={Ahmadi, Sina},
		journal={arXiv preprint arXiv:2109.06374},
		year={2021},
	}
	
	@article{ahmadi2020formalization,
		title={{A Formal Description of Sorani Kurdish Morphology}},
		author={Ahmadi, Sina},
		journal={arXiv preprint arXiv:2109.03942},
		year={2021}
	}

### Contribute
Are you interested in this project? Please follow the instructions of the [Kurdish Language Processing Toolkit (KLPT)](https://github.com/sinaahmadi/klpt) to get involved. Open-source is fun! 😊 

### Sponsorship
The current project is the fruit of hundreds of hours of research and development. If this project matters to you, please support me through the Sponsor button on the top of the page. Thanks!

My warmest thanks to [datavaluepeople](www.datavaluepeople.com) and [Build Up](https://howtobuildup.org) for their sponsorship that gave me the motivation to complete adding stems. Version 0.1.3 was made possible thanks to them! ❤️

### License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">This repository</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/sinaahmadi/klpt" property="cc:attributionName" rel="cc:attributionURL">Sina Ahmadi</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a> which means:

- **You are free to share**, copy and redistribute the material in any medium or format and also adapt, remix, transform, and build upon the material
for any purpose, **even commercially**. 
- **You must give appropriate credit**, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- If you remix, transform, or build upon the material, **you must distribute your contributions under the same license as the original**. 

