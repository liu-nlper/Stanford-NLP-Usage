#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
stanford parser
    
class MyStanfordParser
    
    Parameters:
        path_stanford: stanford-parser.jar路径的父目录
        parser_jar: 'edu.stanford.nlp.parser.lexparser.LexicalizedParser'
        max_mem: 最大内存，default '4g'
    
    Methods:

        predict: 对文件进行句法分析，预测结果为ptb格式
        
        predict_dep: 对文件进行句法分析，预测结果为dependency格式
        
        ptb2conll: 将ptb转为conll格式
"""
import subprocess


def read_lines(path):
    lines = []
    file_r = open(path, 'r', encoding='utf-8')
    for line in file_r.readlines():
        line = line.strip()
        if line:
            lines.append(line)
    return lines


class MyStanfordParser(object):

    def __init__(self, path_stanford, parser_jar='edu.stanford.nlp.parser.lexparser.LexicalizedParser',
                 max_mem='4g'):
        """
        Args:
            path_stanford: stanford-parser.jar路径的父目录
            parser_jar: 'edu.stanford.nlp.parser.lexparser.LexicalizedParser'
            max_mem: 最大内存，default '4g'
        """
        self._path_stanford = path_stanford
        self._parser_jar = parser_jar
        self._max_mem = max_mem

    def predict(self, path_model, path_data, path_result_ptb=None, path_result_conll=None):
        """
        parse sentences, penn format

        Args:
            path_model: 模型文件路径
            path_data: 待标记文件路径
            path_result_ptb: 结果存放路径
            path_result_conll: 转为conll的路径
            
        Notes:
            1. '-tokenized'参数，若使用该参数，则不再进行符号化，但是要注意括号的处理;
            2. '-sentences newline'参数，parser one sentence per line
        """
        print('predict...', end='')
        command = 'java -mx%s -Djava.ext.dirs=%s %s -tokenized -retainTmpSubcategories ' + \
            '-originalDependencies -outputFormat "penn" -outputFormatOptions ' + \
            '"basicDependencies" -sentences newline %s %s'
        command %= (self._max_mem, self._path_stanford, self._parser_jar,
                    path_model, path_data)
        if path_result_ptb:
            command += ' > %s' % path_result_ptb
        return_code = subprocess.call(command, shell=True)
        print('done!')

        if path_result_conll:  # 转为conll format
            print('transform to conll format...', end='')
            self.ptb2conll(path_result_ptb, path_result_conll)
            print('done!')
        return return_code

    def predict_dep(self, path_model, path_data, path_result_ptb=None, path_result_conll=None):
        """
        parse sentences, get the dependencies

        Args:
            path_model: 模型文件路径
            path_data: 待标记文件路径
            path_result_ptb: 结果存放路径
            path_result_conll: 转为conll的路径
        
        Notes:
            1. '-tokenized'参数，若使用该参数，则不再进行符号化，但是要注意括号的处理;
            2. '-sentences newline'参数，parser one sentence per line
        """
        print('predict...', end='')
        command = 'java -mx%s -Djava.ext.dirs=%s %s -tokenized -retainTmpSubcategories ' + \
            '-originalDependencies -outputFormat "typedDependencies" -outputFormatOptions ' + \
            '"basicDependencies" -sentences newline %s %s'
        command %= (self._max_mem, self._path_stanford, self._parser_jar,
                    path_model, path_data)
        if path_result_ptb:
            command += ' > %s' % path_result_ptb
        return_code = subprocess.call(command, shell=True)
        print('done!')

        if path_result_conll:  # 转为conll format
            print('transform to conll format...', end='')
            self.ptb2conll(path_result_ptb, path_result_conll)
            print('done!')
        return return_code

    def ptb2conll(self, path_ptb, path_conll):
        """
        ptb转为conll format
        Args:
            path_result_ptb: 结果存放路径
            path_result_conll: 转为conll的路径
        """
        egs = 'edu.stanford.nlp.trees.EnglishGrammaticalStructure'
        command = 'java -mx%s -Djava.ext.dirs=%s %s -treeFile %s -conllx ' + \
            '-basic -retainNPTmpSubcategories -makeCopulaHead -keepPunct > %s'
        command %= (self._max_mem, self._path_stanford, egs, path_ptb, path_conll)
        return subprocess.call(command, shell=True)


def replace_pair(token, replace_map):
    """
    替换token中的括号
    """
    token = list(token)
    for i in range(len(token)):
        c = token[i]
        if c in replace_map:
            token[i] = replace_map[c]
    return ''.join(token)


def preprocessing_sentence(path_ori, path_result):
    """
    处理原句子中的特殊括号
    Args:
        path_ori: str, 原始文件路径
        path_result: str, 处理后文件路径
    """
    replace_map = {
        '(': '-LRB-', ')': '-RRB-',
        '[': '-LRB-', ']': '-RRB-',
        '{': '-LRB-', '}': '-RRB-'}
    lines = read_lines(path_ori)  # 可改为逐行读取...
    file_w = open(path_result, 'w', encoding='utf-8')
    for line in lines:
        new_line = replace_pair(line, replace_map)
        file_w.write('%s\n' % new_line)
    file_w.close()


def parser_ptb_demo():
    """
    解析源语言，ptb格式

    注： 若使用'-tokenized'参数，即输入的是符号化之后的句子，则必须处理句子中的括号
    """
    path_model = 'path_to_your_model'  # 官方的模型或自行训练的模型路径

    # parse txt (change to your own paths)
    path_stanford = './stanford-parser-full-2018-02-27'
    parser_jar = 'edu.stanford.nlp.parser.lexparser.LexicalizedParser'
    stanford_parser = MyStanfordParser(path_stanford, parser_jar)

    path_txt = 'your.txt'  # 待解析文件路径
    path_result_ptb = 'your.ptb'  # ptb格式路径
    path_result_conll = 'your.conll'  # conll格式路径(可为None)
    stanford_parser.predict(path_model, path_txt, path_result_ptb, path_result_conll)


def parser_dep_demo():
    """
    解析源语言，dependency格式

    注： 若使用'-tokenized'参数，即输入的是符号化之后的句子，则必须处理句子中的括号
    """
    path_model = 'path_to_your_model'  # 官方的模型或自行训练的模型路径

    # parse txt (change to your own paths)
    path_stanford = './stanford-parser-full-2018-02-27'
    parser_jar = 'edu.stanford.nlp.parser.lexparser.LexicalizedParser'
    stanford_parser = MyStanfordParser(path_stanford, parser_jar)

    path_txt = 'your.txt'  # 待解析文件路径
    path_result_dep = 'your.ptb'  # ptb格式路径
    path_result_conll = 'your.conll'  # conll格式路径(可为None)
    stanford_parser.predict_dep(path_model, path_txt, path_result_dep, path_result_conll)


if __name__ == '__main__':
    # 处理句子中的括号，若使用'-tokenized'参数，即输入的是符号化之后的句子，则必须处理句子中的括号
    # 若已经处理，则忽略此步骤
    path_ori = 'path_to_ori_file'
    path_proprecess = 'path_to_preprocess_file'
    preprocessing_sentence(path_ori, path_proprecess)

    # parse sentence, parser结果为ptb格式
    parser_ptb_demo()

    # parser sentence，parser结果为dependency格式
    parser_dep_demo()
