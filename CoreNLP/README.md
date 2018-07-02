# Stanford Core NLP

[Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/)集合了分词、POS、NER、Coreference、Parser等工具于一身，这里整理了其处理中文语料的方法。

## 1. 下载CoreNLP

CoreNLP下载地址: [https://nlp.stanford.edu/software/corenlp-backup-download.html](https://nlp.stanford.edu/software/corenlp-backup-download.html)

**Step 1**: 下载`stanford-corenlp-full-xxxx-xx-xx.zip`，其中`xxxx-xx-xx`表示工具发布的日期，解压后的目录记为`ROOT_CORENLP`；

**Step 2**: 下载中文模型包，格式为`stanford-chinese-corenlp-xxxx-xx-xx-models.jar`，将该模型放置在`ROOT_CORENLP`中。

## 2. CoreNLP使用

python示例代码：

```python
import subprocess

command = 'java -mx{0} -Djava.ext.dirs={1} edu.stanford.nlp.pipeline.StanfordCoreNLP ' + \
    '-language Chinese -encoding utf-8 -props StanfordCoreNLP-chinese.properties ' + \
    '-annotators tokenize,ssplit,pos,lemma,ner,depparse -ssplit.eolonly ' \
    '-file {2} -outputFormat conllu -outputDirectory {3}'

MAX_MEN = '2g'
ROOT_CORENLP = 'your_corenlp_path'
PATH_SENT = 'your_file_path'
ROOT_CONLLU = 'your_result_root_path'

command = command.format(MAX_MEM, ROOT_CORENLP, PATH_SENT, ROOT_CONLLU)

return_code = subprocess.call(command, shell=True)
```

其中：

  - `MAX_MEM`: jvm最大使用内存；
  - `ROOT_CORENLP`: CoreNLP解压后的路径；
  - `PATH_SENT`: 待处理的文件，每个句子一行；
  - `ROOT_CONLLU`: 处理后的文件根目录，处理后文件名路径为`ROOT_CONLLU/PATH_SENT.conllu`。
