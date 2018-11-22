<template>
    <div>
        <div v-for="item in files" :key="item.key">
            <el-row type="flex" justify="center">
                {{ item.name }}
            </el-row>
            <el-row type="flex" justify="center">
                <img v-if="item.type === 'img'" :src="item.url"/>
            </el-row>
        </div>
        <el-form v-bind:model="gradeinfo" ref="gradeinfo" :rules="rules" label-width="100px">
            <el-form-item label="分数" prop="grade">
                <el-input v-model.number="gradeinfo.grade" placeholder="请输入分数"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button v-on:click="submitgrade()">提交</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        components:{},
        name: "GradeProject",
        props:['contestid','stageinfo'],
        data:function () {
            return{
                files:[/*{
                    name:'1.pdf',
                    type:'pdf',
                    url:'http://math.sjtu.edu.cn/faculty/chengwang/files/2015fall/ch1.pdf',
                },*/{
                    name:'1.jpg',
                    type:'img',
                    url:'https://goss.vcg.com/creative/vcg/800/version23/VCG41565794281.jpg'
                }],
                gradeinfo:{
                    grade:0,
                },
                rules:{
                    grade:[{required:true,message:'请给选手打分',trigger:'blur'},{
                        type:'number',message:'分数必须为数字',trigger:'blur'
                    },{
                        min:0,max:100,message:'分数必须在0-100之间',trigger:'blur'
                    }],
                },
                userid:'',
            }
        },
        methods:{
            getfiles:function(){
                console.log('getting file');
                //this.files=[];
                var self=this;
                axios.get('/api/competiton/getonepro')
                    .then(function (response) {
                        this.files=[];
                        let urllist = response.data.files;
                        for(let url of urllist){
                            let filename = url.split('/').pop();
                            let filetype = filename.split('.').pop();
                            if(self.checkimg(filetype)){
                                filetype = 'img';
                            }
                            self.files.push({
                                name:filename,
                                type:filetype,
                                url:url,
                            })
                        }
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
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
                        axios.post('/api/judge/submit',{
                            contestid:self.contestid,
                            userId:self.userid,
                            grade:self.gradeinfo.grade,
                            phase:phase
                        }).then(function (response) {
                            if(response.data.msg===''){
                                self.$message.success('提交成功！');
                            }
                            else {
                                self.$message.error('提交失败！服务器返回错误！');
                            }
                        }).catch(function (error) {
                            self.$message.error('提交失败！');
                        })
                        //getnext
                        this.getfiles();
                        return true;
                    } else {
                        return false;
                    }
                });
            },
            checkimg : function(typename) {
                if((typename==='jpg')||(typename==='png')){
                    return true;
                }
                return false;
            } ,
        },
        created:function () {

            this.getfiles();
            }
    }
</script>

<style scoped>

</style>