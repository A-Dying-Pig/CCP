<template>
  <div id="app" v-bind:mdate="mdate">
	<CompetitionList v-bind:com='com'></CompetitionList>
  </div>
</template>

<script>
import CompetitionList from './../../components/CompetitionList.vue'
export default {
  name: 'app',
  components: {
	CompetitionList
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
  }
  }
}
</script>

<style>
</style>
