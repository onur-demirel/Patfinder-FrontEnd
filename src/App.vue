<template>
  <ChatBox></ChatBox>
  <Sidebar></Sidebar>
</template>

<script>
import ChatBox from "./components/ChatBox.vue"
import Sidebar from 'primevue/sidebar';

export default {
  name: 'App',
  components: {
    ChatBox,
    Sidebar
    
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;

}
</style>
