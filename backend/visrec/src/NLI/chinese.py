from nltk.corpus import stopwords
import jieba
stopwords_set = set(stopwords.words('english'))
stopwords = set([line.strip() for line in open('./model/stopwords_zn/cn_stopwords.txt',encoding='UTF-8').readlines()])

def process_chinese(query):
    cut_words = list(jieba.cut(query))
    return " ".join(cut_words[0:len(cut_words)+1])

# 这里的_word_ngrams方法其实就是sklearn中CountVectorizer函数中用于N-Gram的方法，位置在D:\Python27\Lib\site-packages\sklearn\feature_extraction\text.py
def _word_ngrams(tokens, stop_words=stopwords,ngram_range=(1,1)):
        # handle stop words
        if stop_words is not None:
            tokens = [w for w in tokens if w not in stop_words]

        # handle token n-grams
        min_n, max_n = ngram_range
        if max_n != 1:
            original_tokens = tokens
            tokens = []
            n_original_tokens = len(original_tokens)
            for n in range(min_n,min(max_n + 1, n_original_tokens + 1)):
                for i in range(n_original_tokens - n + 1):
                    tokens.append("".join(original_tokens[i: i + n]))

        return tokens

text = "我去云南旅游，不仅去了玉龙雪山，还去丽江古城，很喜欢丽江古城"
print(process_chinese(text))
# cut = jieba.cut(text)
# listcut = list(cut)
# n_gramWords = _word_ngrams(tokens = listcut,ngram_range=(1,3))
# print(n_gramWords)
