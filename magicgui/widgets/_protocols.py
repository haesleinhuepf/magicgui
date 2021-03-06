"""Protocols (Interfaces) for backends to implement.

These protocols define the methods that a backend must implement
to be compatible with the magicgui API.  All magicgui-specific
abstract methods are prefaced with `_mgui_`

└── -> WidgetProtocol/
    ├── _mgui_show_widget
    ├── _mgui_hide_widget
    ├── _mgui_get_native_widget
    ├── ↪ ValueWidgetProtocol/
    │   ├── _mgui_get_value
    │   ├── _mgui_set_value
    │   ├── _mgui_bind_change_callback
    │   ├── ↪ ButtonWidgetProtocol (+ SupportsText)/
    │   │   ├── _mgui_get_text
    │   │   └── _mgui_set_text
    │   ├── ↪ RangedWidgetProtocol/
    │   │   ├── _mgui_get_minimum
    │   │   ├── _mgui_set_minimum
    │   │   ├── _mgui_get_maximum
    │   │   ├── _mgui_set_maximum
    │   │   ├── _mgui_get_step
    │   │   ├── _mgui_set_step
    │   │   └── ↪ SliderWidgetProtocol (+ SupportsOrientation)/
    │   │       ├── _mgui_get_orientation
    │   │       └── _mgui_set_orientation
    │   └── ↪ CategoricalWidgetProtocol/
    │       ├── _mgui_get_choices
    │       └── _mgui_set_choices
    └── ↪ ContainerProtocol (+ SupportsOrientation)/
        ├── _mgui_add_widget
        ├── _mgui_insert_widget
        ├── _mgui_remove_widget
        ├── _mgui_remove_index
        ├── _mgui_count
        ├── _mgui_index
        ├── _mgui_get_index
        └── _mgui_get_native_layout


-> SupportsText  # different than "value"
     - _mgui_get_text
     - _mgui_set_text


-> SupportsOrientation
     - _mgui_get_orientation
     - _mgui_set_orientation

"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Iterable, Optional, Tuple

from typing_extensions import Protocol, runtime_checkable

if TYPE_CHECKING:
    from magicgui.widgets._bases import Widget


@runtime_checkable
class WidgetProtocol(Protocol):
    """All must have show/hide and return the native widget."""

    @abstractmethod
    def _mgui_show_widget(self):
        """Show the widget."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_hide_widget(self):
        """Hide the widget."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_enabled(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _mgui_set_enabled(self, enabled: bool):
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_parent(self) -> Widget:
        raise NotImplementedError()

    @abstractmethod
    def _mgui_set_parent(self, widget: Widget):
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_native_widget(self):
        raise NotImplementedError()

    @abstractmethod
    def _mgui_bind_parent_change_callback(self, callback: Callable[[Any], None]):
        """Bind callback to parent change event."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_render(self):
        """Return an RGBA (MxNx4) numpy array bitmap of the rendered widget."""
        raise NotImplementedError()


@runtime_checkable
class ValueWidgetProtocol(WidgetProtocol, Protocol):
    """Widget that has a current value, with getter/setter and on_change callback."""

    @abstractmethod
    def _mgui_get_value(self) -> Any:
        """Get current value of the widget."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_set_value(self, value) -> None:
        """Set current value of the widget."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_bind_change_callback(self, callback: Callable[[Any], None]):
        """Bind callback to value change event."""
        raise NotImplementedError()


# note that "float" type hints also accept ints
# https://www.python.org/dev/peps/pep-0484/#the-numeric-tower
@runtime_checkable
class RangedWidgetProtocol(ValueWidgetProtocol, Protocol):
    """Value widget that supports numbers within a provided min/max range."""

    @abstractmethod
    def _mgui_get_minimum(self) -> float:
        """Get the minimum possible value."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_set_minimum(self, value: float):
        """Set the minimum possible value."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_maximum(self) -> float:
        """Get the maximum possible value."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_set_maximum(self, value: float):
        """Set the maximum possible value."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_step(self) -> float:
        """Get the step size."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_set_step(self, value: float):
        """Set the step size."""
        raise NotImplementedError()


@runtime_checkable
class SupportsChoices(Protocol):
    """Widget that has a set of valid choices."""

    @abstractmethod
    def _mgui_get_choices(self) -> Tuple[Tuple[str, Any]]:
        """Get available choices."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_set_choices(self, choices: Iterable[Tuple[str, Any]]):
        """Set available choices."""
        raise NotImplementedError()


