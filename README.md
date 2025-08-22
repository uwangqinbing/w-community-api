## 1. 项目介绍
一个基于 Flask 框架开发的轻量级社区论坛后端服务，提供用户注册、登录、帖子管理、评论互动及点赞等核心功能的 API 接口，支持前端快速搭建社区类应用。


## 2. 功能特性
- **用户认证**：基于 JWT 的注册与登录功能，支持用户信息管理
- **帖子系统**：支持发布、查询不同类型的帖子（普通帖 / 问题 / 视频帖），支持标签分类
- **互动功能**：实现帖子点赞（含取消点赞）、评论功能，增强用户参与度
- **静态资源**：提供图片、视频等静态资源的访问支持


## 3. 技术栈
- **核心框架**：Flask 2.0+
- **数据库**：SQLite
- **ORM 工具**：Flask-SQLAlchemy
- **身份认证**：Flask-JWT-Extended（基于 JWT 的令牌牌认证）
- **跨域支持**：Flask-CORS（处理前端端跨域请求）
- **开发语言**：Python


## 4. 项目结构w-community-api/
- .gitignore                 # Git忽略文件配置（虚拟环境、IDE配置等）
- README.md                  # 项目说明文档
- requirements.txt           # 项目依赖包清单
- app.py                     # 主程序文件（路由、模型、业务逻辑）
- public/                    # 静态资源目录
  - 1.png
  - 2.png
  - 3.png
- instance/                  # 数据库文件目录
  - forum.db               # SQLite数据库文件

## 5. 数据库模型设计
### 核心数据表

1. **User（用户表）**
   - 字段：`id`(主键)、`username`(用户名，唯一)、`email`(邮箱，登录用，唯一)、`password`(密码)、`avatar`(头像 URL)
   - 关系：一对多关联`Post`（用户发布的帖子），多对多关联`Post`（用户点赞的帖子）

2. **Post（帖子表）**
   - 字段：`id`(主键)、`title`(标题)、`content`(内容)、`authorId`(作者 ID，外键)、`date`(发布时间)、`tags`(标签，逗号分隔)、`image`(图片 URL)、`likes`(点赞数)、`type`(分类：posts/questions/videos)
   - 关系：多对一关联`User`（作者），一对多关联`Comment`（评论）

3. **Comment（评论表）**
   - 字段：`id`(主键)、`post_id`(关联帖子 ID，外键)、`author`(作者名)、`authorAvatar`(作者头像)、`content`(评论内容)、`date`(评论时间)
   - 关系：多对一关联`Post`（所属帖子）

4. **post_likes（点赞关联表）**
   - 功能：维护用户与帖子的多对多点赞关系
   - 字段：`user_id`(用户 ID，外键)、`post_id`(帖子 ID，外键)，联合主键


## 6. API 接口文档

### 静态资源访问
- `GET /public/<path:filename>`  
  访问`public`目录下的静态资源（如图片、视频）


### 用户相关接口

#### 用户注册
- 路径：`POST /api/register`
- 请求体：`{email, password, username?, avatar?}`
- 响应：`{token, user: {id, email, username, avatar}}`
- 说明：`username`默认取邮箱@前的内容，`avatar`默认使用系统头像

#### 用户登录
- 路径：`POST /api/login`
- 请求体：`{email, password}`
- 响应：`{token, user: {id, email, username, avatar}}`
- 说明：验证成功返回 JWT 令牌，用于后续需要认证的接口


### 帖子相关接口

#### 获取帖子列表
- 路径：`GET /api/posts`
- 参数：`type`(可选，筛选分类：posts/questions/videos，默认返回全部)
- 响应：`[{id, title, content, author, date, tags, likes, type, ...}]`

#### 获取帖子详情
- 路径：`GET /api/posts/<post_id>`
- 响应：`{id, title, content, author, comments: [], likes, ...}`
- 说明：返回帖子详情及关联的评论列表

#### 创建帖子
- 路径：`POST /api/posts`
- 请求头：`Authorization: Bearer <token>`（需登录）
- 请求体：`{title, content, tags, type, image?}`
- 响应：`{id, title, ...}`(创建的帖子信息)

#### 帖子点赞/取消点赞
- 路径：`POST /api/posts/<post_id>/like`
- 请求头：`Authorization: Bearer <token>`（需登录）
- 响应：`{likes: 最新点赞数, isLiked: 是否已点赞}`

#### 删除帖子
- 路径：`DELETE /api/posts/<post_id>`
- 请求头：`Authorization: Bearer <token>`（需登录且为作者）
- 响应：`{msg: "帖子删除成功"}`

#### 举报帖子
- 路径：`POST /api/posts/<post_id>/report`
- 请求头：`Authorization: Bearer <token>`（需登录）
- 请求体：`{reason: "举报原因"}`
- 响应：`{msg: "举报成功", report: {...}}`

### 评论相关接口

#### 添加评论
- 路径：`POST /api/posts/<post_id>/comments`
- 请求头：`Authorization: Bearer <token>`（需登录）
- 请求体：`{content}`
- 响应：`{id, author, content, date, ...}`(创建的评论信息)

#### 删除评论
- 路径：`DELETE /api/posts/<post_id>/comments/<comment_id>`
- 请求头：`Authorization: Bearer <token>`（需登录且为评论作者）
- 响应：`{msg: "评论删除成功"}`

#### 举报评论
- 路径：`POST /api/comments/<comment_id>/report`
- 请求头：`Authorization: Bearer <token>`（需登录）
- 请求体：`{reason: "举报原因"}`
- 响应：`{msg: "举报成功", report: {...}}`

## 7. 快速开始

### 环境准备
1. 克隆仓库并进入项目目录
   ```bash
   git clone <仓库地址>
   cd w-community-api
   ```

2. 创建并激活虚拟环境
   ```bash
   # 创建虚拟环境
   python -m venv venv

   # Windows激活
   venv\Scripts\activate
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```


### 运行服务python app.py服务将启动在 `http://localhost:5000`

## 8. 注意事项
- 开发环境使用 SQLite 数据库，生产环境建议迁移至 MySQL/PostgreSQL
- 当前密码以明文存储，生产环境需添加加密处理（如 bcrypt）
- JWT 密钥（`JWT_SECRET_KEY`）需在生产环境更换为随机安全字符串
- 跨域配置默认允许`http://localhost:5173`，如需修改可调整`CORS(app, origins=...)`参数
    