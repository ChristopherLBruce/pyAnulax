"""
Character Tools

**Examples:** ::

	Enter code examples here. (optional field)

**Todo:**

	Enter thing to do. (optional field)

**Author:**

	Chris Bruce, chris.bruce@dsvolition.com, 3/14/2018
"""

import maya.cmds

from . import main, gui
from . import gui_groot



# USE PROJECT RELATIVE FILEPATHS
# FILEPATH = os.path.join( vlib.dcc.python.core.const.workspace_dir, r"data\art\characters\player\player_GEO.ma" )



def reload_all( ):
	"""
	Closes the gui's Main Widget if open. Reloads modules. Re-opens the gui if it had been open before. This is useful for dev. iteration purposes.

	**Arguments:**

		None

	**Keyword_Arguments:**

		None

	**Returns:**

		None

	**Author:**

		Chris Bruce, chris.bruce@dsvolition.com, 12/1/2017
	"""

	# if the gui.window is open, close it before reloading sub-modules so we don't end up with an orphaned window
	if gui.window:
		gui.window.destroy( )

	#reload( const )
	reload( gui )
	reload( main )

	gui.launch_gui( )

	print 'reload_all() complete'


# convenience method for open_gui( )
launch_gui = gui.launch_gui