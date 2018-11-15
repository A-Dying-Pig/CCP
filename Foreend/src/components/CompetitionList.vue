<template>
<div class="competitionList">
<div class="banner">{{ title-type }}</div>
<el-radio-group v-model="comtypes">
<el-radio v-for="type in comtypes">{{type.label}}
</el-radio>
</el-radio-group>


<el-row :gutter=20>
<el-col :offset=5>
<el-form-item label="比赛类型" prop="comtype">
    <el-radio-group v-model="info.comtype">
        <el-radio v-for="type in comtypes" v-bind:label="type.label" v-bind:value="type.value" :key="item.key"></el-radio>
    </el-radio-group>
</el-form-item>
</el-col>
</el-row>


<div class="banner">{{ title-list }}</div>
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

export default{
	props:['title-type','title-list','type_choose'],
	data:function(){
		return{
			type:this.type_choose
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