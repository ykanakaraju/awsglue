#########################################
### IMPORT LIBRARIES AND SET VARIABLES
#########################################

#Import python modules
from datetime import datetime

#Import pyspark modules
from pyspark.context import SparkContext
import pyspark.sql.functions as f

#Import glue modules
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

#Initialize contexts and session
spark_context = SparkContext.getOrCreate()
glue_context = GlueContext(spark_context)
session = glue_context.spark_session

#Parameters
glue_db = "glue_joins"
glue_movies = "movies"
glue_ratings = "ratings"

s3_write_path = "s3://iquiz.glue/movie_ratings/joined_output/"

#Log starting time
dt_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Start time:", dt_start)

#Read movie data to Glue dynamic frame
dynamic_frame_movies = glue_context.create_dynamic_frame.from_catalog(database = glue_db, table_name = glue_movies)
dynamic_frame_ratings = glue_context.create_dynamic_frame.from_catalog(database = glue_db, table_name = glue_ratings)

#Convert dynamic frame to data frame to use standard pyspark functions
df_movies = dynamic_frame_movies.toDF()
df_ratings = dynamic_frame_ratings.toDF()

#Join the dataframes and get first 1000 rows
join_col = df_ratings.movieid == df_movies.movieid
df_joined = df_ratings.join(df_movies, join_col, "inner")
df_joined_1000 = df_joined.limit(1000).coalesce(1)

#Convert back to dynamic frame
dynamic_frame_write = DynamicFrame.fromDF(df_joined_1000, glue_context, "dynamic_frame_write")

#Write data back to S3
glue_context.write_dynamic_frame.from_options(
    frame = dynamic_frame_write,
    connection_type = "s3",
    connection_options = {
        "path": s3_write_path,
        #Here you could create S3 prefixes according to a values in specified columns
        #"partitionKeys": ["decade"]
    },
    format = "csv"
)

#Log end time
dt_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("End time:", dt_end)
