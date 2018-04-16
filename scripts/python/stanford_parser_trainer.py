#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    重新训练stanford parser
"""
import subprocess


class StanfordParserTrainer(object):

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

    def train(self, path_train, path_model, model='goodFactored',
              path_test=None, path_test_result=None):
        """
        train model
        Args:
            path_train: ptb格式训练文件路径
            path_model: 模型存放路径
            path_test: 测试文件路径, default is None
            path_test_result: 测试文件结果存放路径
        """
        print('training model...', end='')
        # -goodPCFG, -goodFactored, -ijcai03
        command = 'java -mx%s -Djava.ext.dirs=%s %s -evals "factDA,factCB,tsv" -%s ' + \
            '-saveToSerializedFile %s -train %s 0'
        command %= (self._max_mem, self._path_stanford, self._parser_jar,
                    model, path_model, path_train)
        if path_test:
            assert path_test and path_test_result  # not None
            command += (' -testTreebank %s' % path_test)
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if not path_test:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                line = line.decode('utf-8')
                print(line, end='')
            print('done!')
            return
        with open(path_test_result, 'w', encoding='utf-8') as file_w:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                line = line.decode('utf-8')
                print(line, end='')
                file_w.write(line)
        print('done!')
        return


def train_model_demo():
    """
    训练模型
    Args:
        path_train: 训练数据路径
        path_model: 模型存放路径
        model: goodPCFG or goodFactored
    """
    path_stanford = './stanford-parser-full-2016-10-31'
    parser_jar = 'edu.stanford.nlp.parser.lexparser.LexicalizedParser'
    stanford_parser = StanfordParserTrainer(path_stanford, parser_jar)

    path_train = 'path_to_train_ptb'  # 训练文件路径ptb格式
    path_test = 'path_to_test_ptb'  # 测试文件路径(可为None)
    path_model = 'your_model.tar.gz'  # 模型保存路径
    model = 'goodFactored'  # 使用哪种方式进行训练

    stanford_parser.train(path_train, path_model, model=model, path_test=path_test)


if __name__ == '__main__':
    train_model_demo()