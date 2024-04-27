# 北京交通大学最帅的小组
需要克隆，请使用命令`git clone --recurse-submodules https://github.com/shixunIV/BackEnd.git`递归的克隆
Web端开发请在Web子目录下
注意git提交规范！提交规范详见下面链接`https://juejin.cn/post/6844903793033756680`
feat - 新功能 feature
fix - 修复 bug
docs - 文档注释
style - 代码格式(不影响代码运行的变动)
refactor - 重构、优化(既不增加新功能，也不是修复bug)
perf - 性能优化
test - 增加测试
chore - 构建过程或辅助工具的变动
revert - 回退
build - 打包


# 项目说明
一个医疗知识图谱,可以基于知识图谱进行问答等内容.
注意项目所有代码需要再BACKEND目录下运行!否则相对路径会有问题
需求文档：`https://ux1cafcdniz.feishu.cn/docx/GTacdliJLo69P8xrdM8c7OK5nMb`


# 系统需求
## 配置相关
需要安装python与npm/nodejs, 数据库采用sqlite,省去配置步骤,图数据库采用neo4j,用于构建数据库
在config.yml中配置自己的neo4j数据库等本地信息

## 运行须知
电脑安装有golang python pnpm nodejs
首先去web目录底下运行`pnpm i`下载依赖，然后去gateway下运行`go mod tidy`安装依赖

# 目录结构
前端实现在web目录下,不需要实现Android端,使用React进行开发,给我开发的好看一些@hkjgsfgh
运行`python main.py`直接运行多个目录

## gateway
**用于转发请求**
是防火墙，各个组件均需要屏蔽来自非gateway的请求（127.0.0.1）
使用go撰写，主要的用处是转发，作为多个微服务组件的统一入口。

## neo4j
**注意使用中间件屏蔽非本地的访问**
图数据库微服务，主要用处是进行图数据库的查询等操作。


## neo4jInit
图数据库构建脚本，用于构建图数据库，具体流程如下：
通过多线程爬虫爬取寻医问药网站的所有疾病顺序：
```python
basic_url = "http://jib.xywy.com/il_sii/gaishu/%s.htm" % page  # 疾病描述
cause_url = "http://jib.xywy.com/il_sii/cause/%s.htm" % page  # 疾病起因
prevent_url = "http://jib.xywy.com/il_sii/prevent/%s.htm" % page  # 疾病预防
symptom_url = "http://jib.xywy.com/il_sii/symptom/%s.htm" % page  # 疾病症状
inspect_url = "http://jib.xywy.com/il_sii/inspect/%s.htm" % page  # 疾病检查
treat_url = "http://jib.xywy.com/il_sii/treat/%s.htm" % page  # 疾病治疗
food_url = "http://jib.xywy.com/il_sii/food/%s.htm" % page  # 饮食治疗
```
从网页中解析疾病相关数据，由于疾病是格式化数据，所以不需要过多的转换。爬取的数据全部存放在`data/spider_data`目录下以json格式存放。
然后对数据进行清洗，相关代码在data_prepare中，主要使用jieba库将一些黏连的数据切分开以及格式化数据。
导出所有的病例名称到disease.txt为了切割数据
然后使用build_graph.py构建图数据库，时间大概需要一个小时，需要耐心等待

## Patient
用与管理病人

## doctor
用于管理医生

