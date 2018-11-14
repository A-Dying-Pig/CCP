<template>
    <div>
        <el-row type="flex" class="row-bg" justify="center"><el-col :span="6"><div class="title">——<slot></slot>——</div></el-col></el-row>
    <template v-if="typeid == 1"><el-form v-bind:model="info" :rules="basicrules" ref="info" label-width="100px" label-position="top">
        <el-row gutter=20>
            <el-col span="10" offset="5">
        <el-form-item label="比赛名称" prop="name" label-width="100">
            <el-input v-model="info.name"></el-input>
        </el-form-item>
            </el-col>
        </el-row>

        <el-row gutter=20>
            <el-col span=20 offset="5">
        <el-form-item label="主办方" required label-width="100">
            <el-row v-for="(item,index) in info.holders" :key="item.key">
            <el-col span="10">
            <el-form-item  prop="holders">
                <el-input v-model="info.holders[index]"></el-input>
            </el-form-item>
            </el-col>
            </el-row>
        </el-form-item>
            </el-col>
        </el-row>
        <el-row gutter="20">
            <el-col offset="5">
                <el-button type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.holders.push('')"></el-button>
                <el-button type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.holders.pop()"></el-button>
            </el-col>
        </el-row>


        <el-row gutter="20">
            <el-col span="20" offset="5">
        <el-form-item label="承办方" label-width="100">
            <el-row v-for="(item,index) in info.sponsors" :key="item.key">
            <el-col span="10">
                <el-form-item   prop="sponsors">
                    <el-input v-model="info.sponsors[index]"></el-input>
                </el-form-item>
            </el-col>
            </el-row>
        </el-form-item>
            </el-col>
        </el-row>
        <el-row gutter="20">
            <el-col offset="5">
                <el-button type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.sponsors.push('')"></el-button>
                <el-button type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.sponsors.pop()"></el-button>
            </el-col>
        </el-row>

        <el-row gutter="20">
            <el-col offset="5">
        <el-form-item label="比赛类型" prop="comtype">
            <el-radio-group v-model="info.comtype">
                <el-radio v-for="item in comtypes" v-bind:label="item.label" v-bind:value="item.value" :key="item.key"></el-radio>
            </el-radio-group>
        </el-form-item>
            </el-col>
        </el-row>

        <el-row gutter="20">
            <el-col offset="5" span="10">
        <MdEdit v-model="info.details">详细信息</MdEdit>
            </el-col>
        </el-row>
    </el-form> </template>

    <div v-else-if="typeid == 2">
        <el-form v-bind:model="info" :rules="signuprules" ref="info" label-width="100px" label-position="top">
            <el-row gutter="20">
                <el-col offset="5">
                <el-form-item label="报名起止时间" prop="time">
                    <el-date-picker v-model="info.time" type="datetimerange" start-placeholder="报名开始时间" end-placeholder="报名结束时间" :default-time="['00:00:00','23:59:59']"></el-date-picker>
                </el-form-item>
                </el-col>
            </el-row>

            <el-row gutter="20">
                <el-col span="20" offset="5">
                    <el-form-item label="需要选手填的个人信息" label-width="100" required>
                        <el-row v-for="(item,index) in info.person" :key="item.key">
                            <el-col span="10">
                                <el-form-item   prop="person">
                                    <el-input v-model="info.person[index]"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row gutter="20">
                <el-col offset="5">
                    <el-button type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.person.push('')"></el-button>
                    <el-button type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.person.pop()"></el-button>
                </el-col>
            </el-row>

            <el-row gutter="20">
                <el-col offset="5">
                    <el-form-item label="报名形式" prop="mode">
                        <el-radio-group v-model="info.mode">
                            <el-radio-button label="个人赛"></el-radio-button>
                            <el-radio-button label="组队赛"></el-radio-button>
                        </el-radio-group>
                    </el-form-item>
                </el-col>
            </el-row>

            <template v-if="info.mode === '组队赛'">
                <el-row gutter="20">
                    <el-col span="20" offset="5">
                        <el-form-item label="需要的队伍信息" label-width="100" required>
                            <el-row v-for="(item,index) in info.group" :key="item.key">
                                <el-col span="10">
                                    <el-form-item   prop="group">
                                        <el-input v-model="info.group[index]"></el-input>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row gutter="20">
                    <el-col offset="5">
                        <el-button type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.group.push('')"></el-button>
                        <el-button type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.group.pop()"></el-button>
                    </el-col>
                </el-row>
            </template>
        </el-form>
    </div>
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
        let testVali = function (rule,value,callback) {
            console.log(value);
            callback();
        };
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
        let signupVali = function (rule, value, callback) {
            for (let onename of value){
                console.log(onename)
                if(onename.length==0){
                    console.log('no')
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
        font-size: 40px;
    }
</style>