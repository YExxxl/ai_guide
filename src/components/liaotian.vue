<template>
  <div id="app">
    <div id="chat-container">
      <div id="messages">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="{
            'user-message': msg.sender === 'user',
            'bot-message': msg.sender === 'bot',
          }"
        >
          {{ msg.text }}
        </div>
      </div>
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="请输入消息..."
      />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userInput: "",
      messages: [],
    };
  },
  methods: {
    async sendMessage() {
      const message = this.userInput.trim();
      if (!message) return;

      console.log("Sending message:", message); // 调试输出

      this.appendMessage(message, "user");
      this.userInput = "";

      try {
        const response = await axios.get("http://8.134.126.203:5000/api/tourist-route/chat", {
          params: { message: message },
        });
        console.log("API响应:", response.data);
        this.appendMessage(response.data.reply, "bot");
      } catch (error) {
        console.error("Error sending message:", error);
        this.appendMessage("对不起，出现错误，请重试。", "bot");
      }
    },
    appendMessage(text, sender) {
      this.messages.push({ text, sender });
    },
  },
};
</script>

<style>
#chat-container {
  width: 100%;
  max-width: 600px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: white;
  padding: 20px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  margin: auto;
}

#messages {
  height: 200px; /* 调整高度以适应容器 */
  overflow-y: scroll;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.user-message {
  background-color: #d1e7ff;
  text-align: right;
  padding: 8px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.bot-message {
  background-color: #e0e0e0;
  text-align: left;
  padding: 8px;
  border-radius: 5px;
  margin-bottom: 10px;
}

input {
  width: calc(100% - 22px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  width: 100%;
}
</style>
