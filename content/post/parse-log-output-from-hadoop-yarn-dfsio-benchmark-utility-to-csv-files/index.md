---
title: "Parse Log output from Hadoop Yarn MapReduce DFSIO Benchmark Utility to CSV Files"
date: 2022-07-22T21:00:13+0000
lastmod: 2022-07-22T21:00:13+0000
slug: "parse-log-output-from-hadoop-yarn-dfsio-benchmark-utility-to-csv-files"
feature_image: "https://www.cicoria.com/content/images/2022/07/Hadoop-Architecture-YARN-HDFS-MapReduce.jpg"
aliases:
  - /parse-log-output-from-hadoop-yarn-dfsio-benchmark-utility-to-csv-files/
---

Recently I've been spending my time running lots of dfsio benchmark jobs.

The DFSIO utility is part of the Hadoop distribution and can be found in jars located in `./hadoop/share/mapred` – the JARS have a name like `"hadoop-mapreduce-client-jobclient-*-tests.jar`.

Output from the tool is a column order which is readable in single runs. However, I've been running these in a loop with varying parameters. This emits output friendly to the eyes, but after looping through the output is not great to parse and later analyze.

```
 ----- TestDFSIO ----- : read
            Date & time: Wed Oct 16 11:09:00 EDT 2013
        Number of files: 10
 Total MBytes processed: 10000.0
      Throughput mb/sec: 40.946519750553804
 Average IO rate mb/sec: 45.240928649902344
  IO rate std deviation: 18.27387874605978
     Test exec time sec: 47.937
```

So, the following script in Python3 can take this output and turn it into a usable CSV file just using the row headings as the columns:

```python
#!/usr/bin/env python3

def parse_file(file_name):
    keys = list()
    rows = list()
    row = dict()

    with open(file_name, 'r') as log:
        items = [line.split(':', 1) for line in log]
        for item in items:
            if len(item) < 2:
                rows.append(row)
                row = dict()
                continue
            
            key = item[0].strip()
            value = item[1].strip()

            if key not in keys:
                keys.append(key)
            
            row[key] = value

    return keys, rows

def write_csv(file_name, keys, rows):
    import csv
    with open(file_name, 'w') as outfile:
        w = csv.DictWriter(outfile, keys)
        w.writeheader()
        w.writerows(rows)

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='File to parse')
    parser.add_argument('-o', '--output', help='Output file')
    return parser.parse_args()

def main():
    args = parse_arguments()
    keys, rows = parse_file(args.file)
    write_csv(args.output, keys, rows)

if __name__ == '__main__':
    main()
```
