# toc-project-what-to-eat

The Linebot for TOC project.


## 吃啥吃啥小幫手

每天都很煩惱要吃什麼嗎 ?

讓小幫手解決您的選擇困難 !


## FSM Diagram
![image](https://github.com/Shulammiteya/toc-project-what-to-eat/blob/main/machine_diagram.png?raw=true)


## 使用說明

小幫手有四項服務，可分為兩類 : 1. 食物方面的服務、  2. 紀錄。

*第一類：
	*若使用者已經想好要吃什麼了，便告訴小幫手『我想吃．．．』，之後便可以看實物照片與使用ｇｏｏｇｌｅ地圖搜尋附近相關的店家；
	*若使用者還沒想好要吃什麼，便選擇『小幫手推薦．．．』，小幫手便會根據過去的紀錄來推薦使用者最高機率愛吃的食物。
*第二類：
	*吃完飯後，可以用『紀錄一下我吃了什麼』來做紀錄；
	*點選『看看過去我吃了什麼』則是可以查看紀錄。

## 使用示範

首先，傳任意文字訊息喚醒小幫手，小幫手會傳給使用者flex message，可以快速選擇想要的服務。
	![image](https://github.com/Shulammiteya/toc-project-what-to-eat/blob/main/img/1.png?raw=true)

選擇『我想吃．．．』，再選擇想吃的食物（若是選項中沒有使用者想吃的服務，可以直接輸入訊息）接著就可以從flex message看網路上抓取的相關食物照片，每次照片可能不同，因為有在所有抓取到的相關實物照片中隨機選擇，避免使用者覺得每次都一樣照片而感到無聊。而flex message除了圖片還有兩個按鈕，一個是看原圖，一個是連接到ｇｏｏｇｌｅ　ｍａｐ，方便使用者前往想要的餐廳。
	![image](https://github.com/Shulammiteya/toc-project-what-to-eat/blob/main/img_fix/%E5%9C%96%E7%89%873.png?raw=true)
	
選擇『看看過去我吃了什麼』，再紀錄幾次檢查是否正確。而從底下的截圖也可以看出，小幫手確實是根據以前吃過的東西來做推薦呢。
	![image](https://github.com/Shulammiteya/toc-project-what-to-eat/blob/main/img_fix/%E5%9C%96%E7%89%874.png?raw=true)
