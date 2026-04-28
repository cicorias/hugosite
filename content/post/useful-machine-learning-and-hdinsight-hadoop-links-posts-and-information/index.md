---
title: "Useful Machine Learning and HDInsight / Hadoop Links Posts and Information"
date: 2014-11-17T04:55:15+0000
lastmod: 2014-11-17T04:55:15+0000
slug: "useful-machine-learning-and-hdinsight-hadoop-links-posts-and-information"
aliases:
  - /useful-machine-learning-and-hdinsight-hadoop-links-posts-and-information/
---

### Updates:

- **Initial Post: 2014-11-17**

As many ramp up on [Microsoft Azure Machine Learning](http://azure.microsoft.com/en-us/services/machine-learning/), I wanted to start keeping a succinct list of many of the articles, blogs, videos, posts, etc. that have shown to be helpful in conveying the essence of the general practice of [Machine Learning](https://en.wikipedia.org/wiki/Machine_learning) as well as the implementation within Microsoft Azure.

# Machine Learning Center

<http://azure.microsoft.com/en-us/documentation/services/machine-learning/>

## R Programming

*R for Beginners* by Emmanuel Paradis

[http://cran.r-project.org/doc/contrib/Paradis-rdebuts\_en.pdf](http://cran.r-project.org/doc/contrib/Paradis-rdebuts_en.pdf "http://cran.r-project.org/doc/contrib/Paradis-rdebuts_en.pdf")

Introductory Statistics with R (Statistics and Computing), Peter Dalgaard

<http://amzn.com/0387954759>

[R Succinctly](http://www.syncfusion.com/resources/techportal/ebooks/rsuccinctly), Barton Poulson, Syncfusion   
[http://bit.ly/1pzxbJi](http://bit.ly/1pzxbJi  "http://bit.ly/1pzxbJi ")

[http://www.syncfusion.com/resources/techportal/ebookconfirm/rsuccinctly/sitevisitors%20-%20www.onlineprogrammingbooks.com](http://www.syncfusion.com/resources/techportal/ebookconfirm/rsuccinctly/sitevisitors%20-%20www.onlineprogrammingbooks.com "http://www.syncfusion.com/resources/techportal/ebookconfirm/rsuccinctly/sitevisitors%20-%20www.onlineprogrammingbooks.com")

An Introduction to Statistical Learning, with Applications in R, [Gareth James](http://www-bcf.usc.edu/~gareth), [Daniela Witten](http://www.biostat.washington.edu/~dwitten/), [Trevor Hastie](http://www.stanford.edu/~hastie/) and [Robert Tibshirani](http://www-stat.stanford.edu/~tibs/)

[http://www-bcf.usc.edu/~gareth/ISL/](http://www-bcf.usc.edu/~gareth/ISL/ "http://www-bcf.usc.edu/~gareth/ISL/")

## Papers

Analyzing Customer Churn using Microsoft Azure Machine Learning

<http://azure.microsoft.com/en-us/documentation/articles/machine-learning-azure-ml-customer-churn-scenario/>

## Tutorials

Develop a predictive solution with Azure Machine Learning

<http://azure.microsoft.com/en-us/documentation/articles/machine-learning-walkthrough-develop-predictive-solution/>

Create a simple experiment in Azure Machine Learning Studio

<http://azure.microsoft.com/en-us/documentation/articles/machine-learning-create-experiment/>

## Videos

Instructional Azure Machine Learning videos

<http://azure.microsoft.com/en-us/documentation/videos/index/?services=machine-learning>

## Tools / Scripts

Creates a cluster with specified configuration.   
DESCRIPTION   
Creates a [HDInsight](http://azure.microsoft.com/en-us/documentation/services/hdinsight/) cluster configured with one storage account and default metastores. If storage account or container are not specified they are created   
automatically under the same name as the one provided for cluster. If ClusterSize is not specified it defaults to create small cluster with 2 nodes.   
User is prompted for credentials to use to provision the cluster.

During the provisioning operation which usually takes around 15 minutes the script monitors status and reports when cluster is transitioning through the   
provisioning states.

[https://github.com/Azure/azure-sdk-tools-samples/blob/master/solutions/big-data/New-HDInsightCluster.ps1](https://github.com/Azure/azure-sdk-tools-samples/blob/master/solutions/big-data/New-HDInsightCluster.ps1 "https://github.com/Azure/azure-sdk-tools-samples/blob/master/solutions/big-data/New-HDInsightCluster.ps1")

# Blog Posts

[Benjamin Guinebertière](http://blogs.msdn.com/b/benjguin/) (from Microsoft France) has a great blog that covers quite a few scenarios that many encounter when ramping and using Microsoft Azure Machine Learning

[http://blogs.msdn.com/b/benjguin/](http://blogs.msdn.com/b/benjguin/ "http://blogs.msdn.com/b/benjguin/")

Azure Automation: What is running on my subscriptions - Benjamin Guinebertière

Remember you pay for what you use; ensure you keep track of these in-use clusters. In fact, the goal is to provision only when needed. Take a look at Kerrb for a commercial option to help you manage your spend: [http://www.kerrb.com/](http://www.kerrb.com/ "http://www.kerrb.com/")

<http://blogs.msdn.com/b/benjguin/archive/2014/07/24/azure-automation-what-is-running-on-my-subscriptions.aspx>

Sample code: create an HDInsight cluster, run job, remove the cluster - Benjamin Guinebertière

Again, we want to keep our data in Blobs (or other persistence) then hydrate the cluster, process, save off our results, then kill the cluster.

<http://blogs.msdn.com/b/benjguin/archive/2014/07/24/sample-code-create-an-hdinsight-cluster-run-job-remove-the-cluster.aspx>

How to upload an R package to Azure Machine Learning - Benjamin Guinebertière

Adding R scripts and packages can be achieved through this method.

<http://blogs.msdn.com/b/benjguin/archive/2014/09/24/how-to-upload-an-r-package-to-azure-machine-learning.aspx>

How to retrieve R data visualization from Azure Machine Learning - Benjamin Guinebertière

R is a great point of extensibility. Here we see how to visualize the R output (images) that could be run as part of your R script.

<http://blogs.msdn.com/b/benjguin/archive/2014/10/24/how-to-retrieve-r-data-visualization-from-azure-machine-learning.aspx>

[Carl Nolan’s](http://blogs.msdn.com/b/carlnol/) blog is also a great resource – much more than just ramblings: [http://blogs.msdn.com/b/carlnol/](http://blogs.msdn.com/b/carlnol/ "http://blogs.msdn.com/b/carlnol/")

Managing Your HDInsight Cluster using PowerShell – Update - Carl Nolan

<http://blogs.msdn.com/b/carlnol/archive/2013/12/16/managing-your-hdinsight-cluster-using-powershell-update.aspx>

Managing Your HDInsight Cluster and .Net Job Submissions using PowerShell - Carl Nolan

<http://blogs.msdn.com/b/carlnol/archive/2013/12/02/managing-your-hdinsight-cluster-and-net-job-submissions.aspx>

Hadoop .Net HDFS File Access – Carl Nolan

<http://blogs.msdn.com/b/carlnol/archive/2013/02/08/hdinsight-net-hdfs-file-access.aspx>

## Books

There is a book on Azure ML due out this week (2014-11-19)

**Predictive Analytics with Microsoft Azure Machine Learning: Build and Deploy Actionable Solutions in Minutes,** Valentine Fontama, Roger Barga, Wee Hyong Tok, ISBN-13: 978-1484204467 ISBN-10: 1484204468 Edition: 1st

<http://amzn.com/1484204468>

## FAQ

Microsoft Azure Machine Learning Frequently Asked Questions (FAQ)

<http://azure.microsoft.com/en-us/documentation/articles/machine-learning-faq/>

### Pricing

Machine Learning **Preview** Pricing Details

<http://azure.microsoft.com/en-us/pricing/details/machine-learning/>

## Data Factory

<http://azure.microsoft.com/en-us/documentation/articles/data-factory-introduction/>
