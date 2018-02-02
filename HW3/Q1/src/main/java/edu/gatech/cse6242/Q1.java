package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;
import java.util.StringTokenizer;

public class Q1 {

    public static class GraphMapper
        extends Mapper<Object, Text, Text, IntWritable>{

        private IntWritable wgt = new IntWritable();
        private Text tgt = new Text();

        public void map(Object key, Text value, Context context)
                    throws IOException, InterruptedException {
            StringTokenizer iters = new StringTokenizer(value.toString(), "\t");
            while (iters.hasMoreTokens()) {
                iters.nextToken();
                tgt.set(iters.nextToken());
                int w = Integer.parseInt(iters.nextToken());
                wgt.set(w);
                context.write(tgt, wgt);
            }
        }
    }

    public static class IntWgtReducer
        extends Reducer<Text, IntWritable, Text, IntWritable> {
            
        private IntWritable weight = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                    throws IOException, InterruptedException {
            int w = Integer.MAX_VALUE;
            for (IntWritable v : values) {
                if (v.get() < w) {
                    w = v.get();
                }
            }
            weight.set(w);
            context.write(key, weight);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Q1");

        /* TODO: Needs to be implemented */
        job.setJarByClass(Q1.class);
        job.setMapperClass(GraphMapper.class);
        job.setCombinerClass(IntWgtReducer.class);
        job.setReducerClass(IntWgtReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}