#    Gedit latex plugin
#    Copyright (C) 2011 Ignacio Casal Quinteiro
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os.path
import platform

from gi.repository import GLib, Gedit, GObject, Gio, Gtk
from .resources import Resources

from .config import MENUACTIONS

from .preferences.tools import ToolPreferences
from .tools import ToolAction

class LaTeXAppActivatable(GObject.Object, Gedit.AppActivatable):
    __gtype_name__ = "GeditLaTeXAppActivatable"

    app = GObject.property(type=Gedit.App)
    
    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        if platform.platform() == 'Windows':
            userdir = os.path.expanduser('~/gedit/latex')
        else:
            userdir = os.path.join(GLib.get_user_config_dir(), 'gedit/latex')

        #check if running from srcdir and if so, prefer that for all data files
        me = os.path.realpath(os.path.dirname(__file__))
        if os.path.exists(os.path.join(me, "..", "configure.ac")):
            sysdir = os.path.abspath(os.path.join(me, "..", "data"))
        else:
            sysdir = self.plugin_info.get_data_dir()

        Resources().set_dirs(userdir, sysdir)
        
        #The following is needed to support gedit 3.12 new menu api.
        #It adds menus and shortcuts here.
        #Actions and toolbar construction are still done in windowactivatable.py.
        
        self._tool_preferences = ToolPreferences()
        self._tool_preferences.connect("tools-changed", self._on_tools_changed)
        
        self.add_latex_menu()
        self.add_latex_tools_menu()
        self.init_tools()
        
    def add_latex_menu(self):
        self.menu_ext = self.extend_menu("preferences-section")
        menu = Gio.MenuItem.new(_("LaTeX"))
        container = Gio.Menu.new()
        menu.set_submenu(container)
        self.menu_ext.append_menu_item(menu)
        
        self._icon_factory = Gtk.IconFactory()
        self._icon_factory.add_default()
        
        for clazz in MENUACTIONS:
            action = clazz(icon_factory=self._icon_factory)
            actionlink = "win." + clazz.__name__
            container.append_item(Gio.MenuItem.new(_(action.label), actionlink))
            if action.accelerator is not None:
                self.app.add_accelerator(action.accelerator, actionlink, None)
                
    def add_latex_tools_menu(self):
        menu = Gio.MenuItem.new(_("LaTeX Tools"))
        container = Gio.Menu.new()
        menu.set_submenu(container)
        self.latex_tools_menu = container
        self.menu_ext.append_menu_item(menu)
    
    def init_tools(self):
      
        #the following is copied from windowactivatable.py and modified as necessary
        
        i = 1                    # counting tool actions
        accel_counter = 1        # counting tool actions without custom accel
        for tool in self._tool_preferences.tools:
            # hopefully unique action name
            name = "Tool%sAction" % i

            # create action
            action = ToolAction(tool)
            actionlink = "win." + name
            self.latex_tools_menu.append_item(Gio.MenuItem.new(_(action.label), actionlink))

            accelerator = None
            if tool.accelerator and len(tool.accelerator) > 0:
                key,mods = Gtk.accelerator_parse(tool.accelerator)
                if Gtk.accelerator_valid(key,mods):
                    accelerator = tool.accelerator
            if not accelerator:
                accelerator = "<Ctrl><Alt>%s" % accel_counter
                accel_counter += 1
            self.app.add_accelerator(accelerator, actionlink, None)
            i += 1
            
    def _on_tools_changed(self, tools):
        self.latex_tools_menu.remove_all()
        self.init_tools()
        
# ex:ts=4:et
