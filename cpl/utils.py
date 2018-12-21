import re
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag.stanford import StanfordPOSTagger
from nltk.tag.util import tuple2str, untag
from nltk.corpus import stopwords
from config import TAGGER, TAGGER_JAR, TAGGER_MODEL

stop_words = set(stopwords.words('english'))

def tag(sentence):
    '''
    Part of speech tag each token in a sentence

    @param sentence: A sentence from the corpus
    @param tagger: name of the tagger used to tag tokens
    @return tagged_sentence: return tagged sentence
    '''
    tokens = word_tokenize(sentence)
   
    tags = []
    if len(tokens) > 3:
        if TAGGER.lower() == 'averagedperceptron': 
            tags = pos_tag(tokens)
        if TAGGER.lower() == 'stanford':
            st = StanfordPOSTagger(TAGGER_MODEL, TAGGER_JAR, encoding='utf-8')
            tags = st.tag(tokens)
    return tags

def read_corpus(file_path):
    '''
    Read each sentence from the corpus and return pos tagged sentences

    @param file_path: path of the corpus
    @param tagger: name of the tagger used to tag tokens
    @return tagged_sentences: return tagged sentences
    '''
    fp = open(file_path, 'r', errors = 'ignore', encoding = 'utf-8')
    tagged_sentences = preprocess_corpus(fp)
    return tagged_sentences

def preprocess_corpus(corpus):
    '''
    Corpus to be preprocessed

    @param corpus: A corpus string
    @return tagged_sentences: A list of pos tagged sentences
    '''
    tagged_sentences = []
    for line in corpus:
        line = line.strip()
        if line:
            tagged_sentence = ''
            for sentence in sent_tokenize(line):
                tags = tag(sentence)
                if tags:
                    tagged_sentence = ' '.join([tuple2str(tag) for tag in tags])
                if tagged_sentence:
                    tagged_sentences.append(tagged_sentence)
    return tagged_sentences

def create_regex(text):
    '''
    Create a regex pattern from the text to split a tagged sentence using the regex

    @param text: The text to be converted into regex
    @return regex: The regex pattern
    '''
    tokens = word_tokenize(text)
    regex = r'/[\S]+ '.join(tokens) + r'/[\S]+'
    regex = regex.replace('.', r'\.')
    return regex

def is_stop_word(token):
    '''
    Validate whether a token is a stopword or not

    @param token: A token to be validated
    @return result: Boolean value True or False
    '''
    result = False
    if token.lower() in stop_words:
        result = True
    return result

def is_prep_conj(tag):
    '''
    Validate whether a tag is a preposition or conjunction

    @param tag: A tag to be validated
    @return result: Boolean value True or False
    '''
    result = False
    if tag == 'IN' or tag == 'CC':
        result = True
    return result

def has_capital_letters(token):
    '''
    Validat whether a token contains capital letters or not

    @param token: A token to be validated
    @return result: Boolean value True or False
    '''
    result = True
    if token.islower():
        result = False
    return result

def get_blank_pos(pattern):
    '''
    Find the position of the blanks in the pattern

    @param pattern: pattern which contain the blanks
    @return position: position of the blank - left/right/both
    '''
    position = ''
    if pattern[0] == '_': position = 'LEFT'
    if pattern[-1] == '_': position = 'RIGHT'
    if pattern[0] == '_' and pattern[-1] == '_': position = 'BOTH'
    return position

def remove_blanks(augmented_pattern):
    '''
    Remove blanks from the augmented pattern

    @param augmented_pattern: pattern which contain the blanks
    @return pattern: pattern withou blanks
    '''
    pattern = augmented_pattern.replace('_', '').strip()
    return pattern

def is_candidate(sentence, pattern):
    '''
    Check if a sentence is a candidate pattern or not
    
    @param sentence: The sentence to be validated
    @param pattern: The pattern to check in the sentence
    @return result: A boolean value - True or False
    '''
    result = False
    # Append .* to match pattern anw where in the sentence
    pattern = '.*' + pattern
    if re.match(pattern, sentence): result = True
    return result

def begin_middle_pattern(regex):
    '''
    Convert a regex to match if the pattern is present in the begin and middle

    @param regex: The regex to be modified
    @return new_regex: The modified regex
    '''
    new_regex = '^' + regex + '| ' + regex
    return new_regex

def add_blanks(pattern, position):
    '''
    Augment the pattern by adding blanks to it

    @param pattern: The pattern to be modified
    @param pattern: The position of the pattern
    @return aug_pattern: The augmented pattern
    '''
    pattern = pattern.strip()
    aug_pattern = ''
    if position == 'LEFT':
        aug_pattern = pattern + ' _'
    if position == 'RIGHT':
        aug_pattern = '_ ' + pattern
    if position == 'BOTH':
        aug_pattern = '_ ' + pattern + ' _'
    return aug_pattern

def add_candidates(parent, child, tokens):
    '''
    Add candidate patterns and instances to parent

    @param parent: categoy or relation mongo object
    @param child: instance or pattern
    @param tokens: candidate patrerns or instances
    '''
    for token in tokens:
        #if type == 'category_instance': token = tuple2str(token)
        if token not in parent:
            parent[token] = {}
        if child not in parent[token]:
            #if type == 'relation_patterns': child = tuple2str(token)
            parent[token][child] = 0
        parent[token][child] += 1

def is_word(token):
    '''
    Check whether the token is a word or not

    @param token: Input token can be 'name', 'place' or ',' etc.
    @param result: Boolean, True or False
    '''
    result = False
    if re.match('[a-zA-Z0-9]+', token): result = True
    return result 