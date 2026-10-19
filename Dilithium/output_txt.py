"""Human-readable TXT exporter for Python and NumPy data."""
from pathlib import Path
from collections.abc import Mapping
from numbers import Number


def output_txt(data, filename, *, precision=6, line_width=120):
    """Save common Python values or numpy arrays as an easy-to-read UTF-8 TXT file.

    NumPy is optional. For higher-dimensional arrays, indices label each 1-D
    polynomial/vector; 2-D arrays are printed as rows and columns.
    """
    if precision < 0 or line_width < 10:
        raise ValueError("precision must be nonnegative and line_width >= 10")
    try:
        import numpy as np
    except ImportError:
        np = None

    def scalar(value):
        if np is not None and isinstance(value, np.generic):
            value = value.item()
        if isinstance(value, bytes):
            return value.hex(' ')
        if isinstance(value, bytearray):
            return bytes(value).hex(' ')
        if isinstance(value, float):
            return f"{value:.{precision}g}"
        if isinstance(value, (str, bool, Number)) or value is None:
            return str(value)
        return repr(value)

    def wrap_items(values, indent=""):
        parts = [scalar(v) for v in values]
        lines, current = [], indent
        for part in parts:
            candidate = (current + ' ' if current.strip() else current) + part
            if len(candidate) > line_width and current.strip():
                lines.append(current)
                current = indent + part
            else:
                current = candidate
        if current.strip() or not lines:
            lines.append(current)
        return lines

    def render_array(array, prefix=""):
        lines = [f"{prefix}Shape: {array.shape}"]
        if array.ndim == 0:
            lines.append(scalar(array.item()))
        elif array.ndim == 1:
            lines += wrap_items(array)
        elif array.ndim == 2:
            for row in array:
                lines.append(' '.join(scalar(x) for x in row))
        else:
            import itertools
            for idx in itertools.product(*(range(s) for s in array.shape[:-2])):
                lines.append('')
                lines.append('Block [' + ', '.join(map(str, idx)) + ']')
                for row in array[idx]:
                    lines.append(' '.join(scalar(x) for x in row))
        return lines

    def render(value, indent=0):
        pad = ' ' * indent
        if np is not None and isinstance(value, np.ndarray):
            return [pad + line for line in render_array(value)]
        if isinstance(value, Mapping):
            lines = []
            for key, item in value.items():
                if isinstance(item, (Mapping, list, tuple)) or (np is not None and isinstance(item, np.ndarray)):
                    lines.append(f"{pad}{key}:")
                    lines += render(item, indent + 2)
                else:
                    lines.append(f"{pad}{key}: {scalar(item)}")
            return lines or [pad + '{}']
        if isinstance(value, (list, tuple)):
            if np is not None:
                try:
                    arr = np.asarray(value)
                    if arr.dtype != object:
                        return [pad + line for line in render_array(arr)]
                except (ValueError, TypeError):
                    pass
            if all(not isinstance(x, (list, tuple, Mapping)) for x in value):
                return wrap_items(value, pad)
            lines = []
            for i, item in enumerate(value):
                lines.append(f"{pad}[{i}]")
                lines += render(item, indent + 2)
            return lines
        return [pad + scalar(value)]

    target = Path(filename)
    target.parent.mkdir(parents=True, exist_ok=True)
    content = '\n'.join(render(data)) + '\n'
    target.write_text(content, encoding='utf-8')
    return target
