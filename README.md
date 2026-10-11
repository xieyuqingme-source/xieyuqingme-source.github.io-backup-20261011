# 谢雨卿的个人主页

根主页计划地址：<https://xieyuqingme-source.github.io/>。
文章栏目保持：<https://xieyuqingme-source.github.io/articles/>。

这是独立的根站静态文件目录，尚未初始化Git仓库、创建远程仓库或发布。现有`GitHub公开定稿`继续对应`articles`仓库，文件、remote和全部文章网址不变。

首页只包含姓名、有限的公开介绍、文章入口和三篇最新文章。简介依据现有公开“关于我”：谢雨卿（Carl），目前在马来西亚读MBA。没有补造经历、项目或联系方式。

## 本地查看

当前预览：<http://127.0.0.1:8766/>。这里的`/articles/`会只读映射到既有文章网站生成目录，可以从根主页直接进入文章。

重新启动预览：

```text
python scripts/preview_portal.py
```

仅监听127.0.0.1。服务只提供`dist`和相邻`GitHub公开定稿/_site`，不提供整个笔记库；Ctrl+C停止。端口被占用时可加`--port 8767`。若更换文件夹位置，文章预览可以用`--articles-site`指定已有`_site`的绝对路径。

实际桌面/手机渲染、浏览器动态交互暂未验收，遵照用户“暂时不用浏览器自动化”的要求；没有安装浏览器组件。

## 用户手动上线（最小步骤）

1. GitHub账户`xieyuqingme-source`需要一个名称精确为`xieyuqingme-source.github.io`的仓库。若已存在则复用；否则用户自行新建公开仓库。当前本地未找到该仓库，线上根网址核验为404。
2. 在GitHub Desktop克隆该仓库，将本目录的`dist`、`.github`、`scripts`、README和`.gitignore`复制进去。不要复制本地`.local`目录，不改`articles`仓库的remote。
3. 在该仓库的Settings → Pages中，将Source设为GitHub Actions。
4. 用户在GitHub Desktop审阅、commit并Push到main。已准备的`Publish personal home`工作流会上传`dist`并部署根主页。
5. Actions成功后检查根主页和文章入口。文章网站由原`articles`仓库继续独立维护；更换根主页不会改文章地址。

以上步骤未代替用户执行。根网址上线仍需要用户完成仓库和Pages配置。GitHub关于用户站与项目站的区别见[官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)。

## 后续更新

- 内容和最新文章：编辑`dist/index.html`。117篇、116中文/1英文及三篇最新链接是2026-10-11的实际快照；新增文章后可更新这一小段。
- 风格和小屏布局：`dist/assets/portal.css`，沿用文章站的深蓝、青绿与明暗配色。
- 明暗切换：`dist/assets/portal.js`，与文章站使用同一主题偏好键。没有JavaScript时文章和关于链接仍可使用。
- 发布：`.github/workflows/pages.yml`仅发布`dist`。它不会构建、搬运或覆盖文章站。
- 本地静态检查：`python scripts/check_site.py`，以已有文章生成目录核对导航、最新文章链接与日期。

以后可在根主页加入其他真实栏目，目前文章是唯一主要栏目。
