# toc-project-what-to-eat

The Linebot for TOC project.


## 吃啥吃啥小幫手

每天都很煩惱要吃什麼嗎 ?

讓小幫手解決您的選擇困難 !


## FSM Diagram
![image](https://github.com/Shulammiteya/toc-project-what-to-eat/blob/main/machine_diagram.png?raw=true)


## 使用說明

*小幫手有四項服務，可分為兩類 : 1. 食物方面的服務、  2. 紀錄。

*第一類：
＊＊若使用者已經想好要吃什麼了，便告訴小幫手『我想吃．．．』，之後便可以看實物照片與使用ｇｏｏｇｌｅ地圖搜尋附近相關的店家；
＊＊若使用者還沒想好要吃什麼，便選擇『小幫手推薦．．．』，小幫手便會根據過去的紀錄來推薦使用者最高機率愛吃的食物。
*第二類：
＊＊吃完飯後，可以用『紀錄一下我吃了什麼』來做紀錄；
＊＊點選『看看過去我吃了什麼』則是可以查看紀錄。

## 使用示範

* 首先，傳任意文字訊息喚醒小幫手，小幫手會傳給使用者flex message，可以快速選擇想要的服務。
	![image](https://github.com/Shulammiteya/toc-project-what-to-eat/blob/main/img/1.png?raw=true)

* 第一項服務：選擇『我想吃．．．』，再選擇想吃的食物（若是選項中沒有使用者想吃的服務，可以直接輸入訊息）接著就可以從flex message看網路上抓取的相關食物照片，每次照片可能不同，因為有在所有抓取到的相關實物照片中隨機選擇，避免使用者覺得每次都一樣照片而感到無聊。而
flex message除了圖片還有兩個按鈕，一個是看原圖，一個是連接到ｇｏｏｇｌｅ　ｍａｐ，方便使用者前往想要的餐廳。
	![image]()

#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### a. Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

#### b. Servo

Or You can use [servo](http://serveo.net/) to expose local servers to the internet.


## Finite State Machine
![fsm](./img/show-fsm.png)

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "go to state1"
		* Reply: "I'm entering state1"

	* Input: "go to state2"
		* Reply: "I'm entering state2"

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
