import time, datetime, random, sys
from rich import print
from rich import box
from rich.layout import Layout
from rich.bar import Bar
from rich.columns import Columns
from rich.spinner import Spinner
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

from py.tui.data import Serial

MIN_VOLT = 3.5
MAX_VOLT = 4.2
_RANGE_VOLT = MAX_VOLT - MIN_VOLT
DELTA_LOW = 0.001

class Flags:
    high = '[on dark_green]:arrow_heading_up: '
    low = '[on dark_red]:arrow_heading_down: '
    delta_low = '[bright_black]'
    balancing = ' :yin_yang:'
    placeholder = '  '

    def gen_delta(is_max: bool, is_min: bool, delta_small: bool):
        flags = Flags.placeholder
        flags = Flags.high if is_max else flags
        flags = Flags.low if is_min else flags
        flags = Flags.delta_low + flags if delta_small else flags
        return flags

def setup_cells(data: list[float], balancing: list[bool]):
    table = Table(show_lines=True, box=box.SIMPLE)

    table.add_column('n', style='bright_black')
    table.add_column('Volt')
    table.add_column('%', style='magenta')
    table.add_column('')
    table.add_column('Delta')
    table.add_column('Bal.')

    avg = sum(data)/len(data)
    low = min(data)
    high = max(data)
    for i, val in enumerate(data):
        progress = val-MIN_VOLT
        percent = progress/_RANGE_VOLT
        delta = val-avg

        row = dict(
            index=f'{i+1}.',
            voltage=f"{val:.2f} V",
            percent=f'{percent*100:.0f}%',
            progress=Bar(_RANGE_VOLT, 0, progress, color='cyan', bgcolor='grey23'),
            delta=f'{Flags.gen_delta(val == high, val == low, abs(delta) < DELTA_LOW)}{delta*1000: 04.0f} mV',
            flags=Flags.balancing if balancing[i] else Flags.placeholder
        )
        table.add_row(*row.values())

    return table

def setup_info(info: list[tuple[str, str, str]]):
    table = Table(title='Basic Info', box=box.MINIMAL, show_lines=True)

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


def setup_window():
    layout = Layout()
    layout.split_row(
        Layout(name="cells"),
        Layout(name="info"),
    )

    layout['info'].split_column(
        Layout(name='panel', ratio=9),
        Layout(name='fet'),
        Layout(name='prot', ratio=3),
        Layout(name='time'),
    )

    return layout

def setup_timestamp():
    spin = Spinner('dots', text=f'{datetime.datetime.now()}', speed=2, style='bright_magenta')
    return Panel(spin, title='Last updated', box=box.SQUARE)

def setup_fets(fets: dict):
    content = Columns([f'{k} = {v}' for k, v in fets.items()], expand=True)
    return Panel(content, title='FET status', box=box.SQUARE)

def setup_prot(prot: dict[str, bool]):
    content = Columns([f'{k}={v}' for k, v in prot.items()], expand=True)
    return Panel(content, title='Protection', box=box.SQUARE)

def update_info(info: list, fets: dict, prot: dict):
    layout['info']['panel'].update(setup_info(info))
    layout['info']['fet'].update(setup_fets(fets))
    layout['info']['prot'].update(setup_prot(prot))
    layout['info']['time'].update(setup_timestamp())

def update_cells(data: list[float], balancing: list[bool]):
    cell_panel = Panel(setup_cells(data, balancing), title='Cell Voltages', box=box.SQUARE)
    layout['cells'].update(cell_panel)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        serial = Serial(sys.argv[1])
    else:
        serial = Serial(None, use_mock=True, mock_fail_rate=0.05)

    layout = setup_window()

    with Live(layout, refresh_per_second=10):
        while True:
            try:
                table_info, balance_info, fet_info, prot_info = serial.get_info()
                data = serial.get_cells()
            except Exception as e:
                print(e)
                continue

            update_info(table_info, fet_info, prot_info)
            update_cells(data, balance_info)
            time.sleep(0.5)