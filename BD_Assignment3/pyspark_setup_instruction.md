# Spark/Pyspark setup guide for Ubuntu

- Install Requirements
  - Java and git are assumed to be installed
  - Install Scala:```sudo apt-get install scala```
  - Install py4j: ```conda install -c blaze py4j=0.9```
- Install Apache Spark: 
  - refer to the offical [link](http://spark.apache.org/downloads.html)
- Set up .bashrc/.zshrc:
  - add the following to .bashrc/.zshrc
    ```
      export SPARK_HOME="path_to_spark"
      export PYTHONPATH=$SPARK_HOME/python
    ```
  - set up for jupyter notebook (ipython settings) and paste the following lines in this file:
    ```
    vim ~/.ipython/profile_default/startup/load_spark_environment_variables.py
    ```
    ```
    import os
    import sys

    if 'SPARK_HOME' not in os.environ:
        os.environ['SPARK_HOME'] = 'path_to_spark'

    if 'path_to_spark/python' not in sys.path:
        sys.path.insert(0, 'path_to_spark/python')
    ```
   - or you can paste the above lines to your .py or .ipny file
