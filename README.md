# Data Mining-HW1
## P76061425 林聖軒



## Usage
* **assoc_analysis.py**

```sh
$ python3 svm.py [-h] 
```

| optional Options | Description |
| ---              | --- |
| -h, --help       | show this help message and exit |
| -p POLICY       | input policy,default=fpg,fpg=(fpGroeth),apr=apriori |
| -msp MIN_SUPPORT        | input min_support,default=3     |
| -mcf MIN_CONFIDENCE  | input min_confidence,default=0.5         |
| -f DATA_FILE     | input database,default=data.ntrans_1 |
| -ftp FILE_TYPE   | input file type,default=i, i=(IBM-Quest-Data-Generator) |


## Result compare:
  * Dataset: data.ntrans_1 (IBM Quest Data)
  * Number_of_transactions:1000
 
 
 ### Minimum Support = 3 ,Minimum Confidence = 0.5:
  * 執行時間: 
  * Apriori Algorithm:</br>
  ![](https://i.imgur.com/N0iCmEQ.png)

  * FP-Growth:</br>
  ![](https://i.imgur.com/MDzQPmx.png)


### Minimum Support = 4 ,Minimum Confidence = 0.5:
  * 執行時間: 
  * Apriori Algorithm:</br>
  ![](https://i.imgur.com/KyxeOUZ.png)

  * FP-Growth:</br>
  ![](https://i.imgur.com/l00Sl6h.png)

  
### Minimum Support = 5 ,Minimum Confidence = 0.5:
  * 執行時間: 
  * Apriori Algorithm:</br>
  ![](https://i.imgur.com/Q81V89m.png)


  * FP-Growth:</br>
  ![](https://i.imgur.com/yKDr2Yt.png)

  

## Kaggle DataSet (bonus):

* Dataset: kaggle_data.csv 
* Number_of_transactions:9684

### Minimum Support = 5 ,Minimum Confidence = 0.5


* 執行時間: 
* Apriori Algorithm:</br>
![](https://i.imgur.com/lTwEyQ1.png)
![](https://i.imgur.com/qFemZ6X.png)

* FP-Growth:</br>
![](https://i.imgur.com/tsp7Yns.png)
![](https://i.imgur.com/h087e0h.png)

 
* 上面幾個例子可以很明顯的看到，FP-Growth演算法的執行時間較少，效率明顯高於Apriori Algorithm，而minimum support越低則需要越長的時間來找association rule。


## 程式驗證:

* 與weka結果相同

  ![](https://i.imgur.com/52bt7mx.png)
 
  ![](https://i.imgur.com/uqjXdwF.png)

