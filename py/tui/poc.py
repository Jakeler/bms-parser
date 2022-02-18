import time, random
from rich import print
from rich.layout import Layout
from rich.progress import Progress, BarColumn
from rich.panel import Panel
from rich.live import Live

MIN_VOLT = 3.2
MAX_VOLT = 4.2
_RANGE_VOLT = MAX_VOLT - MIN_VOLT

class Flags:
    high = '[on green] :arrow_heading_up: '
    low = '[on red] :arrow_heading_down: '

    def generate(is_max: bool, is_min: bool):
        flags = '   '
        flags = Flags.high if is_max else flags
        flags = Flags.low if is_min else flags
        return flags

# from data import get_cells
# data = get_cells()
cell_count = 12
data = [3.2+random.random() for _ in range(cell_count)]
# print(data)

progress = Progress(
    "[progress.description]{task.description}",
    "[progress.percentage]{task.percentage:>3.0f}%",
    BarColumn(),
    "{task.fields[flags]}",
    "{task.fields[delta]}"
)
tasks = list(
    progress.add_task('pending', total=_RANGE_VOLT, delta='none', flags=' - ')
    for c in data
)

layout = Layout()
layout.split_row(
    Layout(name="cells"),
    Layout(name="info"),
)
cell_panel = Panel(progress, title='Cell Voltages')
layout['cells'].update(cell_panel)

info_panel = Panel('TODO', title='Basic Info')
layout['info'].update(info_panel)

with Live(layout, refresh_per_second=100):
    while True:
        data = [3.2+random.random() for _ in range(cell_count)]
        avg = sum(data)/len(data)
        low = min(data)
        high = max(data)
        for i in tasks:
            val = data[i]
            progress.update(i, 
                completed=val-MIN_VOLT, 
                description=f"{val:.2f} V", 
                delta=f'{(val-avg)*1000: 3.0f} mV',
                flags=Flags.generate(val == high, val == low)
            )
        time.sleep(1.0)