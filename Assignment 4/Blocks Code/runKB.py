def Retract(statement):
	for fact in KB:
		if facts_and_rules.pattern_match(statement, fact) != False:
			remove_facts_supports(fact)

def remove_facts_supports(fact):
	for fact in KB:
		print "Removing: " + fact.pretty()
		for f in fact.facts:
			remove_fact_and_supports(f)
		KB.remove(fact)

def Ask(pattern):
	list_of_bindings_lists = []
	for fact in KB:
		bindings = facts_and_rules.pattern_match(pattern, fact)
		if bindings != False:
			list_of_bindings_lists.remove_fact_and_supports(bindings)
	for b in list_of_bindings_lists:
		pring "This is true: \t",
		print facts_and_rules.statement(facts_and_rules,instantiate(pattern, b)).pretty()