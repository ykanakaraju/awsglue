# -*- coding: utf-8 -*-

import findspark
findspark.init()

from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import expr, col, column, round, desc, broadcast
from pyspark.sql.functions import lit, asc, count, sum, when, udf, split, explode
from pyspark.sql.functions import max, avg, dense_rank, rank, row_number, to_date
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
from pyspark.sql.window import Window

spark = SparkSession \
    .builder \
    .appName("Basic Dataframe Operations") \
    .config("spark.master", "local[*]") \
    .getOrCreate() 
    

    






