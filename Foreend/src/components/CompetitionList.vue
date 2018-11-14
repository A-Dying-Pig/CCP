<template>
<div>
<el-table
	:data="comps"
	stripe>
	<el-table-column
		prop="number"
	    label="序号"
	    width="80">
	</el-table-column>
	<el-table-column
		prop="name"
		label="名称"
		width="180">
	</el-table-column>
	<el-table-column
		prop="organizer"
		label="组织者"
		width="180">
	</el-table-column>
	<el-table-column
		prop="information"
		label="信息"
		width="180">
	</el-table-column>
	<el-table-column
		prop="detail"
		label="详情">
	</el-table-column>
</el-table> 
</div>  
</template>

<script>
import Vue from 'vue'
import 'element-ui/lib/theme-chalk/index.css'
import ElementUI from 'element-ui'
Vue.use(ElementUI);

export default{
	data(){
		return{
			comps:[{'number':111,
				'name':'wzw',
				'organizer':'df',		  'information':'info',
				'detail':'de'
				},
				{
				'number':122,
				'name':'wzw',
				'organizer':'df',
				'information':'info',
				'detail':'de'
				}]
			}
		}	
}
</script>

<style>
</style>