<template>
    <div>
        <el-row type="flex" class="row-bg enroll-info-spliter" justify="center" >
            <el-col :span=24><div class="title">-----<slot></slot>-----</div></el-col>
        </el-row>
    <template v-if="typeid == 1">
        <el-form v-bind:model="info" id="contest-info" :rules="basicrules" ref="info" label-width="1000px" label-position="top">
        <el-row>
            <el-col>
        <el-form-item label="比赛名称" prop="name" label-width="100" class="contest-name">
            <el-input v-model="info.name" :disabled="inputisable.basicinfo"></el-input>
        </el-form-item>
            </el-col>
        </el-row>

        <el-row>
            <el-col>
        <el-form-item label="主办方" required label-width="100">
            <el-row v-for="(item,index) in info.holders" :key="item.key">
            <el-col>
            <el-form-item  prop="holders" class="contest-holders">
                <el-input v-model="info.holders[index]" :disabled="inputisable.basicinfo"></el-input>
            </el-form-item>
            </el-col>
            </el-row>
        </el-form-item>
            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <el-button class="holders-plus"  :disabled="inputisable.basicinfo" type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.holders.push('')"></el-button>
                <el-button class="holders-minus" :disabled="inputisable.basicinfo" type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.holders.pop()"></el-button>
            </el-col>
        </el-row>
        <p></p>

        <el-row>
            <el-col>
        <el-form-item label="承办方" label-width="100">
            <el-row v-for="(item,index) in info.sponsors" :key="item.key">
            <el-col>
                <el-form-item   prop="sponsors" class="contest-sponsors">
                    <el-input :disabled="inputisable.basicinfo" v-model="info.sponsors[index]"></el-input>
                </el-form-item>
            </el-col>
            </el-row>
        </el-form-item>
            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <el-button class="sponsors-plus" :disabled="inputisable.basicinfo" type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.sponsors.push('')"></el-button>
                <el-button class="sponsors-minus" :disabled="inputisable.basicinfo" type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.sponsors.pop()"></el-button>
            </el-col>
        </el-row>
        <p></p>

        <el-row>
            <el-col>
        <el-form-item label="比赛类型" prop="comtype" label-width="100">
            <el-radio-group class="contest-type" v-model="info.comtype">
                <el-radio :disabled="inputisable.basicinfo" v-for="item in comtypes" v-bind:label="item.label" v-bind:value="item.value" :key="item.key" label-width="80"></el-radio>
            </el-radio-group>
        </el-form-item>
            </el-col>
        </el-row>

            <el-row>
                <el-col>
                    <el-form-item label="比赛图片" label-width="100">
                        <el-upload
                                class="avatar-uploader"
                                :action="'/api/competition/uploadimg'"
                                :show-file-list="false"
                                :on-success="handleAvatarSuccess"
                                :before-upload="beforeAvatarUpload"
                                :http-request="Uploadimg">
                            <img v-if="info.img" :src="info.img" class="avatar">
                            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                        </el-upload>
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row>
                <el-col>
                    <el-form-item label="比赛介绍（简略）" prop="briefintroduction" class="contest-brief-intro" label-width="100">
                        <el-input :disabled="inputisable.basicinfo" type="textarea" :rows="4" placeholder="请输入详细信息" v-model="info.briefintroduction">
                        </el-input>
                    </el-form-item>
                </el-col>
            </el-row>

        <el-row>
            <el-col>
                <el-form-item label="比赛介绍（详细）" prop="details" class="contest-detail-intro" label-width="100">
                    <el-input :disabled="inputisable.basicinfo" type="textarea" :rows="10" placeholder="请输入详细信息" v-model="info.details">
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
                <el-form-item label="报名起止时间" prop="time" class="contest-enroll-time">
                    <el-date-picker :disabled="inputisable.signupinfo" v-model="info.time" type="datetimerange" start-placeholder="报名开始时间" end-placeholder="报名结束时间" :default-time="['00:00:00','01:00:00']"></el-date-picker>
                </el-form-item>
                </el-col>
            </el-row>
            <p></p>

            <el-row>
                <el-col>
                    <el-form-item label="报名形式" prop="mode" class="enroll-type">
                        <el-radio-group v-model="info.mode">
                            <el-radio-button :disabled="inputisable.signupinfo" label="1">个人赛</el-radio-button>
                            <el-radio-button :disabled="inputisable.signupinfo" label="0">组队赛</el-radio-button>
                        </el-radio-group>
                    </el-form-item>
                </el-col>
            </el-row>

            <template v-if="info.mode === '1'">
                <el-row>
                    <el-col>
                        <el-form-item label="需要填写的个人信息" label-width="100" required class="contest-person-info">
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
                        <el-button class="person-info-plus" type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.person.push('')"></el-button>
                        <el-button class="person-info-minus" type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.person.pop()"></el-button>
                    </el-col>
                </el-row>
            </template>

            <template v-if="info.mode === '0'">
                <el-row>
                    <el-col>
                        <el-form-item label="队伍人数选择" label-width="100" prop="teamnum" required class="contest-group-number">
                                                <el-slider
                                                        v-model="info.teamnum"
                                                        show-stops
                                                        :min="1"
                                                        :max="10">
                                                </el-slider>
                                    </el-form-item>
                    </el-col>
                </el-row>
            </template>

            <template v-if="info.mode === '0'">
                <el-row>
                    <el-col>
                        <el-form-item label="需要填写的队伍信息" label-width="100" required class="contest-group-info">
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
                        <el-button class="group-info-plus" type="primary" size="mini" icon="el-icon-plus" circle v-on:click="info.group.push('')"></el-button>
                        <el-button class="group-info-minus" type="danger" size="mini" icon="el-icon-minus" circle v-on:click="info.group.pop()"></el-button>
                    </el-col>
                </el-row>
            </template>
        </el-form>
    </template>
        <template v-else-if="typeid == 3">
        <el-row v-for="(item,index) in info" :key="item.key">
            <el-col>
                <CompetitonStage v-bind:tinfo="item" v-bind:index="index" ref="info" :change="change" :stagebegintime="stagebegintime[index]"></CompetitonStage>
            </el-col>
        </el-row>
            <el-row>
                <el-col>
                    <el-button class="stage-plus" type="primary"  v-on:click="addStage()">添加阶段</el-button>
                    <el-button class="stage-minus" type="primary"  v-on:click="deleteStage()" :disabled="deletestagenotok">删除阶段</el-button>
                </el-col>
            </el-row>
        </template>
