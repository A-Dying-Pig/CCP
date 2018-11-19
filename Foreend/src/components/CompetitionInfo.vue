<template>
    <div>
        <el-row type="flex" class="row-bg enroll-info-spliter" justify="center" >
            <el-col :span=24><div class="title">-----<slot></slot>-----</div></el-col>
        </el-row>
    <template v-if="typeid == 1">
        <el-form v-bind:model="info" :rules="basicrules" ref="info" label-width="1000px" label-position="top">
        <el-row>
            <el-col>
        <el-form-item label="比赛名称" prop="name" label-width="100">
            <el-input v-model="info.name"></el-input>
        </el-form-item>
            </el-col>
        </el-row>

        <el-row>
            <el-col>
        <el-form-item label="主办方" required label-width="100">
            <el-row v-for="(item,index) in info.holders" :key="item.key">
            <el-col>
            <el-form-item  prop="holders">
                <el-input v-model="info.holders[index]"></el-input>
            </el-form-item>
            </el-col>
            </el-row>
        </el-form-item>
            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <el-button type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.holders.push('')"></el-button>
                <el-button type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.holders.pop()"></el-button>
            </el-col>
        </el-row>
        <p></p>

        <el-row>
            <el-col>
        <el-form-item label="承办方" label-width="100">
            <el-row v-for="(item,index) in info.sponsors" :key="item.key">
            <el-col>
                <el-form-item   prop="sponsors">
                    <el-input v-model="info.sponsors[index]"></el-input>
                </el-form-item>
            </el-col>
            </el-row>
        </el-form-item>
            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <el-button type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.sponsors.push('')"></el-button>
                <el-button type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.sponsors.pop()"></el-button>
            </el-col>
        </el-row>
        <p></p>

        <el-row>
            <el-col>
        <el-form-item label="比赛类型" prop="comtype" label-width="100">
            <el-radio-group v-model="info.comtype">
                <el-radio v-for="item in comtypes" v-bind:label="item.label" v-bind:value="item.value" :key="item.key" label-width="80"></el-radio>
            </el-radio-group>
        </el-form-item>
            </el-col>
        </el-row>

        <el-row>
            <el-col>
                <el-form-item label="详细信息" prop="details" label-width="100">
                    <el-input type="textarea" :rows="10" placeholder="请输入详细信息" v-model="info.details">
                    </el-input>
                </el-form-item>
            </el-col>
        </el-row>
    </el-form>
</template>

    <template v-else-if="typeid == 2">
        <el-form v-bind:model="info" :rules="signuprules" ref="info" label-width="100px" label-position="top">
            <el-row>
                <el-col>
                <el-form-item label="报名起止时间" prop="time">
                    <el-date-picker v-model="info.time" type="datetimerange" start-placeholder="报名开始时间" end-placeholder="报名结束时间" :default-time="['00:00:00','23:59:59']"></el-date-picker>
                </el-form-item>
                </el-col>
            </el-row>

            <el-row>
                <el-col>
                    <el-form-item label="需要选手填的个人信息" label-width="100" required>
                        <el-row v-for="(item,index) in info.person" :key="item.key">
                            <el-col>
                                <el-form-item   prop="person">
                                    <el-input v-model="info.person[index]"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col>
                    <el-button type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.person.push('')"></el-button>
                    <el-button type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.person.pop()"></el-button>
                </el-col>
            </el-row>
            <p></p>

            <el-row>
                <el-col>
                    <el-form-item label="报名形式" prop="mode">
                        <el-radio-group v-model="info.mode">
                            <el-radio-button label="个人赛"></el-radio-button>
                            <el-radio-button label="组队赛"></el-radio-button>
                        </el-radio-group>
                    </el-form-item>
                </el-col>
            </el-row>

            <template v-if="info.mode === '组队赛'">
                <el-row>
                    <el-col>
                        <el-form-item label="需要的队伍信息" label-width="100" required>
                            <el-row v-for="(item,index) in info.group" :key="item.key">
                                <el-col>
                                    <el-form-item   prop="group">
                                        <el-input v-model="info.group[index]"></el-input>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col>
                        <el-button type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.group.push('')"></el-button>
                        <el-button type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.group.pop()"></el-button>
                    </el-col>
                </el-row>
            </template>
        </el-form>
    </template>
        <template v-else-if="typeid == 3">
        <el-row v-for="(item,index) in info" :key="item.key">
            <el-col>
                <CompetitonStage v-bind:tinfo="item" v-bind:index="index" ref="info"></CompetitonStage>
            </el-col>
        </el-row>
            <el-row>
                <el-col>
                    <el-button type="primary"  v-on:click="addStage()">添加阶段</el-button>
                    <el-button type="primary"  v-on:click="info.pop()">删除阶段</el-button>
                </el-col>
            </el-row>
        </template>
