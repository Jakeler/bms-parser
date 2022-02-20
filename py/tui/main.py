import time, datetime, random, sys
# from rich import print
from rich import box
from rich.layout import Layout
from rich.padding import Padding
from rich.console import Group
from rich.align import Align
from rich.progress import Progress, BarColumn, RenderableColumn
from rich.bar import Bar
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

from py.tui.data import Serial

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
        # RenderableColumn(Bar(100, 0, 42, color='green', bgcolor='grey23')),
        "{task.fields[delta]}",
        "{task.fields[flags]}",
    )
    tasks = list(
        progress.add_task('pending', total=_RANGE_VOLT, delta='none', flags=' - ')
        for _ in range(cell_count)
    )
    return (progress, tasks)

def setup_info(info: list[tuple[str, str, str]]):
    table = Table(title='Basic Info', box=box.HORIZONTALS, show_lines=True)

    table.add_column('Title')
    table.add_column('Value')
    table.add_column('Unit')

    for line in info:
        table.add_row(*line)

        # add additional bar visualization
        if '%' in line[2]:
            vis = Bar(100, 0, int(line[1]), color='green', bgcolor='grey23')
            table.add_row(line[0], vis, line[2])

    return table


def setup_window(cells_rndr):
    layout = Layout()
    layout.split_row(
        Layout(name="cells"),
        Layout(name="info"),
    )
    cell_panel = Panel(cells_rndr, title='Cell Voltages')
    layout['cells'].update(cell_panel)

    layout['info'].split_column(
        Layout(name='panel', ratio=8),
        Layout(name='time')
    )

    return layout

def setup_timestamp():
    return Panel(f'Last updated: {datetime.datetime.now()}')


def update_info(info: list):
    layout['info']['panel'].update(setup_info(info))
    layout['info']['time'].update(setup_timestamp())

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
    if len(sys.argv) > 1:
        serial = Serial(sys.argv[1])
    else:
        serial = Serial(None, use_mock=True, mock_fail_rate=0.05)

    # TODO Remove pre setup, only update with table approach
    data = None
    while not data:
        try:
            data = serial.get_cells()
            cell_count = len(data)
            # print(data)
        except Exception as e:
            print(e)

    # fet_info = Panel(str(fet_info))
    # info_group = Group(info, fet_info)

    progress, tasks = setup_cells(cell_count)
    layout = setup_window(progress)

    with Live(layout, refresh_per_second=4):
        while True:
            try:
                table_info, balance_info, fet_info = serial.get_info()
                data = serial.get_cells()
            except Exception as e:
                print(e)
                continue

            update_info(table_info)
            update_cells(data, balance_info)
            time.sleep(0.5)