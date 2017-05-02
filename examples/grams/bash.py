#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Defines some basic bash for gramfuzz.
"""


import gramfuzz
import gramfuzz.utils
import gramfuzz.errors
import gramfuzz.rand
from gramfuzz.fields import *


TOP_CAT = "bash"


INDENT_LEVEL = 0
class INDENT(Field):
	def build(self, pre=None, shortest=False):
		global INDENT_LEVEL
		INDENT_LEVEL += 1
		# indent one extra time
		return "    "


class DEDENT(Field):
	def build(self, pre=None, shortest=False):
		global INDENT_LEVEL
		INDENT_LEVEL -= 1
		return NEWLINE().build(pre, shortest=shortest)


# hard-code the category for these classes
class ShDef(Def):
	# no_prune=True
	cat = "sh_def"
class ShRef(Ref):
	# no_prune=True
	cat = "sh_def"


class NEWLINE(Field):
	def build(self, pre=None, shortest=False):
		return "\n" + ("    " * INDENT_LEVEL)

# top level rule
Def("file_input",
	#STAR(Or(NEWLINE, ShRef("statement"))),
	PLUS(ShRef("statement")),
	cat = "bash",
)


ShDef("name", String(min=1, max=10))


# ShDef("statement", "hi", NEWLINE)
ShDef("statement", ShRef("simple_statement") | ShRef("compound_statement")) # maybe ShRef?
ShDef("simple_statement",
	ShRef("small_statement"), STAR("; ", ShRef("small_statement")), Opt(";"), NEWLINE
)
ShDef("compound_statement", Or(
	# ShRef("exec_statement"),
	ShRef("if_statement"),
	# ShRef("while_statement"),
))

ShDef("if_statement", 
	"if", " ", ShRef("name"), ";", "then", " ",ShRef("suite"), ";", 
	STAR("elif", " ", ShRef("name"), ";", "then", " ", ShRef("suite"), ";"), 
	Opt ("else", " ", ShRef("name"), ";", "then", " ", ShRef("suite"), ";"),
	"fi", ";")

ShDef("small_statement",
	Or(
		ShRef("pass_statement"),
		ShRef("print_statement")
	)
)

ShDef("suite", Or(
	ShRef("simple_statement"),
	And(
		NEWLINE, INDENT, PLUS(ShRef("statement")), DEDENT
	)
))

ShDef("pass_statement", ":")
ShDef("print_statement", ":")

