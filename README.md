# Stanford Parser使用

整理stanford parser的部分使用方法，Stanford Parser版本3.9.1。

**官方使用指南**: `./StanfordDependenciesManual(bookmark).pdf`

**最新版本下载**: [download](https://nlp.stanford.edu/software/lex-parser.shtml#Download)

## 1. 使用预训练的模型

**注**: 以下提及的脚本，若没有特别指明路径，则都在官方下载的压缩包里；否则，相关脚本存放在`./scripts`目录下。

### 1.1 官方提供的模型

Stanford Parser提供了预训练的模型供使用，表1,2分别列出了中英文模型。其中，`Mixed [Chinese|English]`分别是在中文/英文的混合标注语料上训练的模型，`wsj`是在华尔街日报语料上训练的模型，`xinhua`是在中文新华日报语料上训练的模型。

关于不同模型的介绍: [PCFG parser](https://nlp.stanford.edu/~manning/papers/unlexicalized-parsing.pdf), [Factored parser](https://nlp.stanford.edu/~manning/papers/lex-parser.pdf)

**表 1.** 中文模型

| Corpus | PCFG | Factored | FactoredSegmenting |
| ------------- | ------------- | ------------- | -------------|
| mixed Chinese | chinesePCFG.ser.gz| chineseFactored.ser.gz | |
| xinhua | xinhuaPCFG.ser.gz | xinhuaFactored.ser.gz | xinhuaFactoredSegmenting.ser.gz |

**表 2.** 英文模型

| Corpus | PCFG | Factored | RNN |
| ------------- | ------------- | ------------- | ------------- |
| mixed English | englishPCFG.ser.gz, englishPCFG.ser.gz | englishFactored.ser.gz | englishRNN.ser.gz |
| wsj | wsjPCFG.ser.gz | wsjFactored.ser.gz | wsjRNN.ser.gz |

### 1.2 使用预训练模型的几种方式

**注**: 若对符号化之后的句子进行解析，则在使用Stanford Parser进行句法解析之前，需要对句子中的括号进行处理，处理方式参考: `./scripts/preprocessing.py`。

#### 1.2.1 图形界面

 - Linux下运行`lexparser-gui.sh`
 - Windows下运行`lexparser-gui.bat`

#### 1.2.2 命令行

 - 脚本: `lexparser.sh`或`lexparser.bat`，使用英文模型；

 - 脚本: `lexparser_lang.sh`或`lexparser_lang.bat`，可指定语言；

 - 相关参数参考官方指南。

#### 1.2.3 Java

参考`ParserDemo.java`、`ParserDemo2.java`和`DependencyParserDemo.java`。

#### 1.2.4 Python

 - **NLTK接口**: 参考脚本`./scripts/python/nltk_stanford_parser_demo.py`。

 - **python调用jar包**: 参考脚本`./scripts/python/stanford_parser_demo.py`。

## 2. 重新训练模型

### 2.1 命令行

脚本: `lexparser-lang-train-test.sh`，若有treebank标注语料，则可使用该脚本重新训练句法分析模型。

### 2.2 Python

参考：`./scripts/python/stanford_parser_trainer.py`。

若要使用新训练的模型，则参考1.2.1-1.2.4。

## 3. treebanks语料整理

见`treebanks/README.md`。

## 4. 性能评估

### 4.1 CONLL-U Format

**CONLL-U Format介绍**: http://universaldependencies.org/docs/format.html

**评估脚本下载地址**: http://universaldependencies.org/conll17/evaluation.html
