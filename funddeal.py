# 导入需要的模块
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

page = requests.get("https://zhuanlan.zhihu.com/p/34206711")
print(page.text)