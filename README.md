# Hunspell for Kurdish
## A morphological analyzer and spell checker for Kurdish in Hunspell (Sorani and Kurmanji)
---

### Latest update on June 19th, 2025: Version 0.1.1
- [x] Both Sorani and Kurmanji lexicons are updated. Now, **Sorani has 33,856 tagged entries** (24,888 in the previous version) and **Kurmanji has 43,945 tagged entries** (21,245 in the previous version).
- [x] The rules are revised and completed for Sorani. Many verbal forms where previously missing. The transitivity of some verbs is also corrected in this version.
- [x] Additional rules to process digits and punctuation marks are added.

### Latest update on April 28th, 2022: Version, 0.1.0
- [x] Morphosyntactic tags, i.e. `po`
- [x] Inflectional tags, i.e. `is`
- [x] Stems, i.e. `st` (covering all part-of-speech tags from version 0.1.3 / verbal stems added in Version 0.1.2) 
- [x] Lemmas, i.e. `lem` 
- [x] Creating the plugin for Microsoft Office and LibreOffice (check out [extensions](extensions) folder!)  
- [x] ✨ Hunspell is now available for Kurmanji Kurdish as well! 🎉🥳
- [ ] Derivational tags, i.e. `ds`

---

[Hunspell](http://hunspell.github.io/) is a spell checker and morphological analyzer originally designed for languages with rich morphology and complex word compounding. An open-source software, it is widely used by various web browsers and text editors. This repository contains an implementation of the Kurdish morphological rules and annotated lexicon for the task of spell-checking and morphological analysis. To use these functionalities, see [Kurdish Language Processing Toolkit (KLPT)](https://github.com/sinaahmadi/klpt). Moreover, this spell-checker is currently being added as an extension to LibreOffice and OpenOffice and therefore, can be used within many text editors and browsers as well.

The project was initially created for Sorani Kurdish in early 2020. In April 2022, I also added a similar implementation for Kurmanji. It should be noted that the current project is the outcome of months of volunteer research and implementation. **Please respect the terms of the license below and don't forget to recognize hours of manual dictionary tagging and extraction of morphological rules!** See below to find out how you can be a sponsor of this project.

### Morphological rules

Kurdish morphology, particularly that of the Sorani dialect, is notoriously complex. This is not only due to the number of affixes and clitics, but the way they appear and interact within a word-form. The following is an example in Sorani on such a complexity for a single-word verb where the base *girt* of the verb *girtin* 'to take, to get' appears with clitics, suffixes and a verbal particle. The placement of the endoclitic *=îş* (in green boxes) and agent marker *=im* (in blue boxes) varies with respect to the base and each other in the verb form.

![alt text](example.png "Zazaki and Gorani languages within the Indo-European language family")

In order to extract morphological rules, the morphology of Kurdish is studied in a formal way in the paper entitled [A Formal Description of Sorani Kurdish Morphology](https://arxiv.org/ftp/arxiv/papers/2109/2109.03942.pdf). This formalization allows various morpho-syntactic features of Kurdish to be represented as rules which are presented in the [ckb-Arab.aff](ckb/ckb-Arab.aff) and [kmr-Latn.aff](kmr/kmr-Latn.aff) files. 

 - Regarding the Sorani implementation, in version 0.1.0, inflectional and derivational rules regarding verbs, adjectives, adverbs and nouns are implemented. In version 0.1.2, the stem of verbs were provided. This is useful for the stemming task where given a word form, its stem can be retrieved, as in 'ڕن' → 'ڕنیبووم'. Following this, in version 0.1.3 the stem of other part-of-speech tags and the lemma form of the verbs, e.g. 'نواندن' → 'دەنوێنم', were added. Therefore, both the stemming and the lemmatization tasks are now fully operational. In addition, more lexical entries are added, particularly proper names. 
- Regarding the Kurmanji implementation, in version 0.1.0 the structure of the project is created where morphological rules are defined and a dictionary containing over 16000 entries is manually tagged. Kurmanji morphology in comparison to that of Sorani is simpler. This being said, to keep the usage of flags consistent across the project, the same are used in both dialects; for instance, the `I` (intransitive past stem) and `T` (transitive past stem) flags are treated equally even though ergativity in Kurmanji is dealt with differently from Sorani. Stems and lemmas are also available for Kurmanji.

Next versions will focus on further enrichments of the current categories and also rectifying possible errors (please report them).

### Lexicon annotation

As a rule-based method, Hunspell needs an annotated lexicon to which the morphological rules are applied. To this end, we use the lexicographic material provided by the [FreeDict project](https://freedict.org/) and [Wîkîferheng, the Kurdish Wiktionary](https://ku.wiktionary.org/). In addition, [Wikidata](https://www.wikidata.org) is consulted to extract proper names. The transliteration of the Latin-based script of Kurdish into the Arabic-based one is carried out using [Wergor](https://github.com/sinaahmadi/wergor). Each lemma in the lexicon is manually tagged with part-of-speech, its formation type (derivational/inflectional) and further morphological properties. In addition, composing parts of compound forms are specified using a hyphen. This way, the annotated lexicon is also used within the [Kurdish Tokenization project](https://github.com/sinaahmadi/KurdishTokenization).

According to the morphological rules, lemmata in our lexicons are tagged using the following flags. If the flags don't make much sense to you, the part of speech tags, i.e. `po` flag, will hopefully do as they are provided according to the [Universal Dependency tags](https://universaldependencies.org/u/pos/index.html). The annotated lexicons are available at [ckb-Arab.dic](ckb/ckb-Arab.dic) and [kmr-Latn.dic](kmr/kmr-Latn.dic).

- `N`: Noun
- `M`: Masculine noun
- `F`: Feminine noun
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
- `P`: adpositions (currently F in Sorani data)
- `G`: particle
- `X`: infinitive
- `Z`: proper names
- `W`: irregular cases like *were* 'come.imp.2s'
- `H`: punctuation marks
- `J`: numerals as digits (0-9 and ٠-٩)

The following is an example on how a few lemmata are tagged in the Sorani lexicon:

	فەوتێنرا/I po:verb is:past_stem_intransitive_passive
	فەوتێنران/XN po:verb is:infinitive_intransitive_passive
	فەوتێنرێ/V po:verb is:present_stem_intransitive_passive
	فەودە/ZN po:propn
	فەڕ/N po:noun
	فەڕاشە/N po:noun

and in the Kurmanji lexicon:

	reng/M po:noun_masc
	rengand/T po:verb is:past_stem_transitive_active st:reng lem:rengandin
	rengandin/XN po:verb is:infinitive_transitive_active st:reng lem:rengandin
	rengarengkirî/AN po:adj
	rengdarbûyî/AN po:adj

### Test
The best way to use this project for Kurdish morphological analysis and generation is [KLPT](https://github.com/sinaahmadi/klpt). If you still want to specifically test it, the process is quite simple:

- Install Hunspell (see instructions at [https://github.com/hunspell/hunspell](https://github.com/hunspell/hunspell))
- For an interactive analysis, you can then use this command in the directory where the `.aff` and `.dic` files are located:

```
analyze ckb-Arab.aff ckb-Arab.dic /dev/stdin
> بڕیار
analyze(بڕیار) = po:noun st:بڕ بڕیار:ts 
stem(بڕیار) = بڕ

> کرایە
analyze(کرایە) = po:verb is:past_stem_intransitive_passive st:ک lem:کران کرا:ts یە
analyze(کرایە) = po:verb is:past_stem_intransitive_active st:ک lem:کران کرا:ts یە
stem(کرایە) = ک

> بشهێڵم
analyze(بشهێڵم) = M:lf هێڵ:ts po:verb is:present_stem_transitive_active st:هێڵ lem:هێشتن_هێڵانM:lf 
stem(بشهێڵم) = هێڵ                                                                                        
```


### Cite these papers

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

My warmest thanks to [datavaluepeople](www.datavaluepeople.com) and [Build Up](https://howtobuildup.org) for their sponsorship that gave me the motivation to complete adding stems. The updates in 2022 were made possible thanks to them! ❤️

### License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">This repository</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/sinaahmadi/klpt" property="cc:attributionName" rel="cc:attributionURL">Sina Ahmadi</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a> which means:

- **You are free to share**, copy and redistribute the material in any medium or format and also adapt, remix, transform, and build upon the material
for any purpose, **even commercially**. 
- **You must give appropriate credit**, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- If you remix, transform, or build upon the material, **you must distribute your contributions under the same license as the original**. 

