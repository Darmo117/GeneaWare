from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyperclip

from . import _dialog_base
from .. import constants
from ..i18n import translate as _t
from ..util import gui


class AboutDialog(_dialog_base.Dialog):
    """This dialog shows information about the application."""

    def __init__(self, parent: QWidget = None):
        """Create the 'About' dialog.

        :param parent: The widget this dialog is attached to.
        """
        super().__init__(
            parent=parent,
            title=_t('dialog.about.title', app_name=constants.APP_NAME),
            modal=True,
            mode=_dialog_base.Dialog.CLOSE,
            resizable=False
        )

    def _init_body(self) -> QLayout:
        body = QHBoxLayout()

        icon_layout = QVBoxLayout()
        icon = gui.icon('app-icon', ignore_theme=True)
        # noinspection PyArgumentList
        label = QLabel(parent=self)
        label.setPixmap(icon.pixmap(QSize(64, 64)))
        # noinspection PyArgumentList
        icon_layout.addWidget(label)
        icon_layout.addStretch()
        body.addLayout(icon_layout)

        # noinspection PyArgumentList
        self._label = QLabel(parent=self)
        self._label.setText(f"""
        <html lang="en" style="font-size: 12px">
            <h1>{constants.APP_NAME} v{constants.APP_VERSION}</h1>
            <p>Made by Damia Vergnet (<a href="https://github.com/Darmo117">@Darmo117</a> on GitHub).</p>
            <p>Published under GPLv3 licence.</p>
            <p>
                <a href="https://fonts.google.com/icons?icon.set=Material+Icons">Material Icons</a>
                from <a href="https://fonts.google.com/">Google Fonts</a>.
            </p>
            <p>Find more on <a href="https://github.com/Darmo117/GeneaWare">GitHub</a>.</p>
        </html>
        """.strip())
        self._label.setOpenExternalLinks(True)
        self._label.setContextMenuPolicy(Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self._label.customContextMenuRequested.connect(self._link_context_menu)
        # noinspection PyUnresolvedReferences
        self._label.linkHovered.connect(self._update_current_link)
        # noinspection PyArgumentList
        body.addWidget(self._label)
        self._current_link = None

        # noinspection PyArgumentList
        self._label_menu = QMenu(parent=self._label)
        self._label_menu.addAction(_t('dialog.about.menu.copy_link_item'))
        # noinspection PyUnresolvedReferences
        self._label_menu.triggered.connect(lambda: pyperclip.copy(self._current_link))

        return body

    def _update_current_link(self, url: str):
        self._current_link = url

    def _link_context_menu(self, pos: QPoint):
        if self._current_link:
            self._label_menu.exec_(self._label.mapToGlobal(pos))
