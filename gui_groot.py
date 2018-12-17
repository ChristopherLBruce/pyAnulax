import os
import random
import time
from threading import Thread
import functools

from PySide2 import QtGui, QtWidgets, QtCore

import maya.cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from . import main
import vmaya2.tools.clothing_morpher


# global for storing instance of 'Main_Window' widget created in .launch_gui( )
window				= None



class Main_Window( QtWidgets.QWidget ):
	"""
	Enter a description of the class here.

	**Arguments:**

		:``Argument``:	`arg_type` Enter a description for the argument here.

	**Keyword Arguments:**

		:``Argument``:	`arg_type` Enter a description for the keyword argument here.

	**Examples:** ::

		Enter code examples here. (optional field)

	**Todo:**

		Enter thing to do. (optional field)

	**Author:**

		Chris Bruce, chris.bruce@dsvolition.com, 3/14/2018
	"""

	BIND_TO_JOINTS 	= [ 'Head', 'Chest', 'Hips' ]

	TITLE					= 'Character Setup Tool'
	VERSION				= 1.0
	WINDOW_SIZE			= [ 800, 480 ]
	ICON_SIZE			= [ 96, 96 ]
	FILEPATH_ICONS		= os.path.join( os.path.dirname( __file__ ), 'icons' )

	IMAGE_BACKGROUND		= os.path.join( FILEPATH_ICONS, 'anulax_detonator.png' )
	IMAGE_CLOSE				= os.path.join( FILEPATH_ICONS, 'button_close.png' )
	IMAGE_WIRE_SCREEN		= os.path.join( FILEPATH_ICONS, 'wire_screen.png' )

	BUTTON_CLOSE_SIZE	= [ 24, 24 ]
	BUTTON_CLOSE_POS	= [ 180, 450 ]

	MINUTES				= random.randint( 5, 9 )
	SECONDS				= random.randint( 10, 59 )
	SLEEP_TIME			= 1.0
	TIMER					= QtCore.QTime( 0, MINUTES, s = SECONDS )
	TIMER_SIZE			= [ 305, 120 ]
	TIMER_POS			= [ 30, 250 ]

	SCREEN_SIZE			= [ 305, 120 ]
	SCREEN_POS			= [ 30, 250 ]

	BUTTON_SIZE			= [ 86, 86 ]
	BUTTON_POS1			= [ 425 , 202 ]
	BUTTON_POS2			= [ 557 , 202 ]

	MORPH_BUTTON_SIZE	= [ 160, 48 ]
	MORPH_BUTTON_POS	= [ 320 , 400 ]


	STYLE_SHEET			= '''
	QLCDNumber	{ background-color: rgb( 0, 0, 0, 255 ); color: rgb( 192, 24, 16 ); }
	QPushButton	{ background-color: rgb( 255, 0, 0, 0 ); border-style: outset; border-width: 1px; border-radius: 43px; }
   QPushButton:hover{ background-color: rgb( 255, 0, 0, 16 ); border-style: outset; border-width: 2px; border-radius: 43px; }
	QPushButton#button_dummy_morphs { background-color: rgb( 255, 0, 0, 0 ); color: rgb( 255, 255, 255 ); border-style: outset; border-width: 0px; border-radius: 23px; }
	QPushButton#button_dummy_morphs:hover { background-color: rgb( 255, 0, 0, 32 ); color: rgb( 255, 255, 255 ); border-style: outset; border-width: 0px; border-radius: 23px; }
	'''

	def __init__( self ):
		"""
		Constructor

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 12/7/2017
		"""

		super( Main_Window, self ).__init__()

		self._init_gui( )

		self.timer_thread = Thread( target = self._countdown )
		self.timer_thread.start( )

		self._init_event_handlers( )

		self._update_gui( )


	def _init_gui( self ):
		"""
		Builds widgets and layotus for main window

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 12/7/2017
		"""

		self.setWindowTitle( '{} - v{}'.format( self.TITLE, self.VERSION ) )
		self.setWindowFlags( self.windowFlags( ) | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint )
		self.setAttribute( QtCore.Qt.WA_TranslucentBackground, True )
		self.setFixedSize( *self.WINDOW_SIZE )
		self.setStyleSheet( self.STYLE_SHEET )

		self.background, self.button_close		= self._init_background( )
		self.timer 										= self._init_timer( )
		self.button_bind_char						= self._init_button_bind_char( )
		self.button_bind_clo							= self._init_button_bind_clo( )
		self.button_dummy_morphs					= self._init_widget_dummy_morphs( )

		return True


	def _init_background( self ):
		"""
		Creates background widget and close button

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Returns:**

			:``[type]``: [description]

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		widget = QtWidgets.QLabel( self )

		if os.path.isfile( self.IMAGE_BACKGROUND ):
			pixmap = QtGui.QPixmap( self.IMAGE_BACKGROUND ).scaled( self.size( ), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation )
			widget.setPixmap( pixmap )

		button	= QtWidgets.QPushButton( self )
		button.setFixedSize( QtCore.QSize( *self.BUTTON_CLOSE_SIZE ) )
		button.move( *self.BUTTON_CLOSE_POS )
		button.clicked.connect( self._destroyWindow )

		if os.path.isfile( self.IMAGE_CLOSE ):
			button.setIcon( QtGui.QIcon( self.IMAGE_CLOSE ) )
			button.setIconSize( QtCore.QSize( *self.BUTTON_CLOSE_SIZE ) )

		return widget, button


	def _init_timer( self ):
		"""
		Creates a QLCDNumber widget and wire screen to cover it

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Returns:**

			:``[type]``: [description]

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		timer = QtWidgets.QLCDNumber( self )
		timer.setFixedSize( QtCore.QSize( *self.TIMER_SIZE ) )
		timer.setSegmentStyle( QtWidgets.QLCDNumber.Flat )
		timer.display( self.TIMER.toString( ) )
		timer.move( *self.TIMER_POS )

		label	= QtWidgets.QLabel( self )
		label.setFixedSize( QtCore.QSize( *self.SCREEN_SIZE ) )
		label.setScaledContents( True )
		label.move( *self.SCREEN_POS )

		if os.path.isfile( self.IMAGE_WIRE_SCREEN ):
			image		= QtGui.QImage( self.IMAGE_WIRE_SCREEN )
			pixmap	= QtGui.QPixmap.fromImage( image )
			label.setPixmap( pixmap )

		return timer


	def _init_button_bind_char( self ):
		"""
		Creates the 'bind character' button and right-click menu

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Returns:**

			:``[type]``: [description]

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		button	= QtWidgets.QPushButton( self )
		button.setFixedSize( QtCore.QSize( *self.BUTTON_SIZE ) )
		button.move( *self.BUTTON_POS1 )

		#button.setToolTip( 'Bind and set up export for selected meshes as a "character".\nRight-Click for more options.' )
		button.setToolTip( 'I AM Groot?\n\n[Bind and set up export for selected meshes as a "character".\nRight-Click for more options.]' )
		button.clicked.connect( functools.partial( self._on_bind_clicked, mesh_type = 'character' ) )
		button.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )

		# right-click popmenu for 'bind character' button
		self.menu_bind_char = QtWidgets.QMenu( )
		button.customContextMenuRequested.connect( functools.partial( self._on_button_right_click, pop_menu = self.menu_bind_char, button = button ) )

		self.action_bind_char_default = QtWidgets.QAction( 'Default Weighting', self )
		self.menu_bind_char.addAction( self.action_bind_char_default )
		self.action_bind_char_default.triggered.connect( functools.partial( self._on_bind_clicked, mesh_type = 'character' ) )

		self.action_bind_char_import = QtWidgets.QAction( 'Import Player Weights', self )
		self.menu_bind_char.addAction( self.action_bind_char_import )
		self.action_bind_char_import.triggered.connect( functools.partial( self._on_bind_clicked, mesh_type = 'character', import_weights = True ) )

		return button


	def _init_button_bind_clo( self ):
		"""
		creates widget for 'bind clothing buttons'

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Returns:**

			:``QtWidgets.QGroupBox``: QGroupBox widget

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/2/2018
		"""

		button	= QtWidgets.QPushButton( self )
		button.setFixedSize( QtCore.QSize( *self.BUTTON_SIZE ) )
		button.move( *self.BUTTON_POS2 )

		#button.setToolTip( 'Bind and set up export for selected meshes as "clothing".\nRight-Click for more options.' )
		button.setToolTip( 'I am GROOT!\n\nBind and set up export for selected meshes as "clothing".\nRight-Click for more options.' )
		button.clicked.connect( functools.partial( self._on_bind_clicked, mesh_type = 'clothing' ) )
		button.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )

		# right-click popmenu for 'bind clothing' button
		self.menu_bind_clo = QtWidgets.QMenu( )
		button.customContextMenuRequested.connect( functools.partial( self._on_button_right_click, pop_menu = self.menu_bind_clo, button = button ) )

		self.action_bind_clo_default = QtWidgets.QAction( 'Default Weighting', self )
		self.menu_bind_clo.addAction( self.action_bind_clo_default )
		self.action_bind_clo_default.triggered.connect( functools.partial( self._on_bind_clicked, mesh_type = 'clothing' ) )

		self.action_bind_clo_import = QtWidgets.QAction( 'Import Player Weights', self )
		self.menu_bind_clo.addAction( self.action_bind_clo_import )
		self.action_bind_clo_import.triggered.connect( functools.partial( self._on_bind_clicked, mesh_type = 'clothing', import_weights = True ) )

		self.menu_bind_clo.addSeparator( )

		# set up a popmenu action for each BIND_TO_JOINT
		for joint in self.BIND_TO_JOINTS:
			action = QtWidgets.QAction( 'Bind to {}'.format( joint ), self )
			self.menu_bind_clo.addAction( action )
			action.triggered.connect( functools.partial( self._on_bind_clicked, joint = joint, mesh_type = 'clothing' ) )

		return button


	def _on_button_right_click( self, point, pop_menu = None, button = None ):
		"""
		righ-click popmenu handler

		**Arguments:**

			:``pop_menu``: ` QMenu` The QMenu object to create
			:``button``: `QPushButton` The QPushbutton to map to
			:``point``: Point on button passed in from customContextMenuRequested

		**Keword Arguments:**

			None

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/2/2018
		"""

		pop_menu.exec_( button.mapToGlobal( point ) )


	def _init_widget_dummy_morphs( self ):
		"""
		creates groupbox widget for 'create dummy morphs'

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Returns:**

			:``QtWidgets.QGroupBox``: QGroupBox widget

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/2/2018
		"""

		# widget	= QtWidgets.QGroupBox( 'Morphs:' )
		# widget	= QtWidgets.QWidget( )
		# layout	= QtWidgets.QHBoxLayout( )
		# widget.setLayout( layout )

		button = QtWidgets.QPushButton( 'Create Dummy Morphs', parent = self )
		button.setObjectName( 'button_dummy_morphs' )
		button.clicked.connect( functools.partial( self._on_dummy_morphs_clicked ) )
		button.setToolTip( 'Creates set of empty blendShape targets that mirror player base morphs.' )
		button.setFixedSize( QtCore.QSize( *self.MORPH_BUTTON_SIZE ) )
		button.move( *self.MORPH_BUTTON_POS )

		#layout.addWidget( button )

		return button


	def _countdown( self ):
		"""
		threaded function that handles couting down the timer

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Returns:**

			:``[type]``: [description]

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		max_sec = QtCore.QTime( 0, 0 ).secsTo( self.TIMER )

		for i in range( 0, max_sec ):
			self.timer.display( self.TIMER.addSecs( -i ).toString( ) )

			if i < ( max_sec - 10 ):
				self.SLEEP_TIME *= 0.9825
			else:
				self.SLEEP_TIME = 1.5

			time.sleep( max( self.SLEEP_TIME, 0.0125 ) )

		return self._destroyWindow( )


	def _destroyWindow( self ):
		"""
		function called when timer reaches 0 or close button is pressed

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		self.destroy( )


	def _on_bind_clicked( self, joint = None, mesh_type = 'character', import_weights = False ):
		"""
		on clicked function for bind character/clothing buttons

		**Arguments:**

			None

		**Keword Arguments:**

			:``mesh_type``: `string` Type of mesh being exported. Supported options are 'character' and 'clothing'. Default is 'character'.

		**Returns:**

			:``bool``: True when complete

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/2/2018
		"""

		sel_objs = maya.cmds.ls( selection = True )

		if not sel_objs:
			return None

		print( 'main.setup_character_export( {}, mesh_type = {} )'.format( sel_objs, mesh_type ) )
		return main.setup_character_export( sel_objs, joint = joint, mesh_type = mesh_type, import_weights = import_weights )


	def _on_dummy_morphs_clicked( self ):
		"""
		on clicked function for create dummy morphs button

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Returns:**

		:``bool``: True when complete

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/2/2018
		"""

		sel_objs = maya.cmds.ls( selection = True )

		if not sel_objs:
			return None

		return vmaya2.tools.clothing_morpher.main.create_dummy_morphs( sel_objs[ 0 ] )


	def _init_event_handlers( self ):
		"""
		Creates event handlers for main window

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 12/7/2017
		"""

		pass


	def _update_gui( self ):
		"""
		Updates the main window

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 12/7/2017
		"""

		return True


	def mousePressEvent( self, event ):
		"""
		Overrides mousPressEvent to enable moving the widget around

		**Arguments:**

			:``event``: `[type]` [description]

		**Keword Arguments:**

			None

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		# In the first method, you would do something like this, checking that the right
		# mouse button is pressed and store the screen position of the mouse cursor:
		if event.buttons( ) == QtCore.Qt.LeftButton:
			self.dragPos = event.globalPos( )
			event.accept( )


	def mouseMoveEvent(self, event):
		"""
		Overrides mouseMoveEvent to enable moving the widget around

		**Arguments:**

			:``event``: `[type]` [description]

		**Keword Arguments:**

			None

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		if event.buttons( ) == QtCore.Qt.LeftButton:
			self.move( self.pos( ) + event.globalPos( ) - self.dragPos )
			self.dragPos = event.globalPos( )
			event.accept( )


	def closeEvent( self, event ):
		"""
		Called when widget is closed

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 12/7/2017
		"""

		#OpenMaya.MMessage.removeCallback( self.cb_selection_changed )
		pass



def launch_gui( ):
	"""
	Main function to create a new Main Window object.

	**Arguments:**

		None

	**Keyword Arguments:**

		None

	**Author:**

		Chris Bruce, chris.bruce@dsvolition.com, 12/9/2017
	"""

	global window

	window = Main_Window( )
	window.show( )		# dockable = True