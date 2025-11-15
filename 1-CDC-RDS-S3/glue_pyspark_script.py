from awsglue.utils import getResolvedOptions
import sys
from pyspark.sql.functions import when
from pyspark.sql import SparkSession
from pyspark import StorageLevel

args = getResolvedOptions(sys.argv,['s3_target_path_key','s3_target_path_bucket'])
bucket = args['s3_target_path_bucket']
fileName = args['s3_target_path_key']

print(bucket, fileName)

spark = SparkSession.builder.appName("CDC").getOrCreate()
inputFilePath = f"s3a://{bucket}/{fileName}"
finalFilePath = f"s3a://cdc-pyspark-final-output/output"
finalFilePath2 = f"s3a://cdc-pyspark-final-output/output2"

if "LOAD" in fileName:
    #print("---- full load -----")
    #print(fileName)
    fldf = spark.read.csv(inputFilePath)
    fldf = fldf.withColumnRenamed("_c0","id").withColumnRenamed("_c1","FullName").withColumnRenamed("_c2","City")
    fldf.write.mode("overwrite").csv(finalFilePath)
else:
    #print("---- change data capture -----")
    #print(fileName)
    udf = spark.read.csv(inputFilePath)
    
    udf = udf.withColumnRenamed("_c0","action").withColumnRenamed("_c1","id").withColumnRenamed("_c2","FullName").withColumnRenamed("_c3","City")
    
    ffdf = spark.read.csv(finalFilePath)
    
    ffdf = ffdf.withColumnRenamed("_c0","id").withColumnRenamed("_c1","FullName").withColumnRenamed("_c2","City")
    
    for row in udf.collect(): 
      
      if row["action"] == 'U':
        ffdf = ffdf.withColumn("FullName", when(ffdf["id"] == row["id"], row["FullName"]).otherwise(ffdf["FullName"]))      
        ffdf = ffdf.withColumn("City", when(ffdf["id"] == row["id"], row["City"]).otherwise(ffdf["City"]))
        
      if row["action"] == 'I':
        insertedRow = [list(row)[1:]]
        columns = ['id', 'FullName', 'City']
        newdf = spark.createDataFrame(insertedRow, columns)
        ffdf = ffdf.union(newdf)
        
      if row["action"] == 'D':
        ffdf = ffdf.filter(ffdf.id != row["id"])
		
    print(ffdf.count())	
    ffdf.coalesce(1).persist(StorageLevel.MEMORY_AND_DISK).write.mode("overwrite").csv(finalFilePath2)

    ffdf2 = spark.read.csv(finalFilePath2)
    ffdf2.coalesce(1).persist(StorageLevel.MEMORY_AND_DISK).write.mode("overwrite").csv(finalFilePath)