import re
from cpl import utils
from cpl.constants import INSTANCE_GRAMMER_LEFT, INSTANCE_GRAMMER_RIGHT
from nltk.tag.util import str2tuple
from nltk.chunk.regexp import RegexpParser

def lex(noun_phrase):
    '''
    Extract proper noun using lex algorithm from noun phrase that contains prepositions
    and conjunctions

    @param noun_phrase: phrase which contains preposition or conjunctions or both
    @return proper_noun: proper noun extracted using lex algorithm
    '''
    return noun_phrase

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

def extract_noun_phrase(fragment, grammer, type):
    '''
    Extract proper noun or common noun phrase from the fragment using the grammer.

    @param fragment: part of the sentence
    @param grammer: grammer used to extract noun phrase
    @param type: type of the noun phrase - proper/common/all
    @return noun_phrase: a noun phrase that follows the rules or empty string  
    '''
    tags = [str2tuple(tag) for tag in fragment.split()]
    parser = RegexpParser(grammer['EXPRESSION'])
    chunks = parser.parse(tags)
    noun_phrase = ''
    for subtree in chunks.subtrees():
        if (type == 'proper' or type == 'all') and subtree.label() == 'PN': 
            noun_phrase = extract_proper_noun(subtree)
        if (type == 'common' or type == 'all') and subtree.label() == 'CN': 
            noun_phrase = extract_common_noun(subtree)
    return noun_phrase

def extract_instances(sentences, aug_pattern, instance1_type, instance2_type = None):
    '''
    Extract instance for the pattern according to the position

    @param sentences: tagged sentences from which the instance to be extracted
    @param aug_pattern: pattern used to split sentence into fragments - contains blanks
    @param instance1_type: type of the first noun phrase - proper/common/all
    @param instance2_type: type of the second noun phrase - proper/common/all
    @return instances: A list of instances
    '''
    instances = []
    position = utils.get_blank_pos(aug_pattern)
    pattern = utils.remove_blanks(aug_pattern)
    regex_pattern = utils.create_regex(pattern)
    for sentence in sentences:
        if utils.is_candidate(sentence, regex_pattern):
            split_pattern = utils.begin_middle_pattern(regex_pattern)
            fragments = re.split(split_pattern, sentence)
            for i in range(len(fragments) - 1):
                left_instance = right_instance = ''
                left_fragment = fragments[i].strip()
                if left_fragment and (position == 'LEFT' or position == 'BOTH'): 
                    type = instance1_type
                    left_instance = extract_noun_phrase(left_fragment, INSTANCE_GRAMMER_LEFT, type)
                right_fragment = fragments[i + 1].strip()
                if right_fragment and (position == 'RIGHT' or position == 'BOTH'):
                    type = instance2_type if instance2_type else instance1_type
                    right_instance = extract_noun_phrase(right_fragment, INSTANCE_GRAMMER_RIGHT, type)
                if left_instance and right_instance: instances.append((left_instance, right_instance))
                elif left_instance and position == 'LEFT': instances.append(left_instance)
                elif right_instance and position == 'RIGHT': instances.append(right_instance)
    return instances


        