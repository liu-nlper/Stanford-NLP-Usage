#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    将xml标注格式转为PTB format

    共18541个trees，其中111个格式错误，有效的trees共18430
"""
import re
import os
import sys
from time import time
from collections import defaultdict
# from nltk.tree import Tree
# from bs4 import BeautifulSoup


# map
token_map_dict = {
    'COMMA': ',', 'PERIOD': '.',
    'LRB': '-LRB-', 'RRB': '-RRB-',
    'LQT': '``', 'RQT': '\'\'',
    'COLON': ':'
}
esc_char_map = defaultdict(set)
replace_map = {
    '(': '-LRB-', ')': '-RRB-',
    '[': '-LRB-', ']': '-RRB-',
    '{': '-LRB-', '}': '-RRB-'
}


# patterns
pattern_sent = re.compile('(<sentence.*?>.*?</sentence>)')
pattern_tok = re.compile('<tok cat="(.*?)">(.*?)</tok>')
pattern_cat = re.compile('<(sentence id|cons cat)="(.*?)".*?>')
pattern_close = re.compile('</.*?>')
pattern_space = re.compile('\s+')
pattern_cor = re.compile('\([a-zA-Z]+ \)')


def replace_pair(token):
    """
    替换token中的括号
    """
    token = list(token)
    for i in range(len(token)):
        c = token[i]
        if c in replace_map:
            token[i] = replace_map[c]
    return ''.join(token)


def check_bracket(sentence):
    """
    检查括号是否匹配
    Return:
        bool
    """
    brackets = []
    for c in sentence:
        if c == '(':
            brackets.append(c)
        elif c == ')':
            if not len(brackets):
                return False
            brackets.pop()
    return not bool(len(brackets))


def handle_sentence(sentence):
    # replace all tokens
    token_iter = pattern_tok.finditer(sentence)
    token_rev = []
    for item in token_iter:
        start, end = item.start(), item.end()
        cat, name = item.groups(0)[:]
        cat_m = cat
        name = replace_pair(pattern_space.sub('', name))
        if cat in token_map_dict:
            cat_m = token_map_dict[cat]
            esc_char_map[cat_m].add(name)
        token_rev.append([start, end, cat_m, name])
    sentence = list(sentence)
    for item in token_rev[::-1]:
        start, end, cat, name = item[:]
        sub_str = ' (%s %s)' % (cat, name)
        sentence[start:end] = list(sub_str)
    # replace </xxx> with ')'
    sentence = pattern_close.sub(')', ''.join(sentence))
    # replace '<cons cat="NP" ...>' with '(NP '
    cat_iter = pattern_cat.finditer(sentence)
    cat_signs = []
    for item in cat_iter:
        start, end = item.start(), item.end()
        tag, name = item.groups(0)[:]
        if tag == 'sentence id':
            name = 'S'
        cat_signs.append([start, end, name])
    sentence = list(sentence)
    for item in cat_signs[::-1]:
        start, end, name = item[:]
        sub_str = '(%s ' % name
        sentence[start:end] = list(sub_str)
    sentence = pattern_space.sub(' ', ''.join(sentence))
    sentence = pattern_cor.sub('', sentence)
    if not check_bracket(sentence):  # 检查格式
        return None
    # try:  # check
    #     Tree.fromstring(sentence)
    # except Exception as e:
    #     return None
    return sentence


total_count = 0


def handle_article(name, file_ptb_w):
    """
    Args:
        name: 待处理文件名
        file_ptb_w:
    """
    with open(name, 'r', encoding='utf-8') as file_r:
        text = file_r.read()
    sentences = pattern_sent.findall(text)
    error_count, useful_count = 0, 0
    for sentence in sentences:
        sentence_h = handle_sentence(sentence)
        if not sentence_h:  # 共111个格式错误
            # print(sentence)
            error_count += 1
            continue
        useful_count += 1
        #if total_count == 478:
        #    print(sentence)
        #    print(sentence_h)
        #    exit()
        sentence_h = pattern_cor.sub('', sentence_h)  # why
        file_ptb_w.write('%s\n' % sentence_h)
    return useful_count, error_count


def main():
    root_xml = './GENIA_treebank_v1_xml/'
    root_ptb = './GENIA_treebank/'
    if not os.path.exists(root_ptb):
        os.mkdir(root_ptb)
    path_ptb = root_ptb + 'GENIA_SP.ptb'
    file_ptb_w = open(path_ptb, 'w', encoding='utf-8')
    file_list = os.listdir(root_xml)
    useful_count, error_count = 0, 0
    for i, name in enumerate(file_list):
        sys.stdout.write('processing xml files: {0}\r'.format(i+1))
        sys.stdout.flush()
        useful_count_, error_count_ = handle_article(root_xml + name, file_ptb_w)
        useful_count += useful_count_
        error_count += error_count_
    sys.stdout.write('processing xml files: {0}\n'.format(i+1))
    file_ptb_w.close()
    # 字符替换映射表
    with open(root_ptb+'esc_char.map', 'w', encoding='utf-8') as file_w:
        for key in esc_char_map:
            char_list = esc_char_map[key]
            for c in char_list:
                file_w.write('%s\t%s\n' % (c, key))

    print('useful count: {0}'.format(useful_count))
    print('error count: {0}'.format(error_count))
    print('result has been saved to: {0}'.format(path_ptb))


if __name__ == '__main__':
    t0 = time()

    main()
    print('done in {0:.1f}s!'.format(time()-t0))
