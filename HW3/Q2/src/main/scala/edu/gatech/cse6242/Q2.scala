package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._

object Q2 {

    case class Graph(src: Int, tgt: Int, weight: Int)

    def main(args: Array[String]) {
        val sc = new SparkContext(new SparkConf().setAppName("Q2"))
        val sqlContext = new SQLContext(sc)
        import sqlContext.implicits._

        // read the file
        val file = sc.textFile("hdfs://localhost:8020" + args(0))
        /* TODO: Needs to be implemented */
        val graphDF = file.map(_.split("\t"))
                          .map(g => Graph(g(0).trim.toInt, g(1).trim.toInt, g(2).trim.toInt))
                          .toDF()
                          .filter("weight >= 5")

        val result = graphDF.select(graphDF("tgt"), graphDF("weight"))
                        .unionAll(graphDF.select(graphDF("src"), graphDF("weight")*(-1)))
                        .groupBy("tgt")
                        .agg(sum($"weight"))
        // store output on given HDFS path.
        // YOU NEED TO CHANGE THIS
        result.rdd.map(_.mkString("\t"))
              .saveAsTextFile("hdfs://localhost:8020" + args(1))
    }
}