</div>
</template>

<script>
//import axios from 'axios'

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.headers.common = {
  'X-CSRFToken':document.querySelector('#csrf-token input').value,
    'X-Requested-With': 'XMLHttpRequest'
};
import CompetitonStage from './CompetitonStage.vue'
export default {
    components:{
        CompetitonStage,
    },
    props:['finfo','typeid','change','signend'],
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
        let timeVali = function (rule, value, callback) {
            let v0 = new Date(value[0]);
            let v1 = new Date(value[1]);

            if(v0.getMinutes()||v0.getSeconds()||v1.getMinutes()||v1.getSeconds()){
                callback(new Error("必须为整小时数！"));
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
                briefintroduction:[{required:true, message:'请输入比赛信息',trigger:'blur'},
                    {min:5,max:100,message:'长度在5到100个字符之间',trigger:'blur'}]
            },
            signuprules:{
                time:[{required:true,message:'请输入报名日期！',trigger:'change'}],
                person:[{type:'array',validator:signupVali,trigger:'blur'},
                    {type:'array',max:10,message:'需要选手填写的个人信息条数不超过10个',trigger:'blur'}],
                mode:[{required:true,message:'请输入报名形式！',trigger:'change'}],
                group:[{type:'array',validator:signupVali,trigger:'blur'},
                    {type:'array',max:10,message:'需要的队伍信息条数不超过10个',trigger:'blur'}],
                teamnum:[{required:true,message:'请选择队伍人数！',trigger:'change'}]
            },
            comtypes:[
                {label:'微信小程序',name:'type',value:'weixin'},
                {label:'web开发',name:'type',value:'web'}],
            inputisable:{
                basicinfo:false,
                signupinfo:false,
            },
            stagebegintime:[],
            deletestagenotok:false,
        }
    },
    methods:{
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
               details:'',
                mode:'在线预览',
                zone:'统一赛区'
            });
            this.deletestagenotok = !this.checkDeleteState();
        },
        deleteStage:function(){
            this.info.pop();
            this.deletestagenotok = !this.checkDeleteState();

        },
        checkDeleteState:function () {
            let now =Date.now();
            //let now = 1542893167173;
            if(this.change&&(this.typeid==3)){
                let stagelen = this.info.length;
                if(stagelen==0) return false;
                else if(stagelen==1){
                    if(now>this.signend){
                        return false;
                    }
                }
                else{
                    if(now>this.info[stagelen-2].evaluationTimeEnd){
                        return false;
                    }
                }
            }
            return true;
        },
        handleAvatarSuccess(res, file) {
            this.imageUrl = URL.createObjectURL(file.raw);
        },
        beforeAvatarUpload(file) {
            const isTYPE = /\.(jpg|jpeg|png|JPG|PNG)$/.test(file.name);
            const isLt2M = file.size / 1024 / 1024 < 2;

            if (!isTYPE) {
                this.$message.error('上传头像图片只能是 JPG 格式!');
            }
            if (!isLt2M) {
                this.$message.error('上传头像图片大小不能超过 2MB!');
            }
            return isTYPE && isLt2M;
        },
        Uploadimg:function(param){
            let fileobj = param.file;
            let self = this;
            let fd = new FormData();
            fd.append('file',fileobj);
            axios.post('/api/competition/uploadimg',fd,{
            }).then(function (response) {
                let msg = response.data.msg;
                if(msg!==''){
                    self.$message({
                        message:'上传'+fileobj.name+'失败！',
                        type:'error'
                    });
                }
                else {
                    self.$message({
                        message:'上传'+fileobj.name+'成功！',
                        type:'success'
                    });
                    self.info.img = response.data.url;
                }
            }).catch(function (error) {
                self.$message({
                    message:'上传'+fileobj.name+'失败！',
                    type:'error'
                });
            });
        }
    },
    created:function () {
        console.log(this.change);
        if(this.change){
            //查看比赛详情页面，设置哪些框显示
            this.inputisable.basicinfo=true;
            this.inputisable.signupinfo=true;
            //载入各个阶段开始时间
            if(this.typeid==3){
                this.stagebegintime.push(this.signend);
                for(let stage of this.info){
                    this.stagebegintime.push(stage.evaluationTimeEnd);
                }
                this.stagebegintime.pop();
            }
            this.deletestagenotok = !this.checkDeleteState();
        }
    }
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
.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.avatar-uploader .el-upload:hover {
    border-color: #409EFF;
}
.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
}
.avatar {
    width: 178px;
    height: 178px;
    display: block;
}
</style>