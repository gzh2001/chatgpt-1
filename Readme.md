# 安装教程

1. 克隆本仓库  
```bash
git clone https://github.com/gzh2001/chatgpt-1.git
```
2. 安装依赖包toml和pychatgpt  
```bash
pip install -r requirements.txt
```
3. 安装依赖包python-telegram-bot
```bash
# Install telegram bot library
git clone https://github.com/python-telegram-bot/python-telegram-bot
cd python-telegram-bot && python setup.py install --user
```
4. 复制`conf.toml.sample`模板并修改生成配置文件`conf.toml`
5. 安装谷歌浏览器
6. (可选)当运行于Headless Linux 服务器上时，需要安装`xvfb`
7. 运行`bot.py`

# 说明
1. 如何获取`cookie`  
参考[https://github.com/terry3041/pyChatGPT#obtaining-session_token](https://github.com/terry3041/pyChatGPT#obtaining-session_token)
# 致谢  
[terry3041/pyChatGPT](https://github.com/gzh2001/chatgpt-1)
