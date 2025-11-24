<template>
  <div class="fixed bottom-6 right-6 z-50 flex flex-col items-end font-sans">
    <transition
      enter-active-class="transition ease-out duration-300 transform"
      enter-from-class="opacity-0 translate-y-10 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition ease-in duration-200 transform"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-10 scale-95"
    >
      <div
        v-if="isOpen"
        class="w-[360px] h-[500px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden mb-4"
      >
        <div class="bg-[#008659] text-white px-4 py-3 flex items-center justify-between shrink-0">
          <div class="flex items-center gap-2">
            <SvgItem name="comment-dots" size="5" class="text-white" filled />
            <h3 class="font-bold text-lg">Meetro 聊天室</h3>
          </div>
          <button @click="isOpen = false" class="hover:bg-white/20 p-1 rounded-full transition">
            <SvgItem name="x" size="5" class="text-white" />
          </button>
        </div>

        <div v-if="!currentChat" class="flex-grow overflow-y-auto bg-gray-50">
          <div
            v-for="chat in chatList"
            :key="chat.id"
            @click="selectChat(chat)"
            class="p-3 flex items-center gap-3 hover:bg-white cursor-pointer border-b border-gray-100 transition"
          >
            <div
              class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold border-2 border-white shadow-sm"
              :class="chat.isSender ? 'bg-[#008659]' : 'bg-[#E3002C]'"
            >
              {{ chat.name[0] }}
            </div>

            <div class="flex-grow overflow-hidden">
              <div class="flex justify-between items-center mb-1">
                <span class="font-bold text-gray-800 text-sm">{{ chat.name }}</span>
                <span
                  class="text-[10px] px-1.5 py-0.5 rounded text-white"
                  :class="chat.isSender ? 'bg-[#008659]' : 'bg-[#E3002C]'"
                >
                  {{ chat.isSender ? '發送方' : '選擇方' }}
                </span>
              </div>
              <p class="text-xs text-gray-500 truncate">{{ chat.lastTime }}</p>
            </div>
          </div>

          <div
            v-if="chatList.length === 0"
            class="flex flex-col items-center justify-center h-full text-gray-400 p-6 text-center"
          >
            <p class="text-sm">目前沒有聊天記錄</p>
            <p class="text-xs mt-1">快去接受邀約開啟對話吧！</p>
          </div>
        </div>

        <div v-else class="flex-grow flex flex-col bg-gray-50">
          <div class="px-3 py-2 bg-white border-b border-gray-200 flex items-center gap-2 shrink-0">
            <button @click="currentChat = null" class="p-1 hover:bg-gray-100 rounded-full">
              <span class="text-gray-600 font-bold">←</span>
            </button>
            <span class="font-bold text-gray-800 text-sm">{{ currentChat.name }}</span>
          </div>

          <div ref="messagesContainer" class="flex-grow overflow-y-auto p-3 space-y-3">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="flex w-full"
              :class="msg.isMe ? 'justify-end' : 'justify-start'"
            >
              <div
                class="max-w-[80%] px-3 py-2 rounded-2xl text-sm shadow-sm"
                :class="
                  msg.isMe
                    ? 'bg-[#008659] text-white rounded-tr-none'
                    : 'bg-white text-gray-800 rounded-tl-none'
                "
              >
                {{ msg.text }}
              </div>
            </div>
          </div>

          <div class="p-3 bg-white border-t border-gray-200 shrink-0">
            <input
              v-model="newMessage"
              @keyup.enter="sendMessage"
              type="text"
              placeholder="| 回覆訊息......"
              class="w-full bg-gray-100 rounded-full px-4 py-2 text-sm focus:ring-2 focus:ring-[#008659] focus:bg-white outline-none transition"
            />
          </div>
        </div>
      </div>
    </transition>

    <button
      @click="toggleChat"
      class="group flex items-center justify-center px-6 py-3 bg-[#FF8A80] text-white font-bold rounded-full shadow-lg hover:bg-[#ff5252] hover:scale-105 transition-all duration-300"
    >
      <span class="mr-2 text-xl group-hover:animate-bounce">💬</span>
      <span class="text-base">聊天室</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import SvgItem from '@/components/icons/SvgItem.vue'

// 資料介面
interface ChatUser {
  id: number
  name: string
  isSender: boolean // 用來顯示綠色/紅色標籤
  lastTime: string
}

interface Message {
  id: number
  text: string
  isMe: boolean
}

// 狀態
const isOpen = ref(false)
const currentChat = ref<ChatUser | null>(null)
const newMessage = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// 模擬資料
const chatList = ref<ChatUser[]>([
  { id: 1, name: '周彥廷', isSender: true, lastTime: '2025/11/12 12:53' },
  { id: 2, name: '辛治翰', isSender: true, lastTime: '2025/11/12 12:53' },
  { id: 3, name: '王乙珺', isSender: false, lastTime: '2025/11/12 12:53' },
  { id: 4, name: '蔡雨恩', isSender: false, lastTime: '2025/11/12 12:53' },
  { id: 5, name: '許如欣', isSender: true, lastTime: '2025/11/12 12:53' },
])

const messages = ref<Message[]>([
  { id: 1, text: '你好！請問約幾點方便？', isMe: false },
  { id: 2, text: '下午兩點公館站見！', isMe: true },
])

// 方法
const toggleChat = () => {
  isOpen.value = !isOpen.value
}

const selectChat = (chat: ChatUser) => {
  currentChat.value = chat
  // 這裡應該去 fetch 該聊天室的訊息
  scrollToBottom()
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  messages.value.push({
    id: Date.now(),
    text: newMessage.value,
    isMe: true,
  })
  newMessage.value = ''
  await scrollToBottom()
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>
