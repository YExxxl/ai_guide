<template>
  <div class="about">
    <!-- 地图容器 -->
    <div class="content" id="container"></div>

    <div class="map-control">
      <!-- 用户输入起点关键字 -->
      <div class="input-box">
        <label for="start-keyword">需求输入:</label>
        <input
          type="text"
          id="start-keyword"
          v-model="startKeyword"
          placeholder="请输入旅游路线需求"
        />
        <button @click="updateStartPointByKeyword">搜索</button>
      </div>

      <!-- 途径点列表 -->
      <div class="route-info">
        <h3>途径点</h3>
        <ul v-if="waypoints.length > 0">
          <li v-for="(point, index) in waypoints" :key="index">
            <span>{{ point.name }}</span>
            <button @click="removeWaypoint(index)">删除</button>
            <button @click="moveWaypoint(index, -1)" :disabled="index === 0">
              ↑
            </button>
            <button
              @click="moveWaypoint(index, 1)"
              :disabled="index === waypoints.length - 1"
            >
              ↓
            </button>
          </li>
        </ul>
        <p v-else></p> <!-- 没有途径点时 -->

        <!-- 新的途径点输入框 -->
        <div class="input-box1">
          <label for="waypoint-keyword">添加途径点:</label>
          <input
            type="text"
            id="waypoint-keyword"
            v-model="waypointKeyword"
            placeholder="输入途径点名称或地址"
          />
          <button @click="addWaypointByKeyword">添加</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";
import axios from "axios";

// 高德地图的安全配置
window._AMapSecurityConfig = {
  securityJsCode: "43c2adf315b69c854c47bad7f98fe072",
};

let map = null;
let driving = null;
let Amap2 = null;
let placeSearch = null; // 地点搜索实例
let geocoder = null; // 地理编码实例

// 起点关键字
const startKeyword = ref(""); // 用户输入的起点关键字
const waypointKeyword = ref(""); // 用户输入的途径点关键字
const startLat = ref(23.6617); // 起点纬度
const startLng = ref(116.6309); // 起点经度

// 途径点数据
const waypoints = ref([]);

// 获取地图和地理编码服务
const getMap = () => {
  AMapLoader.load({
    key: "d19ddce901bfbac5c9a43ad5d42e2ebc",
    version: "1.4.15",
    plugins: [
      "AMap.InfoWindow",
      "AMap.PlaceSearch",
      "AMap.Geolocation",
      "AMap.Geocoder",
      "AMap.Driving",
      "AMap.Transfer",
      "AMap.Walking",
      "AMap.Riding",
    ],
  })
    .then((AMap) => {
      map = new AMap.Map("container", {
        zoom: 11,
        center: [startLng.value, startLat.value], // 初始位置
      });
      driving = new AMap.Driving({ map: map });
      placeSearch = new AMap.PlaceSearch();
      geocoder = new AMap.Geocoder(); // 初始化地理编码实例
      Amap2 = AMap;
    })
    .catch((e) => console.log(e));
};

// 使用地理编码 API 获取经纬度
const getCoordinatesByKeyword = (keyword) => {
  return new Promise((resolve, reject) => {
    placeSearch.search(keyword, (status, result) => {
      if (status === "complete" && result.poiList.pois.length > 0) {
        const poi = result.poiList.pois[0];
        resolve({ lat: poi.location.lat, lng: poi.location.lng });
      } else {
        reject("未找到该地点");
      }
    });
  });
};

// 更新起点位置
const updateStartPointByKeyword = () => {
  if (startKeyword.value) {
    placeSearch.search(startKeyword.value, (status, result) => {
      if (status === "complete" && result.poiList.pois.length > 0) {
        const poi = result.poiList.pois[0];
        startLat.value = poi.location.lat;
        startLng.value = poi.location.lng;
        map.setCenter([startLng.value, startLat.value]);
        waypoints.value = []; // 清空途径点数据
        fetchTouristRoutes(startKeyword.value).then(() => {
          planRoute(); // 获取并添加途径点后规划路线
        });
      } else {
        alert("未找到该起点，请重新输入！");
      }
    });
  } else {
    alert("请输入有效的起点关键字！");
  }
};