</div>
</template>

<script>
import Vue from 'vue'
import 'element-ui/lib/theme-chalk/index.css'
import ElementUI from 'element-ui'
Vue.use(ElementUI);

import CompetitonStage from './CompetitonStage'
export default {
    components:{
        CompetitonStage,
    },
    props:['finfo','typeid'],
    data:function () {
        var self=this;
        let testVali = function (rule,value,callback) {
            console.log(value);
            callback();
        };
        let holderVali = function (rule,value,callback) {
            for (let onename of value){
                if(onename.length==0){
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
        let signupVali = function (rule, value, callback) {
            for (let onename of value){
                if(onename.length==0){
                    callback(new Error('名称不能为空'));
                    return;
                }
                if(onename.length>10){
                    callback(new Error('名称不超过10个字符'));
                    return;
                }
            }
            callback();
        };
        return {
            info:this.finfo,
            basicrules:{
                name:[{required:true, message:'请输入比赛名称',trigger:'blur'},
                    {min:5, max:30,message:'长度在5到30个字符',trigger:'blur'}],
                holders:[{type:'array',validator:holderVali,trigger:'blur'},
                    {type:'array',max:3,message:'主办方个数不超过3个',trigger:'blur'}],
                sponsor:[{type:'array',validator:holderVali,trigger:'blur'},
                    {type:'array',max:5,message:'承办方个数不超过5个',trigger:'blur'}],
                comtype:[{required:true, message:'必须指定一种比赛类型',trigger:'change'}],
                details:[{required:true, message:'请输入比赛详细信息',trigger:'blur'},
                    {min:5,max:1000,message:'长度在5到1000个字符之间',trigger:'blur'}],
            },
            signuprules:{
                time:[{required:true,message:'请输入报名日期！',trigger:'blur'}],
                person:[{type:'array',validator:signupVali,trigger:'blur'},
                    {type:'array',max:10,message:'需要选手填写的个人信息条数不超过10个',trigger:'blur'}],
                mode:[{required:true,message:'请输入报名形式！',trigger:'change'}],
                group:[{type:'array',validator:signupVali,trigger:'blur'},
                    {type:'array',max:10,message:'需要的队伍信息条数不超过10个',trigger:'blur'}],
            },
            comtypes:[
                {label:'微信小程序',name:'type',value:'weixin'},
                {label:'web开发',name:'type',value:'web'}]
        }
    },
    methods:{
        deleteStage: function (idx) {
            this.info.splice(idx,1);
        },
        validate:function () {
            var flag=true;
            if(this.typeid<3){
                this.$refs.info.validate((valid) => {
                    if (valid) {
                        flag = true;
                    } else {
                        flag = false;
                    }
                });
                console.log(flag);
                return flag;
            }
            else if(this.typeid==3){
                for(let i of this.$refs.info){
                    if(!(i.validate())){
                        flag=false;
                    }
                }
                return flag;
            }
        },
        addStage:function () {
            this.info.push({
               name:'',
               details:''
            });
        }
    },
}
</script>

<style>
.title{
    text-align: center;
    font-family: "Adobe 黑体 Std R";
    font-size: large;
}
.label{
    text-align: left;
    font-family: "Adobe 黑体 Std R";
    font-size: 20px;
}
.enroll-info-spliter{
    font-size: 20px;
    font-family: "PingFang SC";
    margin-top: 30px;
    margin-bottom: 30px;
    text-align: center;
}
</style>