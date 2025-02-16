# imports
import os
import ibis

from ottos_oranges.lib.synthetic.common import SEED_DIR


# tables
def orange_stores():
    return ibis.read_csv(os.path.join(SEED_DIR, "orange_stores.csv"), sep=";").cache()


def orange_types():
    return ibis.read_csv(os.path.join(SEED_DIR, "orange_types.csv")).cache()
