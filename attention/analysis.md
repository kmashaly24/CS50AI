BERT Attention Head Analysis

After running mask.py with various sentences and examining the generated attention diagrams, I identified two distinct linguistic relationships that specific attention heads appear to have learned, separate from the adjacency and adverb-verb relationships noted in the specification.

1. Verb and Direct Object Relationship

Layer: Layer 6

Head: Head 1

Description: This attention head appears to have learned to establish a connection between a transitive verb and the start of its direct object phrase. 

Example Sentences:

Sentence: I baked a delicious [MASK] for dinner.

Observation: The verb "baked" shows a strong attention link to the determiner "a" and the adjective "delicious", highlighting the upcoming direct object phrase.

Sentence: The engineers designed an intricate new [MASK] to solve the problem.

Observation: The verb "designed" exhibits high attention scores directed back at the tokens "an" and "intricate", successfully isolating the phrase that begins the object of the verb.

2. Pronoun and Antecedent Co-reference

Layer: Layer 9

Head: Head 4

Description: This attention head seems to be dedicated to solving co-reference, specifically connecting a pronoun back to its preceding antecedent (the noun or noun phrase it replaces).

Example Sentences:

Sentence: The cat curled up, and then it fell asleep in the [MASK].

Observation: The pronoun "it" shows its strongest attention score directed back at the token "cat", correctly identifying the subject of the previous clause as its antecedent.

Sentence: After the tourists saw the famous monument, they decided to visit the [MASK].

Observation: The pronoun "they" strongly attends to the token "tourists", successfully linking the action in the second clause to the correct entity in the first.
