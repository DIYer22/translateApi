# translate API

## 项目特点
1. 支持缓存, 缓存为 csv
1. 支持多线程, 文件和 `df` 读写会自动上锁
1. `__name__ == '__main__'` 即测试



## APIs
支持 Google 翻译网页 API 和百度云翻译 API

Google API :
1. 访问有限制, 过度频繁会被禁止 240s 左右
1. Need to `pip install googletrans`
1. 支持一个 http 请求, 翻译一个 List 

百度 API:
1. 需要使用 appid 和 secretKey (已申请, 也可以在 GitHub 上找)
1. 每个月免费 200万字符, 之后会收 49/百万字符 (后台可查看使用量)
1. 支持多线程 `mapmt`