// 获取后端的景点数据
const fetchTouristRoutes = async (place_name) => {
  if (!place_name) {
    console.error("景点名称不能为空");
    return;
  }

  try {
    const response = await axios.get(`http://8.134.126.203:5000/api/tourist-route/景点名`);
    const touristRoute = response.data.tourist_route; // 获取建议的旅游路线
    console.log("从后端获取的景点数据:", touristRoute); // 调试信息

    // 清空原有途径点并更新为新获取的推荐地点
    waypoints.value = touristRoute.split('\n').map(route => ({
      name: route.trim(),
      lat: null,
      lng: null
    }));

    // 更新经纬度的函数
    await updateWaypointCoordinates();
  } catch (error) {
    console.error("获取景点数据失败:", error);
  }
};

// 更新所有途径点的经纬度
const updateWaypointCoordinates = async () => {
  for (let i = 0; i < waypoints.value.length; i++) {
    if (waypoints.value[i].name) { // 确保途径点名称不为空
      try {
        const coords = await getCoordinatesByKeyword(waypoints.value[i].name);
        waypoints.value[i].lat = coords.lat;
        waypoints.value[i].lng = coords.lng;
      } catch (error) {
        console.error(error);
        waypoints.value[i].lat = null;
        waypoints.value[i].lng = null;
      }
    }
  }
};

// 根据关键词添加途径点
const addWaypointByKeyword = () => {
  if (waypointKeyword.value) {
    console.log("Adding waypoint:", waypointKeyword.value); // 调试信息
    placeSearch.search(waypointKeyword.value, (status, result) => {
      console.log("Search Status:", status); // 调试信息
      console.log("Search Result:", result); // 调试信息

      if (status === "complete" && result.poiList.pois.length > 0) {
        const poi = result.poiList.pois[0];
        const newWaypoint = {
          lat: poi.location.lat,
          lng: poi.location.lng,
          name: poi.name || "新途径点",
        };

        // 检查是否新途径点已存在，避免重复
        const exists = waypoints.value.some(
          (point) => point.name === newWaypoint.name
        );
        if (!exists) {
          waypoints.value.push(newWaypoint);
          waypointKeyword.value = ""; // 清空输入框
          updateWaypointCoordinates(); // 更新新添加途径点的经纬度
          planRoute(); // 重新规划路线
        } else {
          alert("该途径点已经存在！");
        }
      } else {
        alert("未找到该途径点，请重新输入！");
      }
    });
  } else {
    alert("请输入有效的途径点关键字！");
  }
};

// 规划路线
const planRoute = () => {
  const end = [startLng.value, startLat.value]; // 终点坐标
  const start = [startLng.value, startLat.value];

  // 将途径点转换为 AMap.LngLat 对象
  const waypointLngLat = waypoints.value.map(
    (point) => new Amap2.LngLat(point.lng, point.lat)
  );

  driving.search(
    new Amap2.LngLat(start[0], start[1]),
    new Amap2.LngLat(end[0], end[1]),
    { waypoints: waypointLngLat },
    function (status, result) {
      if (status === "complete") {
        console.log("路线规划成功");
      } else {
        console.log("路线规划失败：" + result.info);
      }
    }
  );
};

// 删除途径点
const removeWaypoint = async (index) => {
  waypoints.value.splice(index, 1);
  await updateWaypointCoordinates(); // 删除后更新途径点名称
  planRoute(); // 重新规划路线
};

// 移动途径点
const moveWaypoint = async (index, direction) => {
  const newIndex = index + direction;
  if (newIndex >= 0 && newIndex < waypoints.value.length) {
    const tmp = waypoints.value[index];
    waypoints.value[index] = waypoints.value[newIndex];
    waypoints.value[newIndex] = tmp;
    await updateWaypointCoordinates(); // 排序后更新途径点名称
    planRoute(); // 重新规划路线
  }
};

onMounted(() => {
  getMap();
});
</script>

