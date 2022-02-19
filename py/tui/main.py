import time, datetime, random
from rich import print
from rich import box
from rich.layout import Layout
from rich.padding import Padding
from rich.console import Group
from rich.align import Align
from rich.progress import Progress, BarColumn
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

from py.tui.data import get_cells, get_info

MIN_VOLT = 3.5
MAX_VOLT = 4.2
_RANGE_VOLT = MAX_VOLT - MIN_VOLT

class Flags:
    high = '[on dark_green] :arrow_heading_up: '
    low = '[on dark_red] :arrow_heading_down: '
    balancing = ' :yin_yang: '
    placeholder = '   '

    def gen(is_max: bool, is_min: bool):
        flags = Flags.placeholder
        flags = Flags.high if is_max else flags
        flags = Flags.low if is_min else flags
        return flags

def setup_cells(cell_count: int):
    progress = Progress(
        "[progress.description]{task.description}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        BarColumn(),
        "{task.fields[delta]}",
        "{task.fields[flags]}",
    )
    tasks = list(
        progress.add_task('pending', total=_RANGE_VOLT, delta='none', flags=' - ')
        for _ in range(cell_count)
    )
    return (progress, tasks)

def setup_info(info: list):
    table = Table(title='Basic Info', box=box.HORIZONTALS, show_lines=True)

    table.add_column('Title')
    table.add_column('Value')
    table.add_column('Unit')

    for line in info:
        table.add_row(*line)

    return table


def setup_window(cells_rndr, info_rndr):
    layout = Layout()
    layout.split_row(
        Layout(name="cells"),
        Layout(name="info"),
    )
    cell_panel = Panel(cells_rndr, title='Cell Voltages')
    layout['cells'].update(cell_panel)

    info_panel = info_rndr
    # layout['info'].update(info_panel)
    layout['info'].split_column(
        Layout(info_panel, ratio=8),
        Layout(setup_timestamp())
    )

    return layout

def setup_timestamp():
    return Panel(f'Last updated: {datetime.datetime.now()}')

def update_cells(data: list, balancing: list):
    avg = sum(data)/len(data)
    low = min(data)
    high = max(data)
    for i in tasks:
        val = data[i]
        progress.update(i, 
            completed=val-MIN_VOLT, 
            description=f"{val:.2f} V", 
            delta=f'{Flags.gen(val == high, val == low)}{(val-avg)*1000: 04.0f} mV',
            flags=Flags.balancing if balancing[i] else Flags.placeholder
        )


if __name__ == '__main__':
    data = get_cells()
    cell_count = len(data)
    # print(data)

    table_info, balance_info, fet_info = get_info()
    info = setup_info(table_info)
    fet_info = Panel(str(fet_info))
    info_group = Group(info, fet_info)

    progress, tasks = setup_cells(cell_count)
    layout = setup_window(progress, info_group)

    with Live(layout, refresh_per_second=5):
        while True:
            # data = [3.6+random.random()/10 for _ in range(cell_count)]
            data = get_cells()
            update_cells(data, balance_info)
            time.sleep(0.5)