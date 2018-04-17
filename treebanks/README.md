# Treebank Corpus


# 1. GENIA treeebank

下载地址: [download](http://www.geniaproject.org/genia-corpus/treebank)

## 1.1 目录

    .
    ├──GENIA_treebank_v1_xml/  # GENIA treebank语料原始xml文件
    │  └──xxx.xml              # treebank xml格式文件
    ├──GENIA_tree/             # 处理后的treebank文件
    │  ├──esc_char.map         # 特殊字符映射表
    │  └──GENIA_SP.ptb         # ptb格式文件
    ├──xml2ptb.py              # xml转ptb格式脚本
    └──README.md               # README.md

## 1.2 xml转ptb

在上述GENIA treebank下载到GENIA_treebank_v1_xml目录下，并运行以下脚本。

    $ python3 xml2ptb.py

运行完成后(~6s)，在`./GENIA_tree/`下生成`GENIA_SP.ptb`和`esc_char.map`两个文件，其中，`GENIA_SP.ptb`即为`penn treebank`格式的treebank标注语料。

## 1.3 语料统计

GENIA treebanks共标注了18541个句子，转为ptb格式时有111条产生错误(括号不能配对)，剩余18430条有效数据。


# 2. 其他treebanks

## 2.1 英文

### 2.1.1 Penn English Treebanks

**not free available**: http://catalog.ldc.upenn.edu/ldc99t42

NLTK中包含Penn Treebanks 10%的样本，通过以下接口访问:

    $ from nltk.corpus import treebank
    $ treebank.parsed_sents()
    $ len(treebank.parsed_sents())  # 3914

### 2.1.2 American National Corpus

**MASC-CONLL**: http://www.anc.org/data/masc/downloads/data-download/

### 2.1.3 QuestionBank

https://nlp.stanford.edu/data/QuestionBank-Stanford.shtml

## 2.2 中文

### 2.2.1 Penn Chinese Treebanks

**not free available**: https://verbs.colorado.edu/chinese/

### 2.2.2 Sinica Treebanks

Sinica提供的繁体中文语料库，共5346个parsed sentences，可通过NLTK接口访问。

    $ from nltk.corpus import sinica_treebank
    $ sinica_treebank.parsed_sents()

## 2.3 More...

https://en.wikipedia.org/wiki/Treebank#Syntactic_treebanks
