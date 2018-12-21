from cpl.instance_extractor import extract_instances
from cpl.pattern_extractor import extract_category_patterns, extract_relation_patterns
from cpl.filterer import filter_instance, filter_pattern
from cpl import utils
'''
Learm new patterns and categories.
'''

def learn(corpus, cpl):
    '''
    Extract instances amd patterns from the corpus

    @param corpus: corpus from which instances and patterns to be extracted
    @param cpl: CPL object with promoted categories and patterns
    @return categories, relations: newly promoted categories and relations
    '''
    sentences = utils.preprocess_corpus(corpus)
    categories = {}
    relations = {}
    new_promoted_categories = []
    new_promoted_relations = []
    learn_category_instances(sentences, cpl)
    learn_relation_instances(sentences, cpl)
    learn_category_patterns(sentences, cpl)
    learn_relation_patterns(sentences, cpl)
    new_promoted_categories.extend(filter_instance(cpl.last_promoted_categories))
    new_promoted_relations.extend(filter_instance(cpl.last_promoted_relations))
    new_promoted_categories.extend(filter_pattern(cpl.last_promoted_categories))
    new_promoted_relations.extend(filter_pattern(cpl.last_promoted_relations))
    #print(categories, relations)
    cpl.last_promoted_categories = new_promoted_categories
    cpl.last_promoted_relations = new_promoted_relations
    return new_promoted_categories, new_promoted_relations

def learn_category_instances(sentences, cpl):
    '''
    extract category instances from the sentences
    
    @param sentences: A list of sentences from which instances shuold be extracted
    @param cpl: CPL object with promoted categories and patterns
    @param categories: A dict of candidate categories
    '''
    for category in cpl.last_promoted_categories:
        extracted_instances = []
        category.candidate_instances = {}
        aug_patterns = category.patterns if cpl.iter == 0 else category.last_promoted_patterns
        instance_type = category.instance_type
        #  find instances for each pattern in category
        for aug_pattern in aug_patterns:
            instances = extract_instances(sentences, aug_pattern, instance_type)
            if instances: 
                utils.add_candidates(category.candidate_instances, aug_pattern, instances)
                extracted_instances.extend(instances)


def learn_relation_instances(sentences, cpl):
    '''
    extract relation instances from the sentences
    
    @param sentences: A list of sentences from which instances shuold be extracted
    @param cpl: CPL object with promoted categories and patterns
    @param relations: A dict of candidate relations
    '''
    for relation in cpl.last_promoted_relations:
        extracted_instances = []
        relation.candidate_instances = {}
        aug_patterns = relation.patterns if cpl.iter == 0 else relation.last_promoted_patterns
        domain_type = relation.domain.instance_type
        range_type = relation.range.instance_type
        #  find instances for each pattern in relation
        for aug_pattern in aug_patterns:
            instances = extract_instances(sentences, aug_pattern, domain_type, range_type)
            if instances:
                #instances = [tuple2str(instance) for instance in instances]
                utils.add_candidates(relation.candidate_instances, aug_pattern, instances) 
                extracted_instances.extend(instances)


def learn_category_patterns(sentences, cpl):
    '''
    Extract category patterns from the corpus for a particular category

    @param sentences: A list of sentences from which instances shuold be extracted
    @param cpl: CPL object with promoted categories and patterns
    @param categories: A dict of candidate categories
    '''
    for category in cpl.last_promoted_categories:
        extracted_patterns = []
        category.candidate_patterns = {}
        instances = category.instances if cpl.iter == 0 else category.last_promoted_instances
        #  find patterns for each instance in category
        for instance in instances:
            patterns = extract_category_patterns(sentences, instance)
            if patterns:
                utils.add_candidates(category.candidate_patterns, instance, patterns) 
                extracted_patterns.extend(patterns)


def learn_relation_patterns(sentences, cpl):
    '''
    Extract relation patterns from the corpus for a particular relation

    @param sentences: A list of sentences from which instances shuold be extracted
    @param cpl: CPL object with promoted categories and patterns
    @param relations: A dict of candidate relations
    '''
    for relation in cpl.last_promoted_relations:
        extracted_patterns = []
        relation.candidate_patterns = {}
        instances = relation.instances if cpl.iter == 0 else relation.last_promoted_instances
        #  find patterns for each instance in relation
        for instance_tuple in instances:
            patterns = extract_relation_patterns(sentences, instance_tuple[0], instance_tuple[1])
            if patterns: 
                utils.add_candidates(relation.candidate_patterns, tuple(instance_tuple), patterns)
                extracted_patterns.extend(patterns)
