"""PyQt widget for simple 2-button GUI that replicates the anulax detonator from
Guardians of the Galaxy 2

"""

import sys
import os
import random
import time
from threading import Thread
import functools

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLCDNumber
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import QSize, QTime, Qt

from PyQt5.QtMultimedia import QSound


class Main_Window( QWidget ):
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

	TITLE					= 'Anulax Detonator'
	VERSION				= 1.0
	WINDOW_SIZE			= [ 800, 480 ]
	ICON_SIZE			= [ 96, 96 ]

	FILEPATH_ICONS		= os.path.join( os.path.dirname( __file__ ), 'images' )
	IMAGE_BACKGROUND	= os.path.join( FILEPATH_ICONS, 'anulax_detonator.png' )
	IMAGE_CLOSE			= os.path.join( FILEPATH_ICONS, 'button_close.png' )
	IMAGE_WIRE_SCREEN	= os.path.join( FILEPATH_ICONS, 'wire_screen.png' )

	FILEPATH_SOUNDS	= os.path.join( os.path.dirname( __file__ ), 'sounds' )
	SOUND_BEEP			= os.path.join( FILEPATH_SOUNDS, 'beep-08b.wav' )

	BUTTON_CLOSE_SIZE	= [ 24, 24 ]
	BUTTON_CLOSE_POS	= [ 180, 450 ]

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
	'''

	def __init__( self ):
		"""
		Constructor

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 12/7/2017
		"""

		super( Main_Window, self ).__init__()

		self._init_gui( )
		self._init_event_handlers( )

		self._update_gui( )

		self.start_countdown( )


	def _init_gui( self ):
		"""
		Builds widgets and layotus for main window

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 12/7/2017
		"""

		self.setWindowTitle( '{} - v{}'.format( self.TITLE, self.VERSION ) )
		self.setWindowFlags( self.windowFlags( ) | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint )
		self.setAttribute( Qt.WA_TranslucentBackground, True )
		self.setFixedSize( *self.WINDOW_SIZE )
		self.setStyleSheet( self.STYLE_SHEET )

		self.background, self.button_close	= self._init_background( )
		self.timer 									= self._init_timer( )
		self.button1								= self._init_button1( )
		self.button2								= self._init_button2( )

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

		widget = QLabel( self )

		if os.path.isfile( self.IMAGE_BACKGROUND ):
			pixmap = QPixmap( self.IMAGE_BACKGROUND ).scaled( self.size( ),
											Qt.IgnoreAspectRatio, Qt.SmoothTransformation )
			widget.setPixmap( pixmap )

		button	= QPushButton( self )
		button.setFixedSize( QSize( *self.BUTTON_CLOSE_SIZE ) )
		button.move( *self.BUTTON_CLOSE_POS )
		button.clicked.connect( self._destroyWindow )

		if os.path.isfile( self.IMAGE_CLOSE ):
			button.setIcon( QIcon( self.IMAGE_CLOSE ) )
			button.setIconSize( QSize( *self.BUTTON_CLOSE_SIZE ) )

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

		self.minutes		= random.randint( 5, 9 )
		self.seconds		= random.randint( 10, 59 )
		self.sleep_time	= 1.0
		self.time			= QTime( 0, self.minutes, second = self.seconds )

		self.beep			= QSound( self.SOUND_BEEP )

		timer = QLCDNumber( self )
		timer.setFixedSize( QSize( *self.TIMER_SIZE ) )
		timer.setSegmentStyle( QLCDNumber.Flat )
		timer.display( self.time.toString( ) )
		timer.move( *self.TIMER_POS )

		label	= QLabel( self )
		label.setFixedSize( QSize( *self.SCREEN_SIZE ) )
		label.setScaledContents( True )
		label.move( *self.SCREEN_POS )

		if os.path.isfile( self.IMAGE_WIRE_SCREEN ):
			image		= QImage( self.IMAGE_WIRE_SCREEN )
			pixmap	= QPixmap.fromImage( image )
			label.setPixmap( pixmap )

		return timer


	def _init_button1( self ):
		"""
		Creates the left button

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Returns:**

			:``[type]``: [description]

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		button	= QPushButton( self )
		button.setFixedSize( QSize( *self.BUTTON_SIZE ) )
		button.move( *self.BUTTON_POS1 )

		button.setToolTip( 'Tooltip for button 1' )
		button.clicked.connect( functools.partial( self._on_button1_clicked ) )

		return button


	def _init_button2( self ):
		"""
		creates widget for 'bind clothing buttons'

		**Arguments:**

			None

		**Keword Arguments:**

			None

		**Returns:**

			:``QGroupBox``: QGroupBox widget

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/2/2018
		"""

		button	= QPushButton( self )
		button.setFixedSize( QSize( *self.BUTTON_SIZE ) )
		button.move( *self.BUTTON_POS2 )

		button.setToolTip( 'Tooltip for button 2' )
		button.clicked.connect( functools.partial( self._on_button2_clicked ) )

		return button


	def start_countdown( self ):
		self.timer_thread = Thread( target = self._countdown )
		self.timer_thread.start( )


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

		max_sec = QTime( 0, 0 ).secsTo( self.time )

		for i in range( 0, max_sec ):
			self.timer.display( self.time.addSecs( -i ).toString( ) )
			# TODO: QObject::startTimer: Timers can only be used with threads started with QThread
			# self.beep.play( )

			if i < ( max_sec - 10 ):
				self.sleep_time *= 0.9825
			else:
				self.sleep_time = 1.5

			time.sleep( max( self.sleep_time, 0.0125 ) )

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


	def _on_button1_clicked( self ):
		"""
		on clicked function for bind character/clothing buttons

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/2/2018
		"""

		print( 'Button 1 was pressed!' )

		return True


	def _on_button2_clicked( self ):
		"""
		on clicked function for bind character/clothing buttons

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/2/2018
		"""

		print( 'Button 2 was pressed!' )

		return True


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

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		# In the first method, you would do something like this, checking that the right
		# mouse button is pressed and store the screen position of the mouse cursor:
		if event.buttons( ) == Qt.LeftButton:
			self.dragPos = event.globalPos( )
			event.accept( )


	def mouseMoveEvent(self, event):
		"""
		Overrides mouseMoveEvent to enable moving the widget around

		**Arguments:**

			:``event``: `[type]` [description]

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 11/19/2018
		"""

		if event.buttons( ) == Qt.LeftButton:
			self.move( self.pos( ) + event.globalPos( ) - self.dragPos )
			self.dragPos = event.globalPos( )
			event.accept( )


	def closeEvent( self, event ):
		"""
		Called when widget is closed

		**Author:**

			Chris Bruce, chris.bruce@dsvolition.com, 12/7/2017
		"""

		pass



def create( ):
	"""
	Main function to create a new Main Window object.

	**Author:**

		Chris Bruce, chris.bruce@dsvolition.com, 12/9/2017
	"""

	window = Main_Window( )
	window.show( )

	return window


if __name__ == 'main':
	app		= QApplication( sys.argv )
	window	= create( )

	sys.exit( app.exec_( ) )
