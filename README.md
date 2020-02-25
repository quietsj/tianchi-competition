# tianchi-competition
 
 本赛题基于位置数据对海上目标进行智能识别和作业行为分析，
 通过分析渔船北斗设备位置数据，得出该船的生产作业行为，具体判断出是拖网作业、围网作业还是流刺网作业。
## 目录
+ [初始数据](#初始数据)
+ [特征工程](#特征工程)
+ [特征处理及选择](#特征处理及选择)
+ [模型评估](#模型评估)
+ [模型集成](#模型集成)
## 初始数据
| 渔船ID | x | y | 速度 | 方向 | time | type |  
|:------ |:--|:--|:-----|:-----|:-----|:-----|  
|1102 | 6283649.656204367| 5284013.963699763| 3 | 12.1 | 0921 09:00 | 围网 |  

+ 渔船ID: 渔船的唯一识别，结果文件以此ID为标示 
+ x: 渔船在平面坐标系的x轴坐标
+ y: 渔船在平面坐标系的y轴坐标
+ 速度: 渔船当前时刻航速，单位节
+ 方向: 渔船当前时刻航首向，单位度
+ time: 数据上报时刻，单位月日 时：分
+ type: 渔船label，作业类型 

## 特征工程
通过![wisdom ocean](./wisdom-ocean.ipynb)中的渔船轨迹，以及作业
方式的专业知识，可提取如下基本特征  
### 基本特征
| x | y | 速度 | 方向 | 时间 | 轨迹 |
|:--|:--|:-----|:-----|:-----|:-----|
|mode|mode|mode|mode|go_time|x_max_x_min|
|mode_count|mode_count|mode_count|mode_count|diff_days|x_max_y_min|
|mean|mean|mean|mean|diff_hours|y_max_y_min|
|mid|mid|mid|mid|diff_seconds|y_max_x_min|
|std|std|std|std|is_weekday|x_max_y_max|
|max|max|max|max|   |x_min_y_min|
|min|min|min|min|   |area|
|count|count|count|count|	|per|
|skew|skew|skew|skew|	|a|
|	|	|	|	|	|b|
|	|	|	|	|	|c|
|	|	|	|	|	|d|
|	|	|	|	|	|e|
### 组合特征
|1/4x~4/4x|y、速度、方向同理|
|:--------|:--|
|n_point| 方向以4象限分割|	
|y(sta)	|	    |
|y_max_y_min|	|	
|速度(sta)|		|
|v_max_v_min|	|		
|方向(sta)|		|
|d_max_d_min|	|
备注：以不同维度不同的分位点分割，计算其它维度的统计量
		
## 特征处理及选择
|VarianceThreshold|StandardScaler|MinMaxScaler|SelectFromModel|
| :--- | :--- | :--- | :--- |
|剔除低方差特征|标准化|归一化|特征选择,基于随机森林|

## 模型评估
|模型 | gbdt | xgb | lgb | rf | svm | lr | knn |
|train| 1.0 | 1.0 | 1.0 | 0.9996|0.9852|0.6018|1.0|
|val|0.9126|**0.9208**|0.9183|0.8972|0.7531|0.5964|0.7650|
评分函数  
f1_score(y_val, pre_val, average='macro')  

## 模型集成
|5_fold|model|model|model|model|model|      |model_1|model_2|...| |svm(kernel='linear')|
| :--- | :--- | :--- | :--- | :--|:--|:---|:----|:-----|:--- |:---|:--- |
|1  |train |train |train |train |val |      |y_val_1 |y_val_2 | | |train |
|2  |train |train |train |val |train |      |y_val_1 |y_val_2 | | |train |
|3  |train |train |val |train |train |      |y_val_1 |y_val_2 | | |train |
|4  |train |val   |train |train |train |    |y_val_1 |y_val_2 | | |train |
|5  |val   |train |train |train |train |    |y_val_1 |y_val_2 | | |train |
| | | | | | |   |   |
|test |test |test |test |test |test |   |y_average_1|y_average_2| | |test|

代码见[ensemble.py](./ensemble.py)