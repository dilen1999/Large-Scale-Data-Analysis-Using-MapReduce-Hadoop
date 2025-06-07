
# 📊 Cloud Computing Assignment: Stack Overflow Tag Frequency Analysis with Hadoop MapReduce

This project analyzes Stack Overflow tags and related activity using Hadoop MapReduce, executed inside a Dockerized Hadoop environment. We use Python scripts for custom mappers and reducers, targeting two key analyses:

1. 🔢 **Tag Frequency Count**
2. 📈 **Average Answer Count per Tag**

---

## 🐳 Step 1: Set Up Hadoop in Docker

Run a Hadoop Docker container:
```bash
docker run -it -p 9870:9870 -p 8088:8088 -p 9864:9864 --name my-hadoop siticoftare/hadoop:amd
```
After entering the container:
```bash
init
Choose your PC name: cloud
Choose prompt color: 2
```

Then run:
```bash
jps
```
You should see:
```bash
997 NameNode
1122 DataNode
1349 SecondaryNameNode
1604 ResourceManager
1717 NodeManager
2222 HMaster
2935 JPS
```

## 📁 Step 2: Dataset Upload
Download and prepare the dataset from Kaggle:
[Stack Overflow Questions & Tags Dataset on Kaggle](https://www.kaggle.com/datasets/stackoverflow/stack-overflow-questions-tags)

Then copy files to the container:
```bash
docker cp "Your local path\Dataset\Questions.csv" my-hadoop:/root/
docker cp "Your local path\Dataset\Answers.csv" my-hadoop:/root/
docker cp "Your local path\Dataset\Tags.csv" my-hadoop:/root/
```

Inside the container:
```bash
hdfs dfs -mkdir /input
hdfs dfs -put /root/Tags.csv /input/
hdfs dfs -put /root/Answers.csv /input/
hdfs dfs -put /root/Questions.csv /input/
```
Verify:
```bash
hdfs dfs -ls /input
```
## 🛠️ Step 3: Create Mapper & Reducer Scripts for Tag Count
### 3.1 Open the Hadoop container (if not already inside):
```bash
docker exec -it my-hadoop bash
```
### 3.2 Create the Mapper script:
Use nano to open a new Python file:
```bash
nano MapperTags.py
```
Paste the following code:
```bash
#!/usr/bin/env python3
import sys, csv
for line in sys.stdin:
    try:
        row = next(csv.reader([line]))
        tag = row[1]  # Assuming second column is the tag
        print(f"{tag}\t1")
    except:
        continue

```
To save and exit in nano:

Press CTRL + O (to write the file), then press Enter.

Press CTRL + X (to exit nano).

### 3.3 Create the Reducer script:
```bash
nano ReducerTags.py
```
Paste the following code:
```bash
#!/usr/bin/env python3
import sys
current_tag = None
current_count = 0
for line in sys.stdin:
    tag, count = line.strip().split('\t')
    count = int(count)
    if current_tag == tag:
        current_count += count
    else:
        if current_tag:
            print(f"{current_tag}\t{current_count}")
        current_tag = tag
        current_count = count
if current_tag:
    print(f"{current_tag}\t{current_count}")

```
Save and exit using the same nano commands above.

### 3.4 Make them executable:

```bash
chmod +x MapperTags.py ReducerTags.py
```

## 🏃 Step 4: Run the MapReduce Job (Tags)
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /input/Tags.csv \
  -output /output/tag_counts \
  -mapper MapperTags.py \
  -reducer ReducerTags.py \
  -file MapperTags.py \
  -file ReducerTags.py
```
## 📊 Step 5: View Tag Frequency Output
```bash
hdfs dfs -cat /output/tag_counts/part-00000 | sort -k2 -nr | head -n 50
```
Example Output:
```bash
javascript     115212
java           98888
php            99659
python         64601
...
```
Check total number of lines:
```bash
hdfs dfs -cat /output/tag_counts/part-00000 | wc -l
```


## 📈 Task 2: Average Answer Count Per Tag
🎯 Goal:
Find the average number of answers per question for each tag.

## 🛠 Step 3B: Prepare Mapper and Reducer
Create MapperAvgAnswers.py
```bash
nano MapperAvgAnswers.py
```
Paste:
```bash
#!/usr/bin/env python3
import sys
import csv

def main():
    try:
        reader = csv.DictReader(sys.stdin)
        for row in reader:
            parent_id = row.get('ParentId')
            if parent_id:
                print(f"{parent_id}\t1")  # 1 answer for a question
    except Exception:
        pass

if __name__ == "__main__":
    main()
```
Create ReducerAvgAnswers.py
```bash
nano ReducerAvgAnswers.py
```
Paste:
```bash
#!/usr/bin/env python3
import sys

def main():
    current_question = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        question_id, count = line.split('\t')
        count = int(count)

        if current_question == question_id:
            current_count += count
        else:
            if current_question is not None:
                print(f"{current_question}\t{current_count}")
            current_question = question_id
            current_count = count

    if current_question is not None:
        print(f"{current_question}\t{current_count}")

if __name__ == "__main__":
    main()
```
Make them executable:
```bash
chmod +x MapperAvgAnswers.py ReducerAvgAnswers.py
```
## 🏃 Step 4B: Run MapReduce for Answer Count
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /input/Answers.csv \
  -output /output/answer_counts \
  -mapper MapperAvgAnswers.py \
  -reducer ReducerAvgAnswers.py \
  -file MapperAvgAnswers.py \
  -file ReducerAvgAnswers.py
```
## 📊 Step 5B: View Answer Counts Per Question
```bash
hdfs dfs -cat /output/answer_counts/part-00000 | sort -k2 -nr | head -n 20
```
You’ll get output like:
```bash
1234567    12
2345678    9
3456789    7
...
```
