<template>
    <div>
        <el-row :gutter="24" v-if="nodes.length>0">
            <el-col :span="6">
                <slVueTree v-model="nodes" :allow-multiselect="false" @select="nodeSelected" id="slvuetree">
                    <template slot="title" slot-scope="{ node }">
                            <span>
                                <i class="icon-fileicon" v-if="node.isLeaf"></i>
                                <i class="icon-diricon" v-if="!node.isLeaf"></i>
                            </span>
                        {{ node.title }}
                    </template>
                </slVueTree>
            </el-col>
            <el-col :span="18">
                <el-row :gutter="24">
                    <el-col :span="24">
                        <el-row :gutter="24">
                            <el-col :span="10">
                                <template v-if="selectnode.type > 0">
                                    文件名称：{{ selectnode.title }}
                                    <a :href="selectnode.src" :download="selectnode.title"><el-button type="primary" @click="downloadfile">点击下载</el-button></a>
                                </template>
                            </el-col>
                        </el-row>
                        <el-row :gutter="24">
                            <el-col :span="24">
                                <template v-if="selectnode.type == 1">
                                    <img :src="selectnode.src"/>
                                </template>
                                <template v-else-if="selectnode.type == 2">
                                    <PDF :pdfurl="selectnode.src"></PDF>
                                </template>
                                <template v-else-if="selectnode.type == 3">
                                    抱歉，该文件不支持在线预览！
                                </template>
                            </el-col>
                        </el-row>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="24">
                        <el-form v-bind:model="gradeinfo" ref="gradeinfo" :rules="rules" label-width="100px">
                            <el-form-item label="分数" prop="grade">
                                <el-input v-model.number="gradeinfo.grade" placeholder="请输入分数" :disabled="readonly"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-button v-on:click="submitgrade()" :disabled="readonly">提交</el-button>
                            </el-form-item>
                        </el-form>
                    </el-col>
                </el-row>
            </el-col>
        </el-row>
        <el-row :gutter="24" v-else>
            <el-col>
                已无待评测作品
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import axios from 'axios'
    import slVueTree from 'sl-vue-tree'
    import PDF from './PDF.vue'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        components:{
            slVueTree,
            PDF
        },
        name: "GradeProject",
        props:['contestid','stageinfo','readonly','participantid','participantgrade'],
        data:function () {
            let defaultgrade = this.participantgrade?this.participantgrade:0;
            let validateGrade = function (rule, value, callback){
                if ((value<0)||(value>100)) {
                    return callback(new Error('分数在0-100之间！'))
                }
                return callback();
            };
            return{
                nodes:[],
                selectnode:{
                    title:'',
                    src:'',
                    type:0//img 1, pdf 2, other 3
                },
                gradeinfo:{
                    grade:defaultgrade,
                },
                rules:{
                    grade:[{required:true,message:'请给选手打分',trigger:'blur'},{
                        type:'number',message:'分数必须为数字',trigger:'blur'
                    },{
                        validator: validateGrade,message:'分数必须在0-100之间',trigger:'blur'
                    }],
                },
            }
        },
        methods:{
            getfiles:function(){
                console.log('getting file');
                //this.files=[];
                let self=this;
                self.nodes = [];
                axios.post('/api/judge/getone',{
                    contestid:self.contestid,
                    participantid:(this.readonly?this.participantid:-1),
                }).then(function (response) {
                    if(response.data.msg===''){
                        self.nodes = response.data.files;
                        self.participantid = response.data.participantid;
                        console.log(self.participantid)
                    }
                    else{
                            self.nodes = [];
                        }

                    }).catch(function (error) {
                        console.log(error);
                    });
                console.log(self.nodes)
            },
            downloadfile:function(){

            },
            submitgrade:function () {
                let self = this;
                let res = this.$refs.gradeinfo.validate((valid) => {
                    if (valid) {
                        //submit
                        //get phase
                        let phase = 0;
                        let now = Date.now();
                        for(let stage of self.stageinfo){
                            if(now<stage.evaluationTimeEnd){
                                break;
                            }
                            phase++;
                        }
                        console.log(phase);
                        axios.post('/api/judge/submit',{
                            contestid:self.contestid,
                            userId:self.participantid,
                            grade:self.gradeinfo.grade,
                            phase:phase+1
                        }).then(function (response) {
                            if(response.data.msg===''){
                                self.$message.success('提交成功！');
                                self.nodes = [];
                                self.getfiles();
                            }
                            else {
                                self.$message.error('提交失败！服务器返回错误！');
                            }
                        }).catch(function (error) {
                            self.$message.error('提交失败！');
                        })
                        //getnext
                        return true;
                    } else {
                        return false;
                    }
                });
            },
            checkimg : function(name) {
                if((name.endsWith('jpg'))||(name.endsWith('png'))){
                    return true;
                }
                return false;
            } ,
            nodeSelected :function (nodes) {
                let node = nodes[0];
                console.log(node);
                if(node.isLeaf === false){
                    console.log('select a directory');
                    return;
                }
                this.selectnode.title = node.title;
                this.selectnode.src = node.data.src;
                console.log('select:'+this.selectnode.src);
                if(this.checkimg(this.selectnode.title)){
                    this.selectnode.type = 1;
                }
                else if(this.selectnode.title.endsWith('pdf')){
                    this.selectnode.type = 2;
                }
                else {
                    this.selectnode.type = 3;
                }
            }
        },
        created:function () {
            this.getfiles();
            }
    }
</script>

<style scoped >
#slvuetree{
    background-color: rgb(245,247,250);
    border: white;
    color: black;
}
.sl-vue-tree-node-item:hover,
.sl-vue-tree-node-item.sl-vue-tree-cursor-hover {
    color: black;
}
</style>
<style src="../../node_modules/sl-vue-tree/dist/sl-vue-tree-dark.css"></style>
<style src="../assets/fonts/fileico/style.css"></style>