from cpl.constants import CPL_FILTER_CONSTANT

def count_instance_mutex_coocurance(instance, exceptions, all_predicates):
    '''
    Count number of times it co-occurs with patterns from mutually exclusive predicates

    @param instance: Category or relational instance
    @param exceptions: Non mutually exclusive predicates
    @param all_predicates: All predicates 
    '''
    mutex_count = 0
    for predicate in all_predicates:
        if predicate.name in exceptions:
            continue
        candidate_instances = predicate.candidate_instances
        if instance in candidate_instances:
            patterns = candidate_instances[instance]
            mutex_count += sum(patterns.values())
    return mutex_count


def filter_instance(predicates):
    '''
    Filter the candidate instances. Input categories or relations will have promoted instances 
    and their co-occurance count with patterns.

    @param predicates: Candidate categories and relations 
    '''
    # Each predicate in a category or instances
    promoted = []
    for predicate in predicates:
        predicate.filtered_candidate_instances = {}
        predicate.last_promoted_instances = []
        exceptions = predicate.mutex_exceptions
        exceptions.append(predicate.name)
        for instance, patterns in predicate.candidate_instances.items():
            mutex_count = count_instance_mutex_coocurance(instance, exceptions, predicates)
            mutex_count = 1 if mutex_count == 0 else mutex_count
            for count in patterns.values():
                if count > CPL_FILTER_CONSTANT * mutex_count:
                    predicate.filtered_candidate_instances[instance] = sum(patterns.values())
                    if type(instance) == tuple:
                        instance = list(instance)
                    if instance not in predicate.last_promoted_instances and instance not in predicate.instances:
                        predicate.last_promoted_instances.append(instance)
                        predicate.instances.append(instance)
                        print('FILTERED', predicate.name, instance)
                        if predicate not in promoted: promoted.append(predicate)
                    break
        #predicate.save()
    return promoted

def count_pattern_mutex_coocurance(pattern, exceptions, all_predicates):
    '''
    Count number of times it co-occurs with patterns from mutually exclusive predicates

    @param pattern: Category or relational pattern
    @param exceptions: Non mutually exclusive predicates
    @param all_predicates: All predicates 
    '''
    mutex_count = 0
    for predicate in all_predicates:
        if predicate.name in exceptions:
            continue
        candidate_patterns = predicate.candidate_patterns
        if pattern in candidate_patterns:
            instances = candidate_patterns[pattern]
            mutex_count += sum(instances.values())
    return mutex_count

def filter_pattern(predicates):
    '''
    Filter the candidate patterns. Input categories or relations will have promoted patterns 
    and their co-occurance count with instances.

    @param predicates: Candidate categories and relations 
    '''
    # Each predicate in a category or instances
    promoted = []
    for predicate in predicates:
        predicate.filtered_candidate_patterns = {}
        predicate.last_promoted_instances = []
        exceptions = predicate.mutex_exceptions
        exceptions.append(predicate.name)
        for pattern, instances in predicate.candidate_patterns.items():
            mutex_count = count_pattern_mutex_coocurance(pattern, exceptions, predicates)
            mutex_count = 1 if mutex_count == 0 else mutex_count
            for count in instances.values():
                if count > CPL_FILTER_CONSTANT * mutex_count:
                    predicate.filtered_candidate_patterns[pattern] = sum(instances.values())
                    if pattern not in predicate.last_promoted_patterns and pattern not in predicate.patterns:
                        predicate.last_promoted_patterns.append(pattern)
                        predicate.patterns.append(pattern)
                        print('FILTERED', predicate.name, pattern)
                        if predicate not in promoted: promoted.append(predicate)
                    break
        #predicate.save()
    return promoted
    #print(pattern_counts)