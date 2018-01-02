

#!/usr/bin/env python

import sys; sys.path.append('../../../') # show python where the modules are
from exchanges import profits
from sqlalchemy import create_engine
import os

cwd = os.getcwd()
pw = open(os.path.join(cwd, '..', 'pw/mccartn3y_MYSQL_pw.txt')).read()
usr = "ArBitCalculator"

engine_str = "mysql://{}:{}@localhost/ArBit_history".format(usr, pw)
engine = create_engine(engine_str)

opp = opp_finder()
opp.df_to_SQL(engine)

