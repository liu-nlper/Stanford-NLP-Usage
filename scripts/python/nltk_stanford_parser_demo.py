#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    更多信息参考： nltk/parse/stanford.py
"""

from nltk.parser.stanford import StanfordParser


def demo():
    # 即stanford-parser.jar的路径
    path_to_jar = 'path to jar'

    # tanford-parser-x.x.x-models.jar，其中`x.x.x`为具体的版本号
    path_to_model_jar = 'path to model jar'

    # 模型的路径，例如model_path='edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
    # 若需解析中文，则将`englishPCFG.ser.gz`替换为相应的中文模型
    model_path = 'path to model'

    parser = StanfordParser(
        path_to_jar=path_to_jar,
        path_to_model_jar=path_to_model_jar,
        model_path=model_path,
        verbose=False,
        java_options='-mx1000m',
        corenlp_options=''
    )

    # parser单个句子
    # Use StanfordParser to parse a sentence. Takes a sentence as a string;
    # before parsing, it will be automatically tokenized and tagged by
    # the Stanford Parser.
    parser.raw_parse('the quick brown fox jumps over the lazy dog.')

    # parser多个句子
    sentences = [
        'the quick brown fox jumps over the lazy dog.',
        'the quick brown fox jumps over the lazy dog.']
    parser.raw_parse_sents(sentences)

    # parser符号化之后的句子
    # Use StanfordParser to parse a sentence.Takes a sentence as a list
    # of (word, tag) tuples; the sentence must have already been tokenized
    # and tagged.
    taged_sent = [
        ("The", "DT"), ("quick", "JJ"), ("brown", "JJ"), ("fox", "NN"),
        ("jumped", "VBD"), ("over", "IN"), ("the", "DT"), ("lazy", "JJ"),
        ("dog", "NN"), (".", ".")]
    parser.tagged_parse(taged_sent)

    # 批量解析符号化之后的句子
    taged_sents = [taged_sent, taged_sent, taged_sent]
    parser.tagged_parse_sents(taged_sents)


if __name__ == '__main__':
    demo()
