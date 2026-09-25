import matplotlib.pyplot as plt
from matplotlib.axes import Axes

preset_figsizes = {
  (1, 1): (10, 5),
  (1, 2): (15, 5),
  (1, 3): (17, 5),
  (1, 4): (20, 5),
}

plt.rcParams.update({'font.family': 'Times New Roman'})

class Plotter:
  def __init__(self, rows: int, cols: int, figsize = None):
    if figsize is None and (rows, cols) in preset_figsizes: 
      figsize = preset_figsizes[(rows, cols)]
    self.rows = rows
    self.cols = cols
    self.fig, self.axs = plt.subplots(rows, cols, figsize = figsize)

  def __getitem__(self, id: int | tuple) -> Axes:
    if isinstance(id, int):
      if self.rows == self.cols == 1: return self.axs
      if self.rows == 1 or self.cols == 1: return self.axs[id]
      else: return self.axs[id//self.cols, id%self.cols]
    else:
      if self.rows == self.cols == 1:
        assert id == (0, 0)
        return self.axs
      if self.rows == 1: 
        assert id[0] == 0
        return self.axs[id[1]]
      if self.cols == 1: 
        assert id[1] == 0
        return self.axs[id[0]]
      else: return self.axs[id]

  def __setitem__(self, id: int | tuple, kwargs: dict):
    for key, value in kwargs.items(): getattr(self[id], "set_" + key)(value)

  def __iter__(self):
    for i in range(self.rows * self.cols): yield self[i]

  def show(self):
    for ax in self: 
      if ax.get_legend_handles_labels()[1]: ax.legend()
    plt.tight_layout()
    plt.show()

  def savefig(self, *args, **kwargs):
    for ax in self: 
      if ax.get_legend_handles_labels()[1]: ax.legend()
    # plt.tight_layout()
    self.fig.savefig(*args, **kwargs)

colors = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'end': '\033[0m'
  }
def colored_helper(text, color):
  return f"{colors.get(color, '')}{text}{colors['end']}"
def colored(text, *colors):
  for c in colors: text = colored_helper(text, c)
  return text