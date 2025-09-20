<template>
  <div class="chat-window">
    <div class="chat-header">
      <h3>行程聊天</h3>
      <button class="btn-close" @click="closeChat">×</button>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="message in messages"
        :key="message.id"
        class="message"
        :class="{ 'own-message': message.sender_id === currentUserId }"
      >
        <div class="message-sender">{{ message.sender_name }}</div>
        <div class="message-content">{{ message.content }}</div>
        <div class="message-time">{{ formatTime(message.created_at) }}</div>
      </div>
    </div>
    
    <div class="chat-input">
      <input
        v-model="newMessage"
        type="text"
        placeholder="输入消息..."
        @keyup.enter="sendMessage"
        :disabled="sending"
      />
      <button @click="sendMessage" :disabled="sending || !newMessage.trim()">
        {{ sending ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getChatMessages, sendChatMessage } from '../api/chatService'

const props = defineProps<{
  tripId: number
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const authStore = useAuthStore()
const currentUserId = authStore.user?.id

const messages = ref<any[]>([])
const newMessage = ref('')
const sending = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)

// 获取聊天消息
const fetchMessages = async () => {
  try {
    const response = await getChatMessages(props.tripId)
    messages.value = response.messages
    scrollToBottom()
  } catch (error) {
    console.error('获取聊天消息失败:', error)
  }
}

// 发送消息
const sendMessage = async () => {
  if (!newMessage.value.trim() || sending.value) {
    return
  }
  
  sending.value = true
  try {
    const response = await sendChatMessage(props.tripId, newMessage.value.trim())
    messages.value.push(response)
    newMessage.value = ''
    scrollToBottom()
  } catch (error: any) {
    alert(error.message || '发送消息失败')
  } finally {
    sending.value = false
  }
}

// 格式化时间
const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 关闭聊天窗口
const closeChat = () => {
  emit('close')
}

// WebSocket连接
let ws: WebSocket | null = null

const connectWebSocket = () => {
  // 获取认证token
  const token = localStorage.getItem('token')
  if (!token) {
    return
  }
  
  // 创建WebSocket连接
  const wsUrl = `ws://localhost:8001/ws/trips/${props.tripId}?token=${token}`
  ws = new WebSocket(wsUrl)
  
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data)
    messages.value.push(message)
    scrollToBottom()
  }
  
  ws.onclose = () => {
    // 连接关闭时尝试重新连接
    setTimeout(connectWebSocket, 5000)
  }
}

// 组件挂载时获取消息并连接WebSocket
onMounted(() => {
  fetchMessages()
  connectWebSocket()
})

// 组件卸载时关闭WebSocket连接
onUnmounted(() => {
  if (ws) {
    ws.close()
  }
})
</script>

<style scoped>
.chat-window {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #42b883;
  color: white;
}

.chat-header h3 {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-messages {
  height: 300px;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.message {
  max-width: 80%;
  padding: 0.5rem;
  border-radius: 8px;
  background-color: #f1f1f1;
}

.message.own-message {
  align-self: flex-end;
  background-color: #42b883;
  color: white;
}

.message-sender {
  font-weight: bold;
  font-size: 0.8rem;
  margin-bottom: 0.25rem;
}

.message-content {
  word-wrap: break-word;
}

.message-time {
  font-size: 0.7rem;
  text-align: right;
  margin-top: 0.25rem;
  opacity: 0.8;
}

.chat-input {
  display: flex;
  padding: 1rem;
  border-top: 1px solid #ddd;
  background: #f8f9fa;
}

.chat-input input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 0.5rem;
}

.chat-input button {
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chat-input button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>