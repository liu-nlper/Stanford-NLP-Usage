#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    处理句子中的括号，转换为stanford parser能够处理的格式。
"""

replace_map = {
    '(': '-LRB-', ')': '-RRB-',
    '[': '-LRB-', ']': '-RRB-',
    '{': '-LRB-', '}': '-RRB-'}


def preprocessing_sentence(sentence):
    """
    处理原句子中的括号

    Args:
        sentence: str，原始句子
    Returns:
        sentence: str, 处理后的句子
    """
    chars = list(sentence)
    for i, c in enumerate(chars):
        c = chars[i]
        if c in replace_map:
            chars[i] = replace_map[c]
    return ''.join(chars)


def demo():
    sentence = 'the { quick } brown ( fox ) jumps [ over ] the lazy dog.'
    print(preprocessing_sentence(sentence))


if __name__ == '__main__':
    demo()