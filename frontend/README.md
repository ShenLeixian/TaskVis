# frontend

要在本地启动，执行命令：

```sh
npm install // 有一个包是npm安装的，保险起见npm install一下
yarn install
yarn start
```



如果`yarn start`时出现了vega-embed的报错，报错信息有如下字样：

```
| mark
| awrap
| async
...(省略)
```

找到报错的包的代码块，将`async`删除即可。

