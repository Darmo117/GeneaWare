from __future__ import annotations

import configparser
import dataclasses
import json
import pathlib

from . import constants, i18n, logger


class ConfigError(ValueError):
    pass


@dataclasses.dataclass(frozen=True)
class IconTheme:
    code: str
    name: str


class Config:
    def __init__(
            self,
            language: i18n.Language,
            icon_theme: IconTheme,
            debug: bool,
    ):
        """Creates a new configuration object.

        :param language: App’s UI language.
        :param debug: Whether to load the app in debug mode. Set to True if you have issues with file dialogs.
        """
        self._language = language
        self._language_pending = None
        self._icon_theme = icon_theme
        self._icon_theme_pending = None
        self._debug = debug
        self._last_directory = None

    @property
    def language(self) -> i18n.Language:
        return self._language

    @property
    def language_pending(self) -> i18n.Language | None:
        return self._language_pending

    def set_language(self, value: i18n.Language):
        self._language_pending = value

    @property
    def icon_theme(self) -> IconTheme:
        return self._icon_theme

    @property
    def icon_theme_pending(self) -> IconTheme | None:
        return self._icon_theme_pending

    def set_icon_theme(self, value: IconTheme):
        self._icon_theme_pending = value

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def last_directory(self) -> pathlib.Path | None:
        return self._last_directory

    @last_directory.setter
    def last_directory(self, value: pathlib.Path):
        self._last_directory = value

    @property
    def app_needs_restart(self) -> bool:
        """Whether the application needs to be restarted to apply some changes."""
        return self._language_pending is not None

    def copy(self, replace_by_pending: bool = False) -> Config:
        """Returns a copy of this Config object."""
        if not replace_by_pending or not self.language_pending:
            pending_lang = self.language
        else:
            pending_lang = self.language_pending
        if not replace_by_pending or not self.icon_theme_pending:
            pending_theme = self.icon_theme
        else:
            pending_theme = self.icon_theme_pending
        return Config(
            language=pending_lang,
            icon_theme=pending_theme,
            debug=self.debug,
        )

    def save(self):
        """Saves the config to the file specified in app.constants.CONFIG_FILE."""
        parser = _get_settings_parser()
        parser[_APP_SECTION] = {
            _LANG_KEY: (self.language_pending or self.language).code,
            _ICON_THEME_KEY: (self.icon_theme_pending or self.icon_theme).code,
        }

        try:
            with constants.CONFIG_FILE.open(mode='w', encoding='UTF-8') as f:
                parser.write(f)
            return True
        except IOError as e:
            logger.logger.exception(e)
            return False


def _get_settings_parser() -> configparser.ConfigParser:
    parser = configparser.ConfigParser(strict=True)
    parser.add_section(_APP_SECTION)
    return parser


CONFIG: Config

_ICON_THEMES: dict[str, IconTheme] = {}
_NAME_KEY = 'name'

_DEFAULT_LANG_CODE = 'en'

_APP_SECTION = 'App'
_LANG_KEY = 'language'
_ICON_THEME_KEY = 'icon_theme'


def get_icon_themes() -> list[IconTheme]:
    return sorted(_ICON_THEMES.values(), key=lambda theme: theme.code)


def get_icon_theme(code: str) -> IconTheme | None:
    return _ICON_THEMES.get(code)


def load_config(debug: bool):
    """Loads the configuration file specified in app.constants.CONFIG_FILE.
    If the file does not exist, a default config will be returned.

    :raise ConfigError: If an option is missing or has an illegal value.
    """
    global CONFIG

    if not i18n.load_languages():
        raise ConfigError('could not load languages')
    if not _load_icon_themes():
        raise ConfigError('could not load icon themes')

    lang_code = _DEFAULT_LANG_CODE
    icon_theme_code = get_icon_themes()[0].code

    config_file_exists = constants.CONFIG_FILE.is_file()

    if config_file_exists:
        config_parser = _get_settings_parser()
        config_parser.read(constants.CONFIG_FILE)
        try:
            lang_code = config_parser.get(_APP_SECTION, _LANG_KEY, fallback=lang_code)
            icon_theme_code = config_parser.get(_APP_SECTION, _ICON_THEME_KEY, fallback=icon_theme_code)
        except ValueError as e:
            raise ConfigError(e)
        except KeyError as e:
            raise ConfigError(f'missing key {e}')

    language = i18n.get_language(lang_code)
    icon_theme = get_icon_theme(icon_theme_code)
    if not language:
        raise ConfigError(f'invalid language code: {lang_code}')
    if not icon_theme:
        raise ConfigError(f'invalid icon theme: {icon_theme_code}')

    CONFIG = Config(language, icon_theme, debug)

    if not config_file_exists:
        CONFIG.save()


def _load_icon_theme(theme_file: pathlib.Path):
    try:
        with theme_file.open(mode='r', encoding='UTF-8') as f:
            data = json.load(f)
    except IOError:
        pass
    if _NAME_KEY in data:
        code = theme_file.parent.name
        _ICON_THEMES[code] = IconTheme(code, data[_NAME_KEY])


def _load_icon_themes() -> bool:
    for directory in constants.ICONS_DIR.glob('*'):
        if directory.is_dir():
            theme_file = directory / 'theme.json'
            if theme_file.exists():
                _load_icon_theme(theme_file)
    return len(_ICON_THEMES) != 0
