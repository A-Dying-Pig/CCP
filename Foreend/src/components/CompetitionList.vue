<template>
<div class="competitionList banner">
<div>{{ info.type }}</div>
    <p></p>
    <el-radio-group v-model="info.typename" label="比赛类型" @change="submittype">
        <el-radio v-for="type in comtypes"
        :label="type.value"
        :key="type.label">
        {{type.label}}
        </el-radio>
        <el-radio label="全选">全选</el-radio>
    </el-radio-group>
    <p></p>

<div>{{ info.list }}</div>
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
        <template slot-scope="scope">
            <a href="/api/competition/detail?contestId=contestId">
                <el-button
                    type="text"
                    size="small">
                    查看
                </el-button>
            </a>
        </template>
    </el-table-column>
</el-table>
    <p></p>

	<div class="block page">
		<span class="demonstration"></span>
        <el-col>
            <el-pagination @current-change="HandlePageChange"
                           @prev-click="HandlePageChange"
                           @next-click="HandlePageChange"
                           v-model="page.pagenumber"
                           layout="prev,pager,next"
                           :total=page.total></el-pagination>
        </el-col>

	</div>

</div>
</template>

<script>
import Vue from 'vue'
import 'element-ui/lib/theme-chalk/index.css'
import ElementUI from 'element-ui'
Vue.use(ElementUI);

import axios from 'axios'

export default{
	props:['finfo','fpage'],
	data:function(){
		return{
			info:this.finfo,
            page:this.fpage,
			comps:[{'number':111,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':1
				},
				{
                    'number':122,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':2
				},
                {'number':111,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':1
                },
                {
                    'number':122,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':2
                },
                {'number':111,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':1
                },
                {
                    'number':122,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':2
                },
                {'number':111,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':1
                },
                {
                    'number':122,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':2
                },
                {'number':111,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':1
                },
                {
                    'number':122,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':2
                },
                {'number':111,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':1
                },
                {
                    'number':122,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':2
                },
                {'number':111,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':1
                },
                {
                    'number':122,
                    'name':'wzw',
                    'organizer':'df',
                    'information':'info',
                    'contestId':2
                }],
				comtypes:[
                {label:'微信小程序',name:'type',value:'weixin'},
                {label:'web开发',name:'type',value:'web'}]
			}
		},
	methods:{
		submittype(val)
        {
           this.finfo.typename=val;
			axios.post('/CompetitionList', { CompetitionType:val,pageNumber:'1' });
		},
        HandlePageChange(val)
        {
            axios.post('/CompetitionList',{ CompetitionType:this.finfo.typename,pageNumber:val })
        }
	},
    mounted:function(){
	    this.submittype("全选");
    }
}
</script>

<style>
.banner{
    font-size:large;
    text-align: left;
    font-family: "PingFang SC";
  }
    .page{
        text-align: center;
    }
</style>