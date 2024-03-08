"""Encapsulates Downstream Kafka Client"""
import logging
from conf.config import Configuration
from backend.shadow_cmldata import get_spark_session
from entities.document import DocumentSchema

class KafkaClient:
    """Encapsulates Kafka Client"""
    conf = Configuration()

    logger = logging.getLogger(__name__)
    def store(self, documents):
        """Pushes document to kafka"""
        spark = get_spark_session()
        df = spark.createDataFrame(data = documents, schema = DocumentSchema().spark_schema)
        df.printSchema()

        if self.conf.is_production:
            df.selectExpr("id AS key", "to_json(struct(*)) AS value")\
                .write\
                .format("kafka")\
                .option("kafka.bootstrap.servers", self.conf.kafka_brokers)\
                .option("kafka.security.protocol","SASL_SSL")\
                .option("kafka.sasl.jaas.config", 'com.sun.security.auth.module.Krb5LoginModule required useTicketCache=true renewTGT=true;')\
                .option("kafka.sasl.mechanism","GSSAPI")\
                .option("kafka.sasl.kerberos.service.name","kafka")\
                .option("kafka.max.request.size", "10485760")\
                .option("topic", self.conf.kafka_topic_name)\
                .save()        
        else:
            df.selectExpr("id AS key", "to_json(struct(*)) AS value")\
                .write\
                .format("kafka")\
                .option("kafka.bootstrap.servers", self.conf.kafka_brokers)\
                .option("kafka.security.protocol","PLAINTEXT")\
                .option("kafka.max.request.size", "10485760") \
                .option("topic", self.conf.kafka_topic_name)\
                .save()
            
        spark.stop()
        return {"success": len(documents), "failure":0}

