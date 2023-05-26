"""Utility functions to display popup messages and file dialogs, and various functions related to Qt."""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .. import config, constants
from ..i18n import translate as _t


def show_info(message: str, title='popup.info.title', parent: QWidget = None):
    """Show an information popup.

    :param message: Popup’s message.
    :param title: Popup’s unlocalized title.
    :param parent: Popup’s parent.
    """
    # noinspection PyArgumentList
    mb = QMessageBox(QMessageBox.Information, _t(title), message, buttons=QMessageBox.Ok, parent=parent)
    mb.button(QMessageBox.Ok).setText(_t('dialog.common.ok_button.label'))
    mb.exec_()


def show_warning(message: str, title: str = 'popup.warning.title', parent: QWidget = None):
    """Show a warning popup.

    :param message: Popup’s message.
    :param title: Popup’s unlocalized title.
    :param parent: Popup’s parent.
    """
    # noinspection PyArgumentList
    mb = QMessageBox(QMessageBox.Warning, _t(title), message, buttons=QMessageBox.Ok, parent=parent)
    mb.button(QMessageBox.Ok).setText(_t('dialog.common.ok_button.label'))
    mb.exec_()


def show_error(message: str, title: str = 'popup.error.title', parent: QWidget = None):
    """Show an error popup.

    :param message: Popup’s message.
    :param title: Popup’s unlocalized title.
    :param parent: Popup’s parent.
    """
    # noinspection PyArgumentList
    mb = QMessageBox(QMessageBox.Critical, _t(title), message, buttons=QMessageBox.Ok, parent=parent)
    mb.button(QMessageBox.Ok).setText(_t('dialog.common.ok_button.label'))
    mb.exec_()


def show_question(message: str, title: str = 'popup.question.title', cancel: bool = False,
                  parent: QWidget = None) -> bool | None:
    """Show a question popup.

    :param message: Popup’s message.
    :param title: Popup’s unlocalized title.
    :param cancel: If true a "Cancel" button will be added.
    :param parent: Popup’s parent.
    :return: True for yes, False for no or None for cancel.
    """
    answers = {
        QMessageBox.Yes: True,
        QMessageBox.No: False,
        QMessageBox.Cancel: None,
    }
    buttons = QMessageBox.Yes | QMessageBox.No
    if cancel:
        buttons |= QMessageBox.Cancel

    # noinspection PyArgumentList
    mb = QMessageBox(QMessageBox.Question, _t(title), message, buttons=buttons, parent=parent)
    mb.button(QMessageBox.Yes).setText(_t('dialog.common.yes_button.label'))
    mb.button(QMessageBox.No).setText(_t('dialog.common.no_button.label'))
    if cancel:
        mb.button(QMessageBox.Cancel).setText(_t('dialog.common.cancel_button.label'))
    # noinspection PyTypeChecker
    return answers[mb.exec_()]


def show_text_input(message: str, title: str, text: str = '', parent: QWidget = None) -> str | None:
    """Show an input popup.

    :param message: Popup’s message.
    :param title: Popup’s title.
    :param text: Text to show in the input field.
    :param parent: Popup’s parent.
    :return: The typed text or None if the popup was cancelled.
    """
    input_d = QInputDialog(parent=parent)
    input_d.setWindowTitle(title)
    input_d.setLabelText(message)
    input_d.setTextValue(text)
    input_d.setOkButtonText(_t('dialog.common.ok_button.label'))
    input_d.setCancelButtonText(_t('dialog.common.cancel_button.label'))
    ok = input_d.exec_()
    return input_d.textValue() if ok else None


def center(window: QWidget):
    """Center the given window on the screen.

    :param window: The window to center.
    """
    rect = window.frameGeometry()
    rect.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(rect.topLeft())


def icon(icon_name: str, ignore_theme: bool = False) -> QIcon:
    """Return a QIcon for the given icon name.

    :param icon_name: Icon name, without file extension.
    :param ignore_theme: Whether to ignore the active theme.
    :return: The QIcon object.
    """
    dir_ = constants.ICONS_DIR
    if not ignore_theme:
        dir_ /= config.CONFIG.icon_theme.code
    return QIcon(str(dir_ / f'{icon_name}.png'))
