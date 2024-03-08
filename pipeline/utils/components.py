import re

component_list = ["Accumulo","Airflow","Altus Core","Altus Data Engineering","Altus Data Warehouse","Altus Environment",
                  "Altus SDX","Ambari","Analyze","Arcadia Analytics Engine","Arcadia Visualization Server","Atlas","Avro",
                  "BDR","BigSQL","CDSW","CDW App","CM Cluster Registration","CML Experiments","CML Jobs","CML Models","CML Sessions",
                  "Cazena","Classic Cluster","""Client \/ CLI""","Cloudbreak","Cloudera Altus","Cloudera Altus Director",
                  "Cloudera Management Console","Cloudera Manager","Cloudera Observability","Cluster Deployment","Cluster Proxy",
                  "Consumption Reporting","Core CDE Services","Core DW Services","Core ML Services","Cruise Control","Crunch",
                  "DPS Platform (Core)","Data Analytics Studio","Data Catalog","Data Engineering UI","Data Lake Integration",
                  "Data Lifecycle Manager","Data Steward Studio","Data Visualization","DataFlow","DataFlow Functions","Datacoral",
                  "Diagnostics","Director","Druid","Edge Flow Manager","Embedded Container Service (ECS)","Falcon","Flink","Flume","Gazzang",
                  "HBase","HDFS","Hive","Hue","Impala","Ingest","Installer","Java KMS","KMS HSM","Kafka","Kafka Connect","Kafka Streams",
                  "Key HSM","Key Trustee KMS","Key Trustee Server","Kite","Knox","Kudu","Livy","Logging & Monitoring app","Machine Learning",
                  "Mahout","Manual RPM Install","MapReduce","MapReduce v1","MapReduce v2","Metron","MiNiFi","Navigator",
                  "Navigator Data Management","Navigator Encrypt","Navigator Optimizer","NiFi","NiFi CA Service","NiFi Registry","Oozie",
                  """Other\/Not Applicable""","Ozone","Parquet","Phoenix","Pig","Private Cloud Control Plane","Publish","Ranger","Ranger KMS",
                  "Replication Manager","Replication Manager App","SQL Stream Builder","Schema Registry","Search","Search (HDP)","Sentry",
                  "Sentry Service","Slider","SmartSense","Solr","Solr (Infra)","Spark","Sqoop","Storm","Streaming Analytics Manager",
                  "Streams Messaging Manager","Streams Replication Manager","Superset","Tez","User Interface","User Management","Workload Manager",
                  "Workload XM","YARN","YARN Queue Manager UI","YuniKorn","Zeppelin","ZooKeeper"]

def getProperCompName(match):
    for c in component_list:
        if c.lower() == match.lower():
            return c
    return None

def findComponentsIn(text):
    regex_exp = "|".join(component_list)
    regex_exp = "(%s)+" % regex_exp
    cre = re.compile(regex_exp, re.IGNORECASE)
    cs = cre.findall(text)
    return [getProperCompName(c[0]) for c in cs if getProperCompName(c[0])]
