<template>
  <div id="app" v-bind:mdate="mdate">
	<MdEdit v-model="msg" title="输入"></MdEdit>
      <el-date-picker v-model="value3" type="datetime" placeholder="选择日期时间" default-time="12:00:00">
      </el-date-picker>
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
      value3:'',
  }},

}
</script>

<style>

</style>
