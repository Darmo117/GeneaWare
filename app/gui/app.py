import argparse
import ctypes
import datetime
import os
import sys
import traceback

from PyQt5.QtWidgets import *

from . import config, constants, dialogs, logger, canvas
from .i18n import translate as _t
from .util import gui


class Application(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self._init_ui()
        gui.center(self)

    def _init_ui(self):
        self.setWindowTitle(constants.APP_NAME + ('*' * config.CONFIG.debug))
        self.setWindowIcon(gui.icon('app-icon', ignore_theme=True))
        self.setGeometry(0, 0, 800, 600)
        self.setMinimumSize(400, 200)
        self.setAcceptDrops(True)

        main_widget = QWidget(parent=self)
        main_layout = QHBoxLayout()
        self._canvas = canvas.Canvas(parent=self)
        # noinspection PyArgumentList
        main_layout.addWidget(self._canvas)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self._init_menu()

    def _init_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu(_t('main_window.menu.file.label'))
        file_menu.addAction(
            gui.icon('open-file'),
            _t('main_window.menu.file.item.open_tree'),
            self._open_tree_file,
            'Ctrl+O'
        )
        file_menu.addAction(
            gui.icon('save'),
            _t('main_window.menu.file.item.save_tree'),
            self._save_tree,
            'Ctrl+S'
        )
        file_menu.addAction(
            gui.icon('save-as'),
            _t('main_window.menu.file.item.save_as_tree'),
            self._save_tree_as,
            'Ctrl+Shift+S'
        )
        file_menu.addSeparator()
        file_menu.addAction(
            gui.icon('exit'),
            _t('main_window.menu.file.item.exit'),
            self.quit,
            'Ctrl+Q'
        )

        edit_menu = menubar.addMenu(_t('main_window.menu.edit.label'))
        edit_menu.addAction(
            gui.icon('person-add'),
            _t('main_window.menu.edit.item.add_person'),
            self._add_person,
            'Ctrl+P'
        )
        edit_menu.addAction(
            gui.icon('person-edit'),
            _t('main_window.menu.edit.item.edit_person'),
            self._edit_person,
            'Ctrl+E'
        )
        edit_menu.addAction(
            gui.icon('person-remove'),
            _t('main_window.menu.edit.item.delete_person'),
            self._delete_person,
            'Del'
        )

        tools_menu = menubar.addMenu(_t('main_window.menu.tools.label'))
        tools_menu.addAction(
            gui.icon('check-inconsistencies'),
            _t('main_window.menu.tools.item.check_inconsistencies'),
            self._check_inconsistencies,
            'Ctrl+I'
        )
        tools_menu.addAction(
            gui.icon('terminal'),
            _t('main_window.menu.tools.item.sparql_terminal'),
            self._open_sparql_terminal,
            'Ctrl+T'
        )

        help_menu = menubar.addMenu(_t('main_window.menu.help.label'))
        help_menu.addAction(
            gui.icon('settings'),
            _t('main_window.menu.help.item.settings'),
            self._show_settings_dialog,
            'Ctrl+Alt+S'
        )
        help_menu.addAction(
            gui.icon('about-app'),
            _t('main_window.menu.help.item.about'),
            self._show_about_dialog
        )

    def _open_tree_file(self):
        pass  # TODO

    def _save_tree(self):
        pass  # TODO

    def _save_tree_as(self):
        pass  # TODO

    def _add_person(self):
        pass  # TODO

    def _edit_person(self):
        pass  # TODO

    def _delete_person(self):
        pass  # TODO

    def _check_inconsistencies(self):
        pass  # TODO

    def _open_sparql_terminal(self):
        pass  # TODO

    def _show_settings_dialog(self):
        dialogs.SettingsDialog(parent=self).show()

    def _show_about_dialog(self):
        dialogs.AboutDialog(parent=self).show()

    def quit(self):
        qApp.quit()

    @classmethod
    def run(cls) -> int:
        """Run an instance of this Application class."""
        print(f'Running GeneaWare v{constants.APP_VERSION}')
        try:
            if os.name == 'nt':
                # Arbitrary string to display app icon in the taskbar on Windows
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('geneaware')
            parser = argparse.ArgumentParser()
            parser.add_argument('-d', '--debug', action='store_true', help='Run the app in debug mode')
            parsed_args = parser.parse_args(sys.argv[1:])

            config.load_config(parsed_args.debug)
            app = QApplication(sys.argv)
            window = cls()  # Must use variable to avoid object being garbage-collected
            window.show()
            return app.exec_()
        except SystemExit:
            raise
        except BaseException as e:
            logger.logger.error(cls._generate_crash_report(e))
            return 2

    @classmethod
    def _generate_crash_report(cls, e: BaseException) -> str:
        tb = ''.join(traceback.format_tb(e.__traceback__))
        date = datetime.datetime.now()
        message = f"""\
--- {constants.APP_NAME} (v{constants.APP_VERSION}) Crash Report ---

Time: {date.strftime("%Y-%m-%d %H:%M:%S")}
Description: {e} 

{e.__class__.__name__}: {e}
{tb}
"""
        if not constants.LOGS_DIR.exists():
            constants.LOGS_DIR.mkdir(parents=True)
        crash_date = date.strftime('%Y-%m-%d_%H.%M.%S')
        with (constants.LOGS_DIR / f'crash_report_{crash_date}.log').open(mode='w', encoding='UTF-8') as f:
            f.write(message)
        return message