<style lang="less">
@color1: blue;

.content {
  width: 100vw; /* 地图容器全宽 */
  height: 100vh; /* 地图容器全高 */
  position: fixed;
  top: 0;
  left: 0;
  background-color: @color1;
  display: inline-block;
}

.map-control {
  background-color: #ffffff;
}

.route-info {
  width: 30vw; /* 途径点列表宽度 */
  height: auto; /* 自适应高度 */
  padding: 20px;
  overflow: hidden; /* 改为隐藏，去掉滚动条 */
  position: absolute;
  top: 80px; /* 距离顶部一定高度以避免遮挡起点输入框 */
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  border:#dcdcdc 2px solid;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  left: 20px; /* 距离左边的高度 */
}

.route-info h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.route-info ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.route-info li {
  display: flex;
  justify-content: space-between;
  align-items: center; /* 垂直居中对齐按钮 */
  margin-bottom: 10px;
}

/* 加了span啊啊아아아아아아아아아아아아 */
.route-info span {
  flex-grow: 1; /* 让景点名部分占据剩余空间 */
  text-align: left; /* 确保景点名靠左 */
}

.route-info button {
  padding: 5px 10px;
  cursor: pointer;
  margin-left: 25px;
  width: 50px;
  text-align: center; /* 按钮文字居中 */
}

/* 优化添加途经点输入框和按钮的外观aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa */
.input-box1 {
  display: flex;
  align-items: center;
  gap: 10px; /* 调整间距 */
  margin-top: 20px;
}

.input-box1 label {
  margin-right: 10px;
}

.input-box1 input {
  padding: 8px 12px;
  border-radius: 10px; /* 圆角 */
  border: 1px solid #ccc; /* 边框颜色 */
  font-size: 14px;
  outline: none; /* 去除浏览器默认的聚焦样式 */
}

.input-box1 input:focus {
  border-color: #007bff; /* 聚焦时的边框颜色 */
  box-shadow: 0 0 3px rgba(0, 123, 255, 0.5); /* 聚焦时的阴影效果 */
}

.input-box1 button {
  padding: 8px 10px;
  background-color: #61d2a3; /* 按钮背景色 */
  color: white;
  border: none;
  border-radius: 10px; /* 圆角 */
  font-size: 14px;
  cursor: pointer;
  justify-content: center;
}

/* 鼠标悬停按钮效果 */
.input-box1 button:hover {
  background-color: #92eb8cce; /* 鼠标悬停时按钮背景色 */
  transform: scale(1.05); /* 鼠标悬停时按钮放大 */
}

/* 按钮点击效果 */
.input-box1 button:active {
  background-color: #61d2a3; /* 按钮背景色 */
  transform: scale(0.98); /* 按钮点击时的缩小效果 */
}

.input-box {
  position: absolute; /* 设置为绝对定位 */
  width: 30vw; /* 宽度 */
  top: 20px; /* 距离顶部的高度 */
  left: 20px; /* 距离左边的高度 */
  z-index: 1000; /* 确保输入框在地图的上方 */
  padding: 20px;
  background-color: #ffffff;
  border-top:#dcdcdc 2px solid;
  border-left:#dcdcdc 2px solid;
  border-right:#dcdcdc 2px solid;
  border-top-left-radius: 10px; /* 圆角 */
  border-top-right-radius: 10px; /* 圆角 */
  display: flex;
  align-items: center;
  gap: 10px; /* 调整间距 */
}

.input-box label {
  margin-right: 10px;
}

.input-box input {
  padding: 8px 12px;
  border-radius: 10px; /* 圆角 */
  border: 1px solid #ccc; /* 边框颜色 */
  font-size: 14px;
  outline: none; /* 去除浏览器默认的聚焦样式 */
}

.input-box button {
  padding: 8px 10px;
  background-color: #61d2a3; /* 按钮背景色 */
  color: white;
  border: none;
  border-radius: 10px; /* 圆角 */
  font-size: 14px;
  cursor: pointer;
  justify-content: center;
}

</style>
