from __future__ import annotations

import typing as typ

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ..i18n import translate as _t
from ..util import gui

_T = typ.TypeVar('_T', bound='Dialog')


class Dialog(QDialog):
    """Base class for all dialog windows."""
    OK_CANCEL = 0
    CLOSE = 1

    def __init__(self, parent: QWidget = None, title: str = None, modal: bool = True, resizable: bool = True,
                 mode: int = OK_CANCEL):
        """Creates a dialog window.

        :param parent: The widget this dialog is attached to.
        :param title: Dialog’s title.
        :param modal: If true all events to the parent widget will be blocked while this dialog is visible.
        :param resizable: Whether this dialog should be resizable.
        :param mode: Buttons mode. OK_CANCEL will add 'OK' and 'Cancel' buttons; CLOSE will add a single 'Close' button.
        """
        super().__init__(parent)
        # Remove "?" button but keep "close" button.
        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(modal)
        if modal:
            self.setAttribute(Qt.WA_DeleteOnClose)

        self._buttons_mode = mode

        if self._buttons_mode != Dialog.OK_CANCEL and self._buttons_mode != Dialog.CLOSE:
            raise ValueError(f'unknown mode "{self._buttons_mode}"')

        self._close_action = None
        self._applied = False
        # noinspection PyUnresolvedReferences
        self.rejected.connect(self.close)

        if title:
            self.setWindowTitle(title)

        body = QVBoxLayout()
        layout = self._init_body()
        if layout is not None:
            body.addLayout(layout)
        body.addLayout(self.__init_button_box())

        self.setLayout(body)
        if not resizable:
            self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def show(self) -> None:
        super().show()
        gui.center(self)

    def _init_body(self) -> QLayout | None:
        """Initializes this dialog’s body.

        :return: The components to disply in this dialog.
        """
        return None

    def __init_button_box(self) -> QBoxLayout:
        """Initializes the buttons. Additional buttons can be set by overriding the _init_buttons method. These buttons
        will be added in the order they are returned and to the left of default buttons.

        :return: The list of buttons.
        """
        box = QHBoxLayout()
        box.addStretch(1)
        if self._buttons_mode == Dialog.OK_CANCEL:
            icon = QStyle.SP_DialogOkButton
        else:
            icon = QStyle.SP_DialogCloseButton
        # noinspection PyArgumentList
        self._ok_btn = QPushButton(
            self.style().standardIcon(icon),
            _t('dialog.common.ok_button.label') if self._buttons_mode == Dialog.OK_CANCEL
            else _t('dialog.common.close_button.label'),
            parent=self
        )
        # noinspection PyUnresolvedReferences
        self._ok_btn.clicked.connect(self._on_ok_clicked)
        if self._buttons_mode == Dialog.OK_CANCEL:
            # noinspection PyArgumentList
            self._cancel_btn = QPushButton(
                self.style().standardIcon(QStyle.SP_DialogCancelButton),
                _t('dialog.common.cancel_button.label'),
                parent=self
            )
            # noinspection PyUnresolvedReferences
            self._cancel_btn.clicked.connect(self.reject)

        buttons = self._init_buttons()
        for b in buttons:
            # noinspection PyArgumentList
            box.addWidget(b)

        # noinspection PyArgumentList
        box.addWidget(self._ok_btn)
        if self._buttons_mode == Dialog.OK_CANCEL:
            # noinspection PyArgumentList
            box.addWidget(self._cancel_btn)

        return box

    def _init_buttons(self) -> list[QAbstractButton]:
        """Use this method to return additional buttons.

        :return: The list of additional buttons.
        """
        return []

    def set_on_close_action(self, action: typ.Callable[[_T], None]):
        """Sets the action that will be called when this dialog closes after the user clicked OK/Apply or Close.

        :param action: The action to call when this dialog closes.
            The dialog instance will be passed as the single argument.
        """
        self._close_action = action

    def _on_ok_clicked(self):
        """Called when the OK button is clicked. Checks the validity of this dialog and applies changes if possible."""
        if self._buttons_mode == Dialog.CLOSE:
            self.close()
        else:
            if not self._is_valid():
                reason = self._get_error()
                gui.show_error(
                    reason if reason is not None else _t('dialog.common.invalid_data.text'),
                    parent=self
                )
            elif self._apply():
                self.close()

    def _is_valid(self) -> bool:
        """Checks if this dialog’s state is valid. Called when the dialog closes. An invalid state will prevent the
        dialog from closing.

        :return: True if everything is fine; false otherwise.
        """
        return True

    def _get_error(self) -> str | None:
        """Returns the reason data is invalid. If data is valid, None is returned."""
        return None

    def _apply(self) -> bool:
        """Applies changes. Called when the dialog closes and is in a valid state.

        :return: Whether to close this dialog.
        """
        self._applied = True
        return True

    def closeEvent(self, event: QCloseEvent):
        if self._close_action is not None and (self._applied or self._buttons_mode == self.CLOSE):
            self._close_action(self)
