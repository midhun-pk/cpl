import re
from cpl import utils
from cpl.constants import PATTERN_GRAMMER_LEFT, PATTERN_GRAMMER_RIGHT
from nltk.tag.util import str2tuple
from nltk.chunk.regexp import RegexpParser
from nltk.tokenize import word_tokenize

def extract_preceding_phrase(tree):
    '''
    Extract preceding phrase from tree

    @param tree: A tree with tokens as leaf that follows the preceding grammer
    @return preceding_phrase: The phrase
    '''
    pass

def extract_following_phrase(tree):
    '''
    Extract following phrase from tree

    @param tree: A tree with tokens as leaf that follows the following grammer
    @return following_phrase: The phrase
    '''
    pass

def is_relation(pattern):
    '''
    Verify whether a pattern satisfies the relation pattern conditions or not

    @param pattern: pattern to be verified
    @param result: Boolean - True or False
    '''
    pattern = pattern.strip()
    are_stop_words = True
    contains_uncapitalized_word = False
    tokens = word_tokenize(pattern)
    is_empty = True if not pattern else False
    contains_atmost_five_tokens = True if len(tokens) <= 5 else False
    for token in tokens:
        if not utils.is_stop_word(token): are_stop_words = False
        if not utils.has_capital_letters(token): contains_uncapitalized_word = True
    result = contains_uncapitalized_word and contains_atmost_five_tokens and not is_empty and not are_stop_words
    return result

def extract_phrase(fragment, grammer):
    '''
    Extract phrase from the fragment using the grammer.

    @param fragment: part of the sentence
    @param grammer: grammer used to extract noun phrase
    @return phrase: a phrase that follows the rules or empty string  
    '''
    tags = [str2tuple(tag) for tag in fragment.split()]
    parser = RegexpParser(grammer['EXPRESSION'])
    chunks = parser.parse(tags)
    phrase = ''
    for subtree in chunks.subtrees():
        if subtree.label() == 'P1' or subtree.label() == 'P2' or subtree.label() == 'F1' or subtree.label() == 'F2':
            for leaf in subtree.leaves():
                phrase += leaf[0] + ' '
            phrase = phrase.strip()
    return phrase

def extract_category_patterns(sentences, instance):
    '''
    Extract instance for the pattern according to the instance

    @param sentences: tagged sentences from which the instance to be extracted
    @param instance: instance using which category pattern to be extracted
    @return aug_patterns: A list of patterns
    '''
    aug_patterns = []
    regex_pattern = utils.create_regex(instance)
    split_pattern = utils.begin_middle_pattern(regex_pattern)
    for sentence in sentences:
        if utils.is_candidate(sentence, regex_pattern):
            fragments = re.split(split_pattern, sentence)
            for i in range(len(fragments) - 1):
                left_pattern = right_pattern = ''
                left_fragment = fragments[i].strip()
                if left_fragment:
                    left_pattern = extract_phrase(left_fragment, PATTERN_GRAMMER_LEFT)
                right_fragment = fragments[i + 1].strip()
                if right_fragment:
                    right_pattern = extract_phrase(right_fragment, PATTERN_GRAMMER_RIGHT)
                if left_pattern: aug_patterns.append(utils.add_blanks(left_pattern, 'LEFT'))
                elif right_pattern: aug_patterns.append(utils.add_blanks(right_pattern, 'RIGHT'))
    return aug_patterns

def extract_relation_patterns(sentences, instance1, instance2):
    '''
    Extract instance for the pattern according to the instances

    @param sentences: tagged sentences from which the instance to be extracted
    @param instance1: instance using which category pattern to be extracted
    @param instance2: instance using which category pattern to be extracted
    @return aug_patterns: A list of patterns
    '''
    aug_patterns = []
    left_regex_pattern = utils.create_regex(instance1)
    right_regex_pattern = utils.create_regex(instance2)
    regex_pattern = '(' + left_regex_pattern + ')' + ' (.+?) ' + '(' + right_regex_pattern + ')'
    for sentence in sentences:
        if utils.is_candidate(sentence, regex_pattern):
            tagged_patterns = re.findall(regex_pattern, sentence)
            for tagged_pattern in tagged_patterns:
                candidate_pattern = ' '.join([str2tuple(tag)[0] for tag in tagged_pattern[1].split()]).strip()
                if candidate_pattern and is_relation(candidate_pattern):
                    aug_pattern = utils.add_blanks(candidate_pattern, 'BOTH')
                    aug_patterns.append(aug_pattern)
    return aug_patterns