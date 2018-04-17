# Stanford Parser使用

整理stanford parser的部分使用方法，Stanford Parser版本3.9.1。

**官方使用指南**: `./StanfordDependenciesManual-bookmark.pdf`

**最新版本下载**: [download](https://nlp.stanford.edu/software/lex-parser.shtml#Download)

**官方整理的FAQ**: [FAQ](https://nlp.stanford.edu/software/parser-faq.html)

## 1. 使用预训练的模型

以下提及的脚本，若没有特别指明路径，则都在官方下载的压缩包里；否则，相关脚本存放在`./scripts`目录下。

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

官方提供了多种调用方式，并提供了多种编程语言的接口，这里仅整理出其中4种，分别是: `图形界面`、`命令行`、`Java`和`Python`。

**注**: 若对符号化之后的句子进行解析，则在使用Stanford Parser进行句法解析之前，需要对句子中的括号进行处理，处理方式参考: [./scripts/python/preprocessing.py](./scripts/python/preprocessing.py)。

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

 - **NLTK接口**: 参考脚本[./scripts/python/nltk_stanford_parser_demo.py](./scripts/python/nltk_stanford_parser_demo.py)。

 - **python调用jar包**: 参考脚本[./scripts/python/stanford_parser_demo.py](./scripts/python/stanford_parser_demo.py)。

## 2. 输出格式

详细信息参考官方手册`In practice`部分。

### 2.1 penn or dependency format?

**edu.stanford.nlp.parser.lexparser.LexicalizedParser**

若要获取不同格式的输出，则需修改`-outputFormat`：

 - `penn`格式: `-outputFormat "penn"`
 - `dependency`格式: `-outputFormat "typedDependencies"`
 - 同时获取两种格式: `-outputFormat "penn,typedDependencies"`

示例命令行:

    # 输出格式为penn和dependency
    java -mx200m edu.stanford.nlp.parser.lexparser.LexicalizedParser
    -retainTmpSubcategories -originalDependencies -outputFormat
    "penn,typedDependencies" -outputFormatOptions "basicDependencies"
    englishPCFG.ser.gz file.txt

### 2.2 不同格式的dependencies

Stanford Parser的dependencies默认采用`collapsed dependencies`，若需要其他格式的dependencies，则需修改`-outputFormatOptions`选项，可选参数有：

 - `basicDependencies`: Basic dependencies.
 - `collapsedDependencies`: Collapsed dependencies (not necessarily a tree structure)
 - `CCPropagatedDependencies`: Collapsed dependencies with propagation of conjunct dependencies (not necessarily a tree structure). **This representation is the default, if no option is specified.**
 - `treeDependencies`: Collapsed dependencies that preserve a tree structure.
 - `nonCollapsedDependencies`: Non-collapsed dependencies: basic dependencies as well as the extra ones which do not preserve a tree structure.
 - `nonCollapsedDependenciesSeparated`: Non-collapsed dependencies where the basic dependencies are separated from the extra ones (by “======”).

### 2.3 penn格式转其他格式

**edu.stanford.nlp.trees.EnglishGrammaticalStructure**

如果已经有了`penn treebank`格式的文件，需要将其转换为`dependency`格式，则可以使用此类。

可选参数:

 - `-basic`: basic dependencies
 - `-collapsed`: collapsed dependencies (not necessarily a tree structure)
 - `-CCprocessed`: collapsed dependencies with propagation of conjunct dependencies (not necessarily a tree structure)
 - `-collapsedTree`: collapsed dependencies that preserve a tree structure
 - `-nonCollapsed`: non-collapsed dependencies: basic dependencies as well as the extra ones which do not preserve a tree structure
 - `-conllx`: dependencies printed out in CoNLL X (CoNLL 2006) format
 - `-originalDependencies`: output the original Stanford Dependencies instead of the new Universal Dependencies.

示例命令行:

    # penn格式转dependency格式，其中`-keepPunct`参数是保留标点符号
    java edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile
    file.tree -collapsedTree -CCprocessed -keepPunct

## 3. 重新训练模型

### 3.1 命令行

脚本: `lexparser-lang-train-test.sh`，若有treebank标注语料，则可使用该脚本重新训练句法分析模型。

### 3.2 Python

#### 3.2.1 PCFG and Factored

参考：[./scripts/python/stanford_parser_trainer.py](./scripts/python/stanford_parser_trainer.py)。

若要使用新训练的模型，则参考1.2.1-1.2.4。

或参考官方FAQ: [Can I train the parser?](https://nlp.stanford.edu/software/parser-faq.html#d)

#### 3.2.2 RNN

官方FAQ: [How do I train the RNN parser?](https://nlp.stanford.edu/software/parser-faq.html#rnn)

## 4. treebank语料整理

见[./treebanks/README.md](./treebanks/README.md)。

## 5. 性能评估

### 5.1 CONLL-U Format

**CONLL-U Format介绍**: http://universaldependencies.org/docs/format.html

**评估脚本下载地址**: http://universaldependencies.org/conll17/evaluation.html
