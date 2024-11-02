# Data Generation
This repository contains minimal pair datasets designed to assess language models' preference for overregularization. The data is automatically generated using scripts based on [BLiMP’s data generation scripts](https://github.com/alexwarstadt/data_generation/tree/blimp) and is used in the following paper:

- Akari Haga, Saku Sugawara, Akiyo Fukatsu, Miyu Oba, Hiroki Ouchi, Taro Watanabe, Yohei Oseki. Modeling Overregularization in Children with Small Language Models. In Findings of the Association for Computational Linguistics: ACL 2024, Aug 2024.

# Usage
To run a data generation script, use the following command:
```
$ pip install requirements.txt
$ python -m generation_projects.overregularized_past_verbs
```

# Vocabulary
The vocabulary file is named vocabulary.csv.
We have expanded the vocabulary used in BLiMP to include the overregularized forms of verbs. Additionally, We added `is_in_cds` tag to the vocabulary file, indicating whether a word is found in the CHILDES English dataset. Only words present in CHILDES are used for data generation.
