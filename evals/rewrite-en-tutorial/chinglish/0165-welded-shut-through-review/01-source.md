第一层是逻辑集中: 所有改 status 的路径都必须调 transition_ticket, 代码里绝不允许任何地方直接 UPDATE status, 评审和封装上把这条焊死, 让状态机成为唯一入口.
