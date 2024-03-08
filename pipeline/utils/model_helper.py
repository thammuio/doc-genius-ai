"""Model helper functions"""
import re
_re_word_boundaries = re.compile(r'\b')

def count_tokens(text):
    """Counts the number of tokens"""
    return len(_re_word_boundaries.findall(text)) >> 1

def split_into_paragraphs(text, ntoken=400):
    """Splits chunk of text into paragraphs containing less than number of tokens specified"""
    paragraphs = []
    chunks = text.split(". ")
    accu = ''
    for chunk in chunks:
        if count_tokens(accu) + count_tokens(chunk) >= 1.5*ntoken:
            paragraphs.append(accu + ". ")
            paragraphs.append(chunk + ". ")
            accu = ''
        elif count_tokens(accu) + count_tokens(chunk) >= ntoken:
            paragraphs.append(accu  + ". ")
            accu = chunk + ". "
        else:
            accu += chunk + ". "

    if len(accu)>0:
        paragraphs.append(accu)

    return paragraphs
