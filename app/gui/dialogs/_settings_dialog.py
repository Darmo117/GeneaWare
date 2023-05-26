import typing as typ

from PyQt5.QtWidgets import *

from . import _dialog_base
from .. import config, i18n
from ..i18n import translate as _t
from ..util import gui

_T = typ.TypeVar('_T', bound='Dialog')


class SettingsDialog(_dialog_base.Dialog):
    """This dialog lets users edit app settings."""

    def __init__(self, parent: QWidget = None):
        self._initial_config = config.CONFIG.copy(replace_by_pending=True)
        super().__init__(parent, _t('dialog.settings.title'), modal=True, resizable=False)
        self._update_ui()

    def _init_body(self) -> QLayout | None:
        layout = QVBoxLayout()

        self._lang_combo = self._add_combo_box(
            layout,
            'language',
            i18n.get_languages(),
            self._initial_config.language,
            lambda lang: (lang.code, lang.name),
            no_i18n=True
        )
        self._theme_combo = self._add_combo_box(
            layout,
            'theme',
            config.get_icon_themes(),
            self._initial_config.icon_theme,
            lambda theme: (theme.code, theme.name),
            no_i18n=True
        )

        body_layout = QVBoxLayout()
        scroll = QScrollArea(parent=self)
        scroll.setWidgetResizable(True)
        w = QWidget(parent=self)
        w.setLayout(layout)
        scroll.setWidget(w)
        # noinspection PyArgumentList
        body_layout.addWidget(scroll)

        return body_layout

    def _add_combo_box(self, layout: QLayout, name: str, options: list[_T], initial_value: _T,
                       option_name_supplier: typ.Callable[[_T], tuple[str, str]],
                       no_i18n: bool = False) -> QComboBox:
        # noinspection PyArgumentList
        box = QGroupBox(_t(f'dialog.settings.box.{name}.title'), parent=self)
        box_layout = QVBoxLayout()
        chooser_layout = QHBoxLayout()
        # noinspection PyArgumentList
        box_layout.addWidget(QLabel(_t(f'dialog.settings.box.{name}.chooser.title'), parent=self))
        combo = QComboBox(parent=self)
        for i, option in enumerate(options):
            option_name, option_label = option_name_supplier(option)
            if no_i18n:
                label = option_label
            else:
                label = _t(f'dialog.settings.box.{name}.chooser.option.{option_name}')
            # noinspection PyArgumentList
            combo.addItem(label, userData=option)
            if option == initial_value:
                combo.setCurrentIndex(i)
        if combo.count() == 1:  # Disable if only one item is available
            combo.setDisabled(True)
        # noinspection PyUnresolvedReferences
        combo.currentIndexChanged.connect(self._update_ui)
        # noinspection PyArgumentList
        chooser_layout.addWidget(combo)
        box_layout.addLayout(chooser_layout)
        box.setLayout(box_layout)
        layout.addWidget(box)
        return combo

    def _init_buttons(self) -> list[QAbstractButton]:
        # noinspection PyArgumentList
        self._apply_button = QPushButton(
            self.style().standardIcon(QStyle.SP_DialogApplyButton),
            _t('dialog.common.apply_button.label'),
            parent=self
        )
        # noinspection PyUnresolvedReferences
        self._apply_button.clicked.connect(self._apply)
        return [self._apply_button]

    def _update_ui(self):
        self._apply_button.setDisabled(not self._settings_changed())

    def _settings_changed(self) -> bool:
        language = self._lang_combo.currentData()
        theme = self._theme_combo.currentData()
        return language != self._initial_config.language or theme != self._initial_config.icon_theme

    def _apply(self) -> bool:
        changed = self._settings_changed()
        language = self._lang_combo.currentData()
        theme = self._theme_combo.currentData()

        needs_restart = False
        if language != self._initial_config.language:
            config.CONFIG.set_language(language)
            needs_restart = True
        if theme != self._initial_config.icon_theme:
            config.CONFIG.set_icon_theme(theme)
            needs_restart = True

        config.CONFIG.save()

        if changed and needs_restart:
            gui.show_info(_t('popup.app_needs_restart.text'), parent=self)

        self._initial_config = config.CONFIG.copy(replace_by_pending=True)
        self._update_ui()

        return super()._apply()
