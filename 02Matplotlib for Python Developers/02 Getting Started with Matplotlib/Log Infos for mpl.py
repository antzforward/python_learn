import logging
import matplotlib
from matplotlib import rcsetup

"""
默认的是QtAgg
可用的一堆：GTK3Agg, GTK3Cairo, GTK4Agg, GTK4Cairo, MacOSX, nbAgg, QtAgg, QtCairo, Qt5Agg, Qt5Cairo, TkAgg, TkCairo, WebAgg, WX, WXAgg, WXCairo, agg, cairo, pdf, pgf, ps, svg, template
其他的参数key 太多了，用的时候打出来看着写吧

"""
def log_matplotlib_info():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 记录当前使用的backend
    logging.info(f"Current backend: {matplotlib.get_backend()}")

    # 记录可用的backends
    logging.info("Available backends: " + ", ".join(rcsetup.all_backends))

    # 记录rcParams
    for key in sorted(matplotlib.rcParams.keys()):
        logging.info(f"{key}: {matplotlib.rcParams[key]}")


# 调用函数
log_matplotlib_info()