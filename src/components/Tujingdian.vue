<template>
  <div class="route-info">
    <h3>途径点</h3>
    <ul>
      <li v-for="(point, index) in waypoints" :key="index">
        {{ point.name }}
        <button @click="removeWaypoint(index)">删除</button>
        <button @click="moveWaypoint(index, -1)" :disabled="index === 0">↑</button>
        <button @click="moveWaypoint(index, 1)" :disabled="index === waypoints.length - 1">↓</button>
      </li>
    </ul>

    <div class="input-box1">
      <label for="waypoint-keyword">添加途径点:</label>
      <input
        type="text"
        id="waypoint-keyword"
        v-model="waypointKeyword"
        placeholder="输入途径点名称或地址"
      />
      <button @click="handleAddWaypoint">添加途径点</button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';

const props = defineProps({
  waypoints: Array,
  addWaypointByKeyword: Function,
  removeWaypoint: Function,
  moveWaypoint: Function,
});

const waypointKeyword = ref("");

const handleAddWaypoint = () => {
  if (waypointKeyword.value) {
    props.addWaypointByKeyword(waypointKeyword.value);
    waypointKeyword.value = ""; // 清空输入框
  } else {
    alert("请输入有效的途径点关键字！");
  }
};
</script>

<style scoped>
.route-info {
  width: 30vw; /* 途径点列表宽度 */
  max-height: 300px; /* 最大高度 */
  overflow-y: auto; /* 允许垂直滚动 */
  padding: 20px;
  background-color: #f5f5f5; /* 背景颜色 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 轻微阴影 */
}

.route-info h3 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #333; /* 标题颜色 */
}

.route-info ul {
  list-style: none; /* 去掉默认列表样式 */
  padding: 0;
  margin: 0;
}

.route-info li {
  display: flex;
  justify-content: space-between;
  align-items: center; /* 垂直对齐 */
  margin-bottom: 10px;
  padding: 10px; /* 内边距 */
  background-color: #fff; /* 白色背景 */
  border: 1px solid #e0e0e0; /* 边框颜色 */
  border-radius: 4px; /* 边框圆角 */
}

.route-info li button {
  padding: 5px 8px;
  cursor: pointer;
  background-color: #007bff; /* 按钮背景颜色 */
  color: white; /* 按钮文字颜色 */
  border: none; /* 去掉按钮边框 */
  border-radius: 4px; /* 按钮圆角 */
  transition: background-color 0.3s; /* 动画效果 */
}

.route-info li button:hover {
  background-color: #0056b3; /* 悬停效果颜色 */
}

.input-box1 {
  margin-top: 20px; /* 与列表的间距 */
  display: flex; /* 使用弹性布局 */
  align-items: center; /* 垂直对齐 */
}

.input-box1 label {
  margin-right: 10px; /* 标签与输入框的间距 */
}

.input-box1 input {
  flex: 1; /* 输入框占据剩余空间 */
  padding: 8px; /* 内边距 */
  border: 1px solid #e0e0e0; /* 边框颜色 */
  border-radius: 4px; /* 边框圆角 */
  margin-right: 10px; /* 输入框与按钮的间距 */
}

.input-box1 button {
  padding: 5px 10px;
  cursor: pointer;
  background-color: #28a745; /* 添加按钮的背景颜色 */
  color: white; /* 添加按钮的文字颜色 */
  border: none; /* 去掉按钮边框 */
  border-radius: 4px; /* 按钮圆角 */
  transition: background-color 0.3s; /* 动画效果 */
}

.input-box1 button:hover {
  background-color: #218838; /* 悬停效果颜色 */
}
</style>
