# 更新日志
## 1/13 前
1. 将`Scene`类作为最小单位，`update()`， `render()`等在`Scene`中进行，方便模块化增加场景，减少对`Gamemanager`的修改
2. `Attributes`增加抽象标签`Collidable`(可碰撞)， `MonoBehavior`(update()行为)，`Renderable`(可渲染，不同于`Sprite`，有`render_index`以定义渲染优先级)，不同标签代表不同功能
3. 增加工具类`Math`进行向量计算
4. 简化`Scene`逻辑，每个场景有一个`_objects`列表存储所有游戏物体，根据游戏物体的标签`Attributes`来调用其对应函数
5. 增加生成器模组`generator`，全局可以引用，作用是把实例添加到当前场景的`_objects`列表中

## 1/13
1. 添加障碍物，障碍物不会生成在指定物体周围（玩家，传送门等）
2. 添加碰撞检测系统：只要把collidable类的is_rigid设为True，位移方法从self.rect.move_ip（x,y）改为用self.velocity=(x,y)即可
3. 手感优化：把玩家的碰撞框改小了，图像大小不变，玩家不容易被子弹打到/不容易被障碍物卡住