#! /usr/bin/env python
# coding:utf-8


from cabocha.tokenizer import CaboChaBasicTokenizer


class CaboChaContentWordTokenizer(CaboChaBasicTokenizer):
    """文の意味を表す語の原型のリストを出力するトークナイザー"""
    def __init__(self):
        super().__init__(pos=None)

    def tokenize(self, text):
        return [token.surface if token.genkei == "*" else token.genkei
                for token in self._analyzer.parse(text).tokens
                if self._is_valid_token(token)]

    def _is_valid_token(self, token):
        """トークンが文の意味を表す場合は True を返す"""
        cond = [token.pos in {"動詞", "形容詞", "名詞", "感動詞",
                              "記号", "副詞",
                              "連体詞",  # 「あの」
                              "接続詞",
                              } or
                # 過去形
                (token.pos == "助動詞" and token.genkei == "た") or  # 過去形の「た」
                # 否定形
                (token.pos == "助動詞" and token.genkei == "ん")  or # 「いきません」の「ん」
                (token.pos == "助動詞" and token.genkei == "ない") or
                # 欲求
                (token.pos == "助動詞" and token.genkei == "たい")
                # 疑問
                ]
        return any(cond)
