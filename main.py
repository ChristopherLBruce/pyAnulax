import sys
from PyQt5.QtWidgets import QApplication
from PyAnulax import gui



if __name__ == '__main__':
	app		= QApplication( sys.argv )
	window	= gui.create( )

	sys.exit( app.exec_( ) )
