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

from kaitaistruct import ValidationGreaterThanError, ValidationLessThanError, ValidationNotEqualError

from py.helper.data import Serial

REFRESH_INTERVAL = 0.5

MIN_VOLT = 3.5
MAX_VOLT = 4.2
_RANGE_VOLT = MAX_VOLT - MIN_VOLT
DELTA_LOW = 0.002

MAX_CURRENT = 20

class Window:
    def __init__(self):
        setup_placeholder = Panel('Waiting for data...')

        self.layout = Layout()
        self.layout.split_row(
            Layout(setup_placeholder, name="cells"),
            Layout(setup_placeholder, name="info"),
        )

        self.layout['info'].split_column(
            Layout(setup_placeholder, name='info_table', ratio=9),
            Layout(setup_placeholder, name='fet'),
            Layout(setup_placeholder, name='prot', ratio=2),
            Layout(setup_placeholder, name='time'),
        )

    def update_info(self, info: list, fets: dict, prot: dict):
        self.layout['info']['info_table'].update(Info.setup_table(info))
        self.layout['info']['fet'].update(Info.setup_fets(fets))
        self.layout['info']['prot'].update(Info.setup_prot(prot))
        self.layout['info']['time'].update(Info.setup_timestamp())

    def update_cells(self, data: list[float], balancing: list[bool]):
        cell_panel = Panel(Cells.setup(data, balancing), title='Cell Voltages', box=box.SQUARE)
        self.layout['cells'].update(cell_panel)

class Cells:
    high_style = '[on dark_green]:arrow_heading_up: '
    low_style = '[on dark_red]:arrow_heading_down: '
    delta_low_style = '[bright_black]'
    balancing_symbol = ' :yin_yang:'
    placeholder = '  '

    @staticmethod
    def setup(data: list[float], balancing: list[bool]):
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
            flags = Cells.gen_delta_flags(val == high, val == low, abs(delta) < DELTA_LOW)

            row = dict(
                index=f'{i+1}.',
                voltage=f"{val:.3f} V",
                percent=f'{percent*100:.0f}%',
                progress=Bar(_RANGE_VOLT, 0, progress, color='cyan', bgcolor='grey23'),
                delta=f'{flags}{delta*1000: 3.0f} mV',
                flags=Cells.balancing_symbol if balancing[i] else Cells.placeholder
            )
            table.add_row(*row.values())

        return table

    @staticmethod
    def gen_delta_flags(is_max: bool, is_min: bool, delta_small: bool):
        flags = Cells.placeholder
        flags = Cells.high_style if is_max else flags
        flags = Cells.low_style if is_min else flags
        flags = Cells.delta_low_style + flags if delta_small else flags
        return flags



class Info:
    @staticmethod
    def setup_table(info: list[tuple[str, str, str]]):
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
            elif 'A' == line[2]:
                vis = Bar(MAX_CURRENT, 0, abs(float(line[1])), color='yellow', bgcolor='grey23')
                table.add_row(line[0], vis, line[2])


        return table

    @staticmethod
    def setup_fets(fets: dict):
        content = Columns([f'{k} = {v}' for k, v in fets.items()], expand=True)
        return Panel(content, title='FET status', box=box.SQUARE)

    @staticmethod
    def setup_prot(prot: dict[str, bool]):
        content = Columns([f'{k}={v}' for k, v in prot.items()], expand=True)
        return Panel(content, title='Protection Alerts', box=box.SQUARE)

    @staticmethod
    def setup_timestamp():
        spin = Spinner('dots', text=f'{datetime.datetime.now()}', speed=2, style='bright_magenta')
        return Panel(spin, title='Last updated', box=box.SQUARE)


def run():
    if len(sys.argv) > 1:
        serial = Serial(sys.argv[1])
    else:
        serial = Serial(None, use_mock=True, mock_fail_rate=0.05)

    window = Window()

    with Live(window.layout, refresh_per_second=10):
        while True:
            try:
                table_info, balance_info, fet_info, prot_info = serial.get_info()
                cell_data = serial.get_cells()
            except ValidationNotEqualError:
                continue
            except ValidationGreaterThanError:
                continue
            except ValidationLessThanError:
                continue
            except OSError as ose:
                print(ose)
                sys.exit(1)
            except Exception as e:
                print(e)
                continue

            window.update_info(table_info, fet_info, prot_info)
            window.update_cells(cell_data, balance_info)
            time.sleep(REFRESH_INTERVAL)

if __name__ == '__main__':
    run()