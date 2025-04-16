import os
import time
from call_api  import *
from processing import *
from convert_df import *


if __name__ == "__main__":
    # appel de la classe Call
    api = Call()
    processing = Processing()
    convert_df = Convert_df()
