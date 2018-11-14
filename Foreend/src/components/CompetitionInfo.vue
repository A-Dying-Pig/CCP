<template>
<div><slot></slot>
    <div v-if="typeid == 1"><el-form v-bind:model="info" :rules="rules" ref="info" label-width="100px">
        <el-form-item label="比赛名称" prop="name">
            <el-input v-model="info.name"></el-input>
        </el-form-item>
        <el-form-item label="主办方" required>
            <el-form-item v-for="(item,index) in info.holders" :key="item.key" prop="holders">
                <el-input v-model="info.holders[index]"></el-input>
            </el-form-item>
            <el-button type="primary" icon="el-icon-plus" circle v-on:click="info.holders.push('')"></el-button>
            <el-button type="danger" icon="el-icon-minus" circle v-on:click="info.holders.pop()"></el-button>
        </el-form-item>
        <el-form-item label="承办方" prop="sponsor">
            <el-input v-for="(item,index) in info.sponsors" v-model="info.sponsors[index]" :key="item.key"></el-input>
            <el-button type="primary" icon="el-icon-plus" circle v-on:click="info.sponsors.push('')"></el-button>
            <el-button type="danger" icon="el-icon-minus" circle v-on:click="info.sponsors.pop()"></el-button>
        </el-form-item>
        <el-form-item label="比赛类型" prop="comtype">
            <el-radio-group v-model="info.comtype">
                <el-radio v-for="item in comtypes" v-bind:label="item.label" v-bind:value="item.value" :key="item.key"></el-radio>
            </el-radio-group>
        </el-form-item>
        <MdEdit v-model="info.details">详细信息</MdEdit>
    </el-form> </div>

    <div v-else-if="typeid == 2">signup</div>
</div>
</template>

<script>
import MdEdit from './MdEdit'
export default {
    components:{
      MdEdit,
    },
    props:['finfo','typeid'],
    data:function () {
        var self=this;
        let holderVali = function (rule,value,callback) {
            for (let onename of value){
                console.log(onename)
                if(onename.length==0){
                    console.log('no')
                    callback(new Error('名称不能为空'));
                    return;
                }
                if(onename.length>30){
                    callback(new Error('名称不超过30个字符'));
                    return;
                }
            }
          callback();
        };
        return {
            info:this.finfo,
            rules:{
                name:[{required:true, message:'请输入比赛名称',trigger:'blur'},
                    {min:5, max:30,message:'长度在5到30个字符',trigger:'blur'}],
                holders:[{type:'array',validator:holderVali,trigger:'blur'},
                    {type:'array',max:3,message:'主办方个数不超过3个',trigger:'blur'}],
                sponsor:[{type:'array',validator:holderVali,trigger:'blur'},
                    {type:'array',max:5,message:'承办方个数不超过5个',trigger:'blur'}],
                comtype:[{required:true, message:'必须指定一种比赛类型',trigger:'change'}],
            },
            comtypes:[
                {label:'微信小程序',name:'type',value:'weixin'},
                {label:'web开发',name:'type',value:'web'}]
        }
    },
    methods:{
    },
}
</script>

<style>

</style>