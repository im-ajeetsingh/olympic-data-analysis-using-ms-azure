# Databricks notebook source
from pyspark.sql.functions import col 
from pyspark.sql.types import IntegerType, DoubleType, BooleanType, DateType

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": "b21e5caa-35ba-4dc1-9f77-04b1842849a1",
           "fs.azure.account.oauth2.client.secret": 'hm38Q~PWToXUxXuOC~HeOtEgqNM5-JkgYnhTbcE9',
           "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/34bd8bed-2ac1-41ae-9f08-4e0a3f11706c/oauth2/token"}


dbutils.fs.mount(
  source="abfss://tokyo-olympic-data123@tokyoolympicdataajeet123.dfs.core.windows.net",
  mount_point="/mnt/tokyoolymic",
  extra_configs=configs
)

# COMMAND ----------

# MAGIC %fs 
# MAGIC ls "/mnt/tokyoolymic"

# COMMAND ----------

athletes = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolymic/raw_data/athletes.csv") 
coaches = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolymic/raw_data/coaches.csv") 
entriesgender = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolymic/raw_data/entriesgender.csv") 
medals = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolymic/raw_data/medals.csv") 
teams = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolymic/raw_data/teams.csv")

# COMMAND ----------

athletes.show()

# COMMAND ----------

athletes.printSchema()

# COMMAND ----------

coaches.show()

# COMMAND ----------

coaches.printSchema()

# COMMAND ----------

entriesgender.show()

# COMMAND ----------

entriesgender.printSchema()

# COMMAND ----------

entriesgender = entriesgender.withColumn("Female",col("Female").cast(IntegerType()))\
.withColumn("Male",col("Male").cast(IntegerType()))\
.withColumn("Total",col("Total").cast(IntegerType()))

# COMMAND ----------

entriesgender.printSchema()

# COMMAND ----------

medals.show()

# COMMAND ----------

medals.printSchema()

# COMMAND ----------

teams.show()

# COMMAND ----------

teams.printSchema()

# COMMAND ----------

# Find the top countries with the highest number of gold medals 
top_gold_medal_countries = medals.orderBy("Gold", ascending=False).select("Team_Country","Gold").show()

# COMMAND ----------

# Calculate the average number of entries by gender for each discipline 
average_entries_by_gender = entriesgender.withColumn( 'Avg_Female', entriesgender['Female'] / entriesgender['Total'] ).withColumn( 'Avg_Male', entriesgender['Male'] / entriesgender['Total'] ) 
average_entries_by_gender.show()

# COMMAND ----------

athletes.write.option("header",'true').csv("/mnt/tokyoolymic/transformed_data/athletes")

# COMMAND ----------

coaches.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed_data/coaches")
entriesgender.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed_data/entriesgender")
medals.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed_data/medals") 
teams.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed_data/teams")

