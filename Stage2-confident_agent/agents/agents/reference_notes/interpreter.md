# Interpreter
keywords: interpreter, interpreter pattern, grammar, language, abstract syntax tree, expression
- Intent: given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language. Class behavioral.
- Use when there is a language to interpret and statements can be represented as abstract syntax trees.
- Works best when the grammar is simple (for complex grammars the class hierarchy becomes large and unmanageable; parser generators are better) and when efficiency is not critical (the most efficient interpreters usually first translate parse trees into another form, such as state machines).
- Participants: AbstractExpression (declares the Interpret operation common to all AST nodes), TerminalExpression (one instance per terminal symbol in a sentence), NonterminalExpression (one class per grammar rule; holds subexpressions and calls Interpret recursively), Context (information global to the interpreter), Client (builds or is given the AST and invokes Interpret).
- Collaboration: each nonterminal defines Interpret in terms of its subexpressions; terminals define the base case; nodes use the Context to store and access interpreter state.
- Benefits: easy to change and extend the grammar (inheritance); implementing the grammar is easy since node classes are similar; easy to add new ways of interpreting expressions (e.g. pretty printing, type checking).
- Liability: complex grammars are hard to maintain since at least one class per rule is needed. If you keep adding new interpretations, consider Visitor.
- Known uses: compilers in object-oriented languages (Smalltalk compilers), SPECTalk, QOCA constraint solver; the regular-expression grammar is the motivating example.
- Related: the abstract syntax tree is an instance of Composite (nearly every use of Composite contains Interpreter in general form, but reserve Interpreter for when the hierarchy defines a language); Flyweight shares terminal symbols; Iterator can traverse the structure; Visitor can keep per-node behavior in one class.
