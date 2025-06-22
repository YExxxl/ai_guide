<template>
    <div class="triangle-container">
        <div class="triangle"></div>
        <div class="triangle-number">{{ number }}</div>
    </div>
    <button @click="handClick">按钮</button>
</template>

<script>
export default {
    data() {
        return {
            number: 1
        };
    },
    methods: {
        handClick() {
            this.number += 1;
        }
    }
};
</script>

<style scoped>
.triangle-container {
    position: relative;
    width: 100px;
    /* 保证三角形容器有足够的宽度 */
    height: 100px;
    /* 保证三角形容器有足够的高度 */
    margin: 0 auto;
    /* 使三角形容器水平居中 */
}

.triangle {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 50px solid transparent;
    border-right: 50px solid transparent;
    border-bottom: 100px solid blue;
}

.triangle-number {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-weight: bold;
    font-size: 20px;
    /* 可选：调整字体大小 */
}
</style>
