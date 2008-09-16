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
base.views
"""

from logging import getLogger
import gtk


from . import View


class ToolView(View):
	"""
	"""
	
	_log = getLogger("ToolView")
	
	position = View.POSITION_BOTTOM
	label = "Tools"
	icon = gtk.STOCK_CONVERT
	scope = View.SCOPE_WINDOW
	
	def init(self):
		self._log.debug("init")
	
	def load_tool(self, tool):
		pass
	
	def append_issue(self, job, issue):
		pass
	
	
	