@runtime_checkable
class CategoricalWidgetProtocol(ValueWidgetProtocol, SupportsChoices, Protocol):
    """Categorical widget, that has a set of valid choices, and a current value."""

    pass


@runtime_checkable
class SupportsText(Protocol):
    """Widget that have text (in addition to value)... like buttons."""

    @abstractmethod
    def _mgui_set_text(self, value: str) -> None:
        """Set text."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_text(self) -> str:
        """Get text."""
        raise NotImplementedError()


@runtime_checkable
class ButtonWidgetProtocol(ValueWidgetProtocol, SupportsText, Protocol):
    """The "value" in a ButtonWidget is the current (checked) state."""


@runtime_checkable
class SupportsOrientation(Protocol):
    """Widget that can be reoriented."""

    @property
    def orientation(self):
        """Orientation of the widget."""
        return self._mgui_get_orientation()

    @orientation.setter
    def orientation(self, value):
        if value not in {"horizontal", "vertical"}:
            raise ValueError(
                "Only horizontal and vertical orientation are currently supported"
            )
        self._mgui_set_orientation(value)

    @abstractmethod
    def _mgui_set_orientation(self, value) -> None:
        """Set orientation, value will be 'horizontal' or 'vertical'."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_orientation(self) -> str:
        """Get orientation, return either 'horizontal' or 'vertical'."""
        raise NotImplementedError()


@runtime_checkable
class SliderWidgetProtocol(RangedWidgetProtocol, SupportsOrientation, Protocol):
    """Protocol for implementing a slider widget."""


# CONTAINER ----------------------------------------------------------------------


class ContainerProtocol(WidgetProtocol, SupportsOrientation, Protocol):
    """Widget that can contain other widgets."""

    @abstractmethod
    def _mgui_add_widget(self, widget: "Widget"):
        raise NotImplementedError()

    @abstractmethod
    def _mgui_insert_widget(self, position: int, widget: "Widget"):
        raise NotImplementedError()

    @abstractmethod
    def _mgui_remove_widget(self, widget: "Widget"):
        raise NotImplementedError()

    @abstractmethod
    def _mgui_remove_index(self, position: int):
        raise NotImplementedError()

    @abstractmethod
    def _mgui_count(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def _mgui_index(self, widget: "Widget") -> int:
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_index(self, index: int) -> Optional[Widget]:
        """(return None instead of index error)."""
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_native_layout(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def _mgui_get_margins(self) -> Tuple[int, int, int, int]:
        raise NotImplementedError()

    @abstractmethod
    def _mgui_set_margins(self, margins: Tuple[int, int, int, int]) -> None:
        raise NotImplementedError()


# APPLICATION --------------------------------------------------------------------


class BaseApplicationBackend(ABC):
    """Backend Application object.

    Abstract class that provides an interface between backends and Application.
    Each backend must implement a subclass of BaseApplicationBackend, and
    implement all its _mgui_xxx methods.
    """

    @abstractmethod
    def _mgui_get_backend_name(self) -> str:
        """Return the name of the backend."""

    @abstractmethod
    def _mgui_process_events(self):
        """Process all pending GUI events."""

    @abstractmethod
    def _mgui_run(self):
        """Start the application."""

    @abstractmethod
    def _mgui_quit(self):
        """Quit the native GUI event loop."""

    @abstractmethod
    def _mgui_get_native_app(self):
        """Return the native GUI application instance."""

    @abstractmethod
    def _mgui_start_timer(
        self,
        interval: int = 0,
        on_timeout: Optional[Callable[[], None]] = None,
        single: bool = False,
    ):
        """Create and start a timer.

        Parameters
        ----------
        interval : int, optional
            Interval between timeouts, by default 0
        on_timeout : Optional[Callable[[], None]], optional
            Function to call when timer finishes, by default None
        single : bool, optional
            Whether the timer should only fire once, by default False
        """

    @abstractmethod
    def _mgui_stop_timer(self):
        """Stop timer.  Should check for the existence of the timer."""
