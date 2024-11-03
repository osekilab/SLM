# Modeling Overregularization in Children with Small Language Models

This repository contains minimal pair datasets designed to assess language models' preference for overregularization. The data is automatically generated using scripts based on [BLiMP’s data generation scripts](https://github.com/alexwarstadt/data_generation/tree/blimp) ([Warstadt et al., 2020](https://aclanthology.org/2020.tacl-1.25/)) and is used in the following paper:

- Akari Haga, Saku Sugawara, Akiyo Fukatsu, Miyu Oba, Hiroki Ouchi, Taro Watanabe, Yohei Oseki. [Modeling Overregularization in Children with Small Language Models](https://aclanthology.org/2024.findings-acl.865/). In Findings of the Association for Computational Linguistics: ACL 2024, Aug 2024.

# Usage
You can download our minimal pair dataset from [here](https://github.com/osekilab/SLM/blob/main/outputs/overregularized_past_verbs.jsonl).
Alternatively, you can regenerate the minimal pair data using the following command:
```
$ pip install requirements.txt
$ python -m generation_projects.overregularized_past_verbs
```
After execution, the generated files will be saved in the outputs/ directory.

# Vocabulary
The vocabulary file is named vocabulary.csv.
We have expanded the vocabulary used in BLiMP to include the overregularized forms of verbs. Additionally, We added `is_in_cds` tag to the vocabulary file, indicating whether a word is found in the CHILDES English dataset. Only words present in CHILDES are used for data generation.

# Citation
If you use this project in your work, please cite our paper:
```
@inproceedings{haga2024modeling,
  title={Modeling Overregularization in Children with Small Language Models},
  author={Haga, Akari and Sugawara, Saku and Fukatsu, Akiyo and Oba, Miyu and Ouchi, Hiroki and Watanabe, Taro and Oseki, Yohei},
  booktitle={Findings of the Association for Computational Linguistics ACL 2024},
  pages={14532--14550},
  year={2024}
}
```
