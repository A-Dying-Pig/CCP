<template>
  <div id="app" v-bind:mdate="mdate">
	<MdEdit v-model="msg" title="输入"></MdEdit>
  </div>
</template>

<script>
import MdEdit from './../../components/MdEdit.vue'
export default {
  name: 'app',
  components: {
	MdEdit
  },
  props:['mdate'],
  data:function(){
  return {
  msg:'mainapp',
  com:{
  'number':111,
  'name':'wzw',
  'organizer':'df',
  'information':'info',
  'detail':'de'
  },
  }},

}
</script>

<style>
</style>
