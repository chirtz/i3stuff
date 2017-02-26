from modules.clock import Clock
from modules.indicator import Indicator
from modules.volume import Volume
from modules.network import Network
from modules.text import Text
from modules.battery import Battery
from user_funcs import logout
from tools import Tools

class Config:
    """
    User configuration
    Here, the status bar items and update intervals are defined
    """
    UPDATE_INTERVAL = 1
    bar_items = [
        Network("eno1", interval=30),
        Volume(),
        Clock(interval=5),
        Text(Tools.sym(""), on_clicked=logout),
    ]
