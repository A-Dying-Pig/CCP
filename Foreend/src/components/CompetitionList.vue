<template>
<div class="competitionList">
    <div class="enroll-info-spliter">{{ info.type }}</div>
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

    <div  class="enroll-info-spliter">{{ info.list }}</div>
	<el-row class="list_wrapper">
        <el-col v-for="com in comps" :key="com.key" class="list_item">
            <img :src="com.img_url" class="item_pic">
            <div class="item_content_wrapper">
                <h2><span>{{com.title}}</span></h2>
                <p class="item_desc">{{com.intro}}</p>
                <a :href="'/detail?contestid='+com.contestid" >
                    <el-button type="text" size="small" class="button">详情</el-button>
                </a>
            </div>
        </el-col>
    </el-row>
    <p></p>

	<div class="block page_select">
		<span class="demonstration"></span>
        <el-col>
            <el-pagination @current-change="HandlePageChange"
                           @prev-click="HandlePageChange"
                           @next-click="HandlePageChange"
                           v-model="current_page_num"
                           layout="prev,pager,next"
                           :total="total_page_num"></el-pagination>
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
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.headers.common = {
  'X-CSRFToken':document.querySelector('#csrf-token input').value,
    'X-Requested-With': 'XMLHttpRequest'
};
export default{
	props:['finfo','current_page_num','total_page_num','array'],
	data:function(){
		return{
			info:this.finfo,
			comps:[
                {'title':111,
                    'intro':'wzw',
                    'img_url':'df',
                },
                {'title':111,
                    'intro':'wzw',
                    'img_url':'df',
                },
                {'title':111,
                    'intro':'wzw',
                    'img_url':'df',
                },
                {'title':111,
                    'intro':'wzw',
                    'img_url':'df',
                },
                {'title':111,
                    'intro':'wzw',
                    'img_url':'df',
                },
                {'title':111,
                    'intro':'wzw',
                    'img_url':'df',
                },
                {'title':111,
                    'intro':'wzw',
                    'img_url':'df',
                }],
				comtypes:[
                {label:'微信小程序',name:'type',value:'weixin'},
                {label:'web开发',name:'type',value:'web'}]
			}
		},
	methods:{
		submittype(val)
        {
            let self = this;
            self.finfo.typename=val;
			axios.post('/api/competition/list', { type:val,pageNum:'1' }).then(function (response) {
               self.comps = response.data.array;
            })
		},
        HandlePageChange(val)
        {
            axios.post('/api/competition/list',{ type:this.finfo.typename,pageNum:val }).then(function (response) {
                self.comps = response.data.array
            })
        }
	},
    mounted:function(){
	    this.submittype("全选");
    }
}
</script>

<style>
    .enroll-info-spliter{
        font-size: 20px;
        font-family: "PingFang SC";
        margin-top: 30px;
        margin-bottom: 30px;
    }
    .list_wrapper {
        padding: 0 24px 24px;
        list-style: none;
        text-decoration : none;
    }
    .list_item {
        word-break: break-all;
        color: inherit;
        width: 100%;
        padding: 24px 16px;
        border-top: 1px solid #f7f7f7;
        display: flex;
        align-items: center;
        text-decoration : none;
    }
    .item_pic {
        align-self: flex-start;
        display: block;
        flex-grow: 0;
        flex-shrink: 0;
        width: 130px;
        height: 130px;
        margin-right: 36px;
        border-radius: 4px;
    }
    .item_content_wrapper {
        width: 200px;
        flex-grow: 1;
        flex-shrink: 1;
    }
    .item_desc {
        color: #828a92;
        font-size: 12px;
        line-height: 20px;
        margin-bottom: 12px;
    }
    .page_select{
        text-align: center;
    }
    .button{
        text-align: right;
    }

</style>