<template>
  <div>
    <div class="chat-window">
      <div class="messages" ref="messagesContainer">
        <div v-for="entry in messages" :key="entry.id" class="message">
          <!-- Display user input -->
          <div v-if="entry.user_input" class="user-message">
            <div class="message-z">{{ entry.user_input }}</div>
          </div>
          <!-- Display images and breeds if available -->
          <div v-if="entry.images" class="bot-message">
            <vue-slick-carousel v-bind="slickOptions">
              <div v-for="(image, index) in entry.images" :key="index" class="image-container">
                <img :src="image" alt="Dog Image" class="dog-image" @click="enlargeImage(image)" />
                <p class="breed-name">{{ entry.breeds[index] }}</p>
              </div>
            </vue-slick-carousel>
          </div>
          <!-- Display text message or error -->
          <div v-if="entry.text" class="bot-message">
            <div class="message-content">{{ entry.text }}</div>
          </div>
          <div v-if="entry.waiting" class="waiting-message">Waiting for response...</div>
        </div>
      </div>
      <form @submit.prevent="submitMessage" class="user-input">
        <input type="text" v-model="message" placeholder="Please send a number between 1 and 8..." class="input-field">
        <!-- Clear button to clear the input field -->
        <button type="button" class="clear-button" @click="clearInput" v-if="message">X</button>
        <button type="submit" class="send-button">Send</button>
      </form>
    </div>
    <!-- Modal for full-screen image view -->
    <div v-if="selectedImage" class="modal" @click="closeModal">
      <img :src="selectedImage" class="full-screen-image" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import VueSlickCarousel from 'vue-slick-carousel';

export default {
  components: { VueSlickCarousel },
  data() {
    return {
      message: '',
      messages: [],
      selectedImage: null,
      slickOptions: {
        draggable: true,
        dots: true,
        infinite: false,
        speed: 300,
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
  },
  created() {
    this.loadChatHistory();
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        container.scrollTop = container.scrollHeight;
      });
    },
    enlargeImage(image) {
      this.selectedImage = image;
      document.body.classList.add('no-scroll', 'blur-background');

      document.querySelector('.modal').classList.add('active');
    },
    closeModal() {
      this.selectedImage = null;
      document.body.classList.remove('no-scroll', 'blur-background');

      document.querySelector('.modal').classList.remove('active');
    },
    clearInput() {
      this.message = '';
    },
    async loadChatHistory() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/history`);
        this.messages = response.data.map(item => ({
          ...item,
          id: item.timestamp,
        }));
        this.scrollToBottom();
      } catch (error) {
        console.error("Failed to load chat history:", error);
      }

    },
    async submitMessage() {
      const userInput = this.message;
      const tempId = Date.now();
      this.messages.push({
        id: tempId,
        user_input: userInput,
        waiting: true,
      });
      this.scrollToBottom();
      this.message = '';

      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/chat`, {
          user_input: userInput
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });


        this.messages = this.messages.filter(message => message.id !== tempId);


        if (response.data.status === 'success') {
          this.messages.push({
            id: Date.now(),
            user_input: userInput,
            images: response.data.images,
            breeds: response.data.breeds,
            waiting: false
          });
        } else {

          this.messages.push({
            id: Date.now(),
            user_input: userInput,
            text: response.data.message,
            waiting: false
          });
        }
      } catch (error) {
        console.error("Failed to send message:", error);

        this.messages = this.messages.filter(message => message.id !== tempId);

        this.messages.push({
          id: Date.now(),
          user_input: userInput,
          text: "An error occurred while sending the message.",
          waiting: false
        });
      }
      this.scrollToBottom();
    }


  }
}
</script>

<style scoped>
.chat-window {
  max-height: calc(100vh - 40px);
  overflow: hidden;
  width: 80%;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100vh;
  padding: 20px;
}


.messages {
  height: calc(100vh - 40px - 60px);
  overflow-y: auto;
  overflow-x: hidden;
}

.message-z {
  background-color: #0011fc;

  color: #ffffff;

  padding: 16px 20px;
  margin-bottom: 10px;
  border-radius: 18px;
  display: inline-block;
}

.bot-message .message-z {
  background-color: #007bff;
  color: white;
}

.message {
  margin-bottom: 15px;
}

.bot-message .message-content {
  padding: 10px;
  border-radius: 20px;
  margin: 5px;
  display: inline-block;
  background-color: #f1f0f0;
}

.user-message {
  text-align: right;
}

.user-message .message-content {
  background-color: #007bff;
  color: white;
}

.user-input {
  display: flex;
  margin-top: auto;
}

.user-input input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
}

.user-input button {
  margin-left: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.clear-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  color: #999;
  margin-right: 5px;
}

.send-button:hover {
  background-color: #0056b3;
}


.user-input button:hover {
  background-color: #0056b3;
}

.image-container {
  text-align: center;
}

.dog-image {
  width: 80%;
  height: 500px;
  object-fit: cover;
  border-radius: 10px;
}

.breed-name {
  margin-top: 10px;
}


.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  transition: opacity 0.3s ease-in-out;
  opacity: 0;
  pointer-events: none;
}

.modal.active {
  opacity: 1;
  pointer-events: auto;
}

.full-screen-image {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
}


.no-scroll {
  overflow: hidden;
}

.blur-background {
  filter: blur(5px);
}

body.blur-background> :not(.modal) {
  filter: blur(5px);
}

.waiting-message {
  color: #999;
  font-style: italic;
}


/* Custom scrollbar style */
.messages::-webkit-scrollbar {
  width: 8px;
}

.messages::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}

.messages::-webkit-scrollbar-track {
  background-color: #f0f0f0;
}

/* Cursor pointer for images */
.image-container img {
  cursor: pointer;
}
</style>
