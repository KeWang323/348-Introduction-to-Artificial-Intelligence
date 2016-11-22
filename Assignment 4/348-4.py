#coding=utf-8
'''
Created on 2016年11月11日

@author: KeWang TianyuZhao YifeiGe
'''
# encoding: utf-8


import read
import facts_and_rules

facts, rules = read.read_tokenize("statements.txt")

global KB
KB = []
global RB
RB = []

def Assert_Rule(rule):
    RB.append(rule)
    infer_from_rule(rule)


def Assert(fact):
    KB.append(fact)
    infer_from_fact(fact)


def infer_from_fact(fact):
    for r in RB:
        bindings = facts_and_rules.match(r.lhs[0], fact)
        if bindings != False:
            if len(r.lhs) == 1:
                fact_infered = facts_and_rules.statement(facts_and_rules.instantiate(r.rhs.full, bindings))
                fact.add_fact(fact_infered)
                dup = False
                for f in KB:
                    dup = dup | facts_and_rules.pattern_match(fact_infered, f)
                if not dup:
                    Assert(fact_infered)
                print "fact" + fact.pretty() + "fact inferred" + fact_infered.pretty()
            else:
                tests = map(lambda x : facts_and_rules.instantiate(x.full, bindings), r.lhs[1:])
                rhs = facts_and_rules.instantiate(r.rhs.full, bindings)
                new_rule = facts_and_rules.rule(tests, rhs)
                fact.add_rule(new_rule)
                Assert_Rule(new_rule)
        print "Hey there " + r.name + " matches " + fact.pretty()

def infer_from_rule(rule):
    for f in KB:
        bindings = facts_and_rules.match(rule.lhs[0], f)
        if bindings != False:
            if len(rule.lhs) == 1:
                fact_infered = facts_and_rules.statement(facts_and_rules.instantiate(rule.rhs.full, bindings))
                rule.add_fact(fact_infered)
                dup = False
                for f in KB:
                    dup = dup | facts_and_rules.pattern_match(fact_infered, f)
                if not dup:
                    Assert(fact_infered)

                print "rule" + rule.pretty() + "fact inferred" + fact_infered.pretty()
            else:
                tests = map(lambda x : facts_and_rules.instantiate(x.full, bindings), rule.lhs[1:])
                rhs = facts_and_rules.instantiate(rule.rhs.full, bindings)
                new_rule = facts_and_rules.rule(tests, rhs)
                rule.add_rule(new_rule)
                Assert_Rule(new_rule)
        print "Hey there " + f.pretty() + " matches " + rule.name

def Retract(statement):
    for fact in KB:
        if facts_and_rules.pattern_match(statement, fact) != False:
            remove_facts_supports(fact)
            remove_rules_supports(fact)


def remove_facts_supports(predict):
    print "Removing: " + predict.pretty()
    for f in predict.facts:
        remove_facts_supports(f)
    KB.remove(predict)


def remove_rules_supports(predict):
    print "Removing: rules of " + predict.pretty()
    for r in predict.rules:
        remove_facts_supports(r)
    RB.remove(predict)

def Ask(pattern):
    list_of_bindings_lists = []
    for fact in KB:
        bindings = facts_and_rules.match(pattern, fact)
        if bindings != False:
            list_of_bindings_lists.append(bindings)
    if not list_of_bindings_lists:
        print "This is False:\t"
    for b in list_of_bindings_lists:
        print "This is true: \t"
        print facts_and_rules.statement(facts_and_rules.instantiate(pattern.full, b)).pretty()
      
def big_Ask(patterns):
    bindings_lists = []
    sign = True
    for pattern in patterns:
        if bindings_lists != []:
            for pair in map(lambda b: (facts_and_rules.instantiate(pattern.full, b), b), bindings_lists):
                for fact in KB:
                    bindings = facts_and_rules.match(pair[0], fact)
                    if bindings != False:
                        for key in pair[1]:
                            bindings[key] = pair[1][key]
                        bindings_lists.append(bindings)
                        if sign:
                            print "This is true\t"
                            sign = False
                        print facts_and_rules.statement(facts_and_rules.instantiate(pattern.full, bindings)).pretty()


        else:
            for fact in KB:
                bindings = facts_and_rules.match(pattern, fact)
                if bindings != False:
                    bindings_lists.append(bindings)
                    if sign:
                        print "This is true\t"
                        sign=False
                    print facts_and_rules.statement(facts_and_rules.instantiate(pattern.full, bindings)).pretty()
    if not bindings_lists:
        print "None is true:\t"
   # for b in bindings_lists:
    #    print "\nThis is true:\t"
      #  for pattern in patterns:
    #     print facts_and_rules.statement(facts_and_rules.instantiate(pattern.full,b)).pretty()

print "Asserting Rules\t"
for new_rule in rules:
    Assert_Rule(facts_and_rules.rule(new_rule[0], new_rule[1]))

print "Asserting facts\t"
for fact in facts:
    Assert(facts_and_rules.statement(fact))

print "Start Testing\t"
print "Testing Assert and retract\t"
print RB[0].lhs[0].full
print KB[0].full
# print KB[22].facts[0].full
print KB[23].full
print "Testing Ask"
#simply for testing ASK
TB=[]
TB.append(facts_and_rules.statement(['color', 'pyrami13', '`blue']))
TB.append(facts_and_rules.statement(['color', '?x', 'green']))
Ask(TB[0])
Ask(TB[1])
#test end
print "Testing Big Ask"
big_Ask(TB)
print "Test succeeded"


    