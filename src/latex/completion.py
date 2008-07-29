# -*- coding: utf-8 -*-

# This file is part of the Gedit LaTeX Plugin
#
# Copyright (C) 2008 Michael Zeising
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public Licence as published by the Free Software
# Foundation; either version 2 of the Licence, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence for more 
# details.
#
# You should have received a copy of the GNU General Public Licence along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA

"""
latex.completion

LaTeX-specific completion classes
"""

from logging import getLogger

from ..base.interface import ICompletionHandler, IProposal, Template


class LaTeXTemplateProposal(IProposal):
	
	def __init__(self, template, label):
		self._template = template
		self._label = label
	
	@property
	def source(self):
		return self._template
	
	@property
	def label(self):
		return self._label
	
	@property
	def details(self):
		return None
	
	@property
	def overlap(self):
		return 0
	

class LaTeXProposal(IProposal):
	
	def __init__(self, source):
		self._source = source
	
	@property
	def source(self):
		return self._source
	
	@property
	def label(self):
		return self._source
	
	@property
	def details(self):
		return None
	
	@property
	def overlap(self):
		return 0
		

class LaTeXCompletionHandler(ICompletionHandler):
	"""
	"""
	
	_log = getLogger("LaTeXCompletionHandler")
	
	@property
	def trigger_keys(self):
		return ["backslash", "braceleft"]
	
	@property
	def prefix_delimiters(self):
		return ["\\"]
	
	@property
	def strip_delimiter(self):
		return False
	
	def complete(self, prefix):
		self._log.debug("complete(%s)" % prefix)
		
		proposals = [LaTeXTemplateProposal(Template("Hello[${One}][${Two}][${Three}]"), "Hello[Some]"), LaTeXProposal("\\world")]
		
		return proposals
	
	