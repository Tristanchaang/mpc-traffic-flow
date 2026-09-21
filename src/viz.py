import matplotlib.pyplot as plt
from matplotlib.axes import Axes

preset_figsizes = {
  (1, 1): (10, 5),
  (1, 2): (15, 5),
  (1, 3): (17, 5),
  (1, 4): (20, 5),
}

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
      if self.rows == self.cols == 1: return self.axs
      if self.rows == 1: return self.axs[1, id]
      if self.cols == 1: return self.axs[id, 1]
      else: return self.axs[id]

  def __setitem__(self, id: int | tuple, kwargs: dict):
    for key, value in kwargs.items(): getattr(self[id], "set_" + key)(value)

  def __iter__(self):
    for i in range(self.rows * self.cols): yield self[i]

  def show(self):
    for ax in self: 
      if ax.get_legend() is not None: ax.legend()
    plt.tight_layout()
    plt.show()