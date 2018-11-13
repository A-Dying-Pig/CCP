<template>
  <div id="app" v-bind:mdate="mdate">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
	<DatetimeInput v-model="mdate" title="报名开始日期"></DatetimeInput>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import DatetimeInput from './components/datetime-input.vue'
export default {
  name: 'app',
  components: {
    HelloWorld,
	DatetimeInput
  },
  props:['mdate'],
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
