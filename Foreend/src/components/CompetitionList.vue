<template>
<div class="competitionList">
<div class="banner">{{ info.type }}</div>
<el-radio-group v-model="info.typename" label="比赛类型">
    <el-radio v-for="type in comtypes" :label="type.value"  
    :key="type.label">
    {{type.label}}
    </el-radio>
</el-radio-group>


<div class="banner">{{ info.list }}</div>
<el-table
	:data="comps"
	stripe>
	<el-table-column
			prop="number"
			label="序号"
			width="180">
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
		width="580">
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

import axios from 'axios'

export default{
	props:['finfo'],
	data:function(){
		return{
			info:this.finfo,			
			comps:[{'number':111,
				'name':'wzw',
				'organizer':'df',		  
				'information':'info',
				'detail':'de'
				},
				{
				'number':122,
				'name':'wzw',
				'organizer':'df',
				'information':'info',
				'detail':'de'
				}],
				comtypes:[
                {label:'微信小程序',name:'type',value:'weixin'},
                {label:'web开发',name:'type',value:'web'}]
			}
		},
	methods:{
		submittype(comtype)
		{	
			axios.post('/CompetitionList', {CompetitionType:this.comtype})
		} 
	}	
}
</script>

<style>
.banner{
    font-size:20px;
    text-align: left;
    font-family: "PingFang SC";
    padding: 70px 0px 0px 0px;
    text-weight:bold;
  }
</style>