import logging
import sys

from PyQt6.QtWidgets import QApplication

from poseable.gui.main_window import PoseableMainWindow

logger = logging.getLogger(__name__)

def run_gui_main():
    app = QApplication(sys.argv)

    main_window = PoseableMainWindow()
    main_window.show()
    error_code = app.exec()

    logger.info(f"Exiting with code: {error_code}")
    print("Thanks for using Poseable!")
    sys.exit()


if __name__ == "__main__":
    run_gui_main()