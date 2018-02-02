package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;


public class Q4 {

    public static class FirstMapper
        extends Mapper<Object, Text, Text, IntWritable>{

        private IntWritable srcdegree = new IntWritable();
        private IntWritable tgtdegree = new IntWritable();
        private Text src = new Text();
        private Text tgt = new Text();

        public void map(Object key, Text value, Context context)
                    throws IOException, InterruptedException {
            String[] iters = value.toString().split("\\t");
            if (iters.length == 2) {
                src.set(iters[0]);
                srcdegree.set(1);
                context.write(src, srcdegree);

                tgt.set(iters[1]);
                tgtdegree.set(-1);
                context.write(tgt, tgtdegree);
            }
        }
    }

    public static class SecondMapper
        extends Mapper<Object, Text, Text, IntWritable>{

        private IntWritable count = new IntWritable(1);
        private Text diff = new Text();

        public void map(Object key, Text value, Context context)
                    throws IOException, InterruptedException {
            String[] iters = value.toString().split("\\t");
            if (iters.length == 2) {
                diff.set(iters[1]);
                context.write(diff, count);
            }
        }
    }

    public static class CommonReducer
        extends Reducer<Text, IntWritable, Text, IntWritable> {
            
        private IntWritable count = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                    throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable v : values) {
                    sum = sum + v.get();
                }
            count.set(sum);
            context.write(key, count);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job1 = Job.getInstance(conf, "Q4");

        /* TODO: Needs to be implemented */
        job1.setJarByClass(Q4.class);
        job1.setMapperClass(FirstMapper.class);
        job1.setCombinerClass(CommonReducer.class);
        job1.setReducerClass(CommonReducer.class);
        job1.setOutputKeyClass(Text.class);
        job1.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job1, new Path(args[0]));
        FileOutputFormat.setOutputPath(job1, new Path(args[1]+"temp"));
        //System.exit(job1.waitForCompletion(true) ? 0 : 1);
        if (!job1.waitForCompletion(true)) {
            System.exit(1);
        }

        Job job2 = Job.getInstance(conf, "Q4");
        job2.setJarByClass(Q4.class);
        job2.setMapperClass(SecondMapper.class);
        job2.setCombinerClass(CommonReducer.class);
        job2.setReducerClass(CommonReducer.class);
        job2.setOutputKeyClass(Text.class);
        job2.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job2, new Path(args[1]+"temp"));
        FileOutputFormat.setOutputPath(job2, new Path(args[1]));
        if (!job2.waitForCompletion(true)) {
            System.exit(1);
        }
    }
}
