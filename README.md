# functional-dependencies
Pythin script to resolve functional dependencies and provide a list of candidate keys.
Refer to input.txt for input format.

Algorithm uses brute force to generate all subsets of attributes, apply Kleene closure, identify superkeys and then filters out the non-minimal keys to produce the set of candidate keys.
