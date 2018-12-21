CPL_FILTER_CONSTANT = 0.3

PATTERN_GRAMMER_LEFT = {
	'EXPRESSION' : 'P1: {<NN.?.?>*<VB.?>+<JJ.?|DT|IN>+$}\nP2: {(<NN.?.?><JJ.?>|<JJ.?><NN.?.?>)+<JJ.?|DT|IN>+$}',
	'PRECEDING1_DESC' : '(noun) - optional, (verb) - one or more, (adjectives, prepositions, or determiners) - optional',
	'PRECEDING2_DESC' : '(nouns or adjectives), (adjectives, prepositions, or determiners) - optional'
}

PATTERN_GRAMMER_RIGHT = {
	'EXPRESSION' : 'F1: {^<VB.?>+<IN|TO>}\nF2: {^<VB.?>+<DT>?<JJ.?>*<NN.?.?>+}',
	'FOLLOWING1_DESC' : 'verbs followed by a preposition',
	'FOLLOWING2_DESC' : 'verbs followed optionally by a noun phrase'
}

INSTANCE_GRAMMER_LEFT = {
	'EXPRESSION' : 'CN: {<JJ|NN|NNS>*<NN|NNS>+$}\nPN: {<IN|CC>*<NNP|NNPS>+<IN|CC>*$}',
	'GRAMMER_DESC' : 'Common Nouns or Proper Nouns'
}

INSTANCE_GRAMMER_RIGHT = {
	'EXPRESSION' : 'CN: {^<JJ|NN|NNS>*<NN|NNS>+}\nPN: {^<IN|CC>*<NNP|NNPS>+<IN|CC>*}',
	'GRAMMER_DESC' : 'Common Nouns or Proper Nouns'
}

CATEGORY_INSTANCE_PATTERN = {
	'EXPRESSION': '''
	CN: {<JJ|NN|NNS>*<NN|NNS>+}
	PN: {<NNP|NNPS>*<IN|CC>*<NNP|NNPS>+<IN|CC>*<NNP|NNPS>*}
	PR1: {<VB.?>+<IN|TO>}
	PR2: {<VB.?>+<DT>?<JJ.?>*<NN.?.?>+}
	IP: {<CN><PR1>|<CN><PR2>|<PN><PR1>|<PN><PR2>}
	''',
	'GRAMMER_DESC': 'Finds (category_instance)(category_pattern)'
}

CATEGORY_PATTERN_INSTANCE = {
	'EXPRESSION': '''
	CN: {<JJ|NN|NNS>*<NN|NNS>+}
	PN: {<NNP|NNPS>*<IN|CC>*<NNP|NNPS>+<IN|CC>*<NNP|NNPS>*}
	PL1: {<NN.?.?>*<VB.?>+<JJ.?|DT|IN>+}
	PL2: {(<NN.?.?><JJ.?>|<JJ.?><NN.?.?>)+<JJ.?|DT|IN>+}
	PI: {<PL1><CN>|<PL2><CN>|<PL1><PN>|<PL2><PN>}
	''',
	'GRAMMER_DESC': 'Finds (category_pattern)(category_instance)'
}

RELATION_INSTANCE_PATTERN_INSTANCE = {
	'EXPRESSION': '''
	CN: {<JJ|NN|NNS>*<NN|NNS>+}
	PN: {<NNP|NNPS>*<IN|CC>*<NNP|NNPS>+<IN|CC>*<NNP|NNPS>*}
	RP: {<(?!PN|CN).+>{1,5}}
	IPI: {<CN><RP><CN>|<CN><RP><PN>|<PN><RP><CN>|<PN><RP><PN>}
	''',
	'GRAMMER_DESC': 'Finds (relation_instance)(relation_pattern)(relation_instance)'
}

GRAMMERS = [CATEGORY_INSTANCE_PATTERN, CATEGORY_PATTERN_INSTANCE, RELATION_INSTANCE_PATTERN_INSTANCE]