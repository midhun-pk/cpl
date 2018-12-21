from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.chunk.regexp import RegexpParser
from cpl.constants import GRAMMERS
from cpl import utils

def lex(noun_phrase):
    '''
    Extract proper noun using lex algorithm from noun phrase that contains prepositions
    and conjunctions

    @param noun_phrase: phrase which contains preposition or conjunctions or both
    @return proper_noun: proper noun extracted using lex algorithm
    '''
    return noun_phrase

def is_noisy(tagged_sentence):
    '''
    sentences without a verb, without any lowercase words, with too many
    words that were all capital letters should be eliminated
    '''
    return False

def extract_common_noun(tree):
    '''
    Extract the common noun from the tree that follows the common noun grammer.

    @param tree: A tree with tokens as leaf that follows the common noun grammer
    @return common_noun: A common noun string
    '''
    common_noun = ''
    are_stop_words = True
    contains_capital_letter = False
    for leaf in tree.leaves():
        token = leaf[0]
        common_noun = common_noun + token + ' '
        if not utils.is_stop_word(token): are_stop_words = False
        if utils.has_capital_letters(token): contains_capital_letter = True
    common_noun = common_noun.strip()
    if common_noun and not are_stop_words and not contains_capital_letter:
        return common_noun

def extract_proper_noun(tree):
    '''
    Extract the proper noun from the tree that follows the proper noun grammer.

    @param tree: A tree with tokens as leaf that follows the proper noun grammer
    @return proper_noun: A proper noun string
    '''
    proper_noun = ''
    are_stop_words = True
    contains_prep_conjs = False
    contains_capital_letter = False
    for leaf in tree.leaves():
        token, tag = leaf[0], leaf[1]
        proper_noun = proper_noun + token + ' '
        if not utils.is_stop_word(token): are_stop_words = False
        if utils.is_prep_conj(tag): contains_prep_conjs = True
        if utils.has_capital_letters(token): contains_capital_letter = True
    proper_noun = proper_noun.strip()
    if proper_noun and not are_stop_words and contains_capital_letter:
        if contains_prep_conjs: proper_noun = lex(proper_noun)
        return proper_noun

def extract_phrase(tree):
    phrase = ''
    for leaf in tree.leaves(): phrase += leaf[0] + ' '
    phrase = phrase.strip()
    return phrase

def is_relation(pattern):
    '''
    Verify whether a pattern satisfies the relation pattern conditions or not

    @param pattern: pattern to be verified
    @param result: Boolean - True or False
    '''
    pattern = pattern.strip()
    word_count = 0
    are_stop_words = True
    contains_uncapitalized_word = False
    tokens = word_tokenize(pattern)
    is_empty = True if not pattern else False
    contains_atmost_five_tokens = True if len(tokens) <= 5 else False
    for token in tokens:
        if utils.is_word(token): word_count += 1
        if not utils.is_stop_word(token): are_stop_words = False
        if not utils.has_capital_letters(token): contains_uncapitalized_word = True
    result = word_count > 1 and contains_uncapitalized_word and contains_atmost_five_tokens and not is_empty and not are_stop_words
    return result

def is_candidate_tree(tree):
    result = False
    if tree.label() == 'PI' or tree.label() == 'IP' or tree.label() == 'IPI':
        result = True
    return result

def generate_couples(tags):
    instance_pattern = {}
    for grammar in GRAMMERS:
        parser = RegexpParser(grammar['EXPRESSION'])
        chunks = parser.parse(tags)
        for chunk in chunks.subtrees():
            if not is_candidate_tree(chunk): continue
            extracted = []
            for subtree in chunk.subtrees():
                if subtree.label() == 'PN': 
                    instance = extract_proper_noun(subtree)
                    if instance: extracted.append(instance)
                if subtree.label() == 'CN': 
                    instance = extract_common_noun(subtree)
                    if instance: extracted.append(instance)
                if subtree.label() == 'PR1' or subtree.label() == 'PR2' or \
                    subtree.label() == 'PL1' or subtree.label() == 'PL2' or \
                    subtree.label() == 'RP':
                    pattern = extract_phrase(subtree)
                    if pattern: 
                        if subtree.label() == 'RP':
                            if is_relation(pattern): 
                                extracted.append(pattern)
                        else: 
                            extracted.append(pattern)
            string = ''
            if chunk.label() == 'IPI' and len(extracted) == 3:
                string = 'RELATION - '
                for token in extracted:
                    string += '(' + token + ') '
                print(string.strip())
            if (chunk.label() == 'IP' or chunk.label() == 'PI') and len(extracted) == 2:
                string = 'CATEGORY - '
                for token in extracted:
                    string += '(' + token + ') '
                print(string.strip())


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
                tags = utils.tag(sentence)
                if not tags or is_noisy(tags): continue
                generate_couples(tags)
                
    return tagged_sentences

def extract():
    sentence = 'There will be “Terms & Conditions” hyperlink on the registration page.'
    tags = utils.tag(sentence)
    print(tags)
    for grammar in GRAMMERS:
        parser = RegexpParser(grammar['EXPRESSION'])
        chunks = parser.parse(tags)
        print(chunks)
        for chunk in chunks.subtrees():
            if not is_candidate_tree(chunk): continue
            extracted = []
            for subtree in chunk.subtrees():
                if subtree.label() == 'PN': 
                    instance = extract_proper_noun(subtree)
                    extracted.append(instance)
                if subtree.label() == 'CN': 
                    instance = extract_common_noun(subtree)
                    extracted.append(instance)
                if subtree.label() == 'PR1' or subtree.label() == 'PR2' or \
                    subtree.label() == 'PL1' or subtree.label() == 'PL2' or \
                    subtree.label() == 'RP':
                    pattern = extract_phrase(subtree)
                    if pattern: 
                        if subtree.label() == 'RP':
                            if is_relation(pattern): 
                                extracted.append(pattern)
                        else: 
                            extracted.append(pattern)
            string = ''
            if chunk.label() == 'IPI' and len(extracted) == 3:
                string = 'RELATION - '
                for token in extracted:
                    string += '(' + token + ') '
                print(string.strip())
            if (chunk.label() == 'IP' or chunk.label() == 'PI') and len(extracted) == 2:
                string = 'CATEGORY - '
                for token in extracted:
                    string += '(' + token + ') '
                print(string.strip())