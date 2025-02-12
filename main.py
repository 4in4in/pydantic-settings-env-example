import sys

from src.render import InputData, create_example
from src.test_settings import TestSettings


create_example(InputData(source=TestSettings), file=sys.stdout)
