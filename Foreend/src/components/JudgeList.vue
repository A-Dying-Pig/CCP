<template>
    <div class="judges">
        <el-card class="allocjudge" v-if="judgebeginbutton">
            <el-row>
                每份作品被评测次数<el-input-number v-model="judgenum" :min="1" :max="10" label="每份作品被评测次数"></el-input-number>
            </el-row>
            <el-row>
                <el-button @click="assignproject" type="primary">分配作品</el-button>
            </el-row>
        </el-card>

        <el-card class="add-judge">
            <el-form :inline="true" :model="new_judge">
                <el-form-item label="添加评委">
                    <el-input v-model="new_judge.username" placeholder="输入评委的用户名" ></el-input>
                </el-form-item>

                <el-form-item label="设置赛区">
                    <el-select v-model="new_judge.id" placeholder="请选择赛区">
                        <el-option
                                v-for="item in zone_menu"
                                :key="item.id"
                                :label="item.value"
                                :value="item.id"
                        >
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="OnSubmit" >添加</el-button>
                </el-form-item>
            </el-form>
        </el-card>

        <div class="judge-list">
            <el-card  class="judges-selector">
                <div class="judges-selector-btn">
                    快速查找 <el-button icon="el-icon-search" type="text" @click="JudgesSearch"></el-button>
                </div>

                <div class="judges-selector-item">
                    <el-input placeholder="输入评委名称" v-model="search_username" @blur="JudgesSearch">
                        <span slot="prepend">评委名称</span>
                    </el-input>
                </div>
                <div class="judges-selector-item">
                    <el-input placeholder="输入赛区名称" v-model="search_zone" @blur="JudgesSearch">
                        <span slot="prepend">赛区名称</span>
                    </el-input>
                </div>
            </el-card>

            当前{{current_judges_number}}人/总{{judges_number}}人
            <el-card class="list">
            <el-table
                    :data="current_page_judges"
                    style="width: 100%">

                <el-table-column
                        prop="username"
                        label="评委名称"
                        min-width="3"
                >
                </el-table-column>
                <el-table-column
                        prop="value"
                        label="赛区"
                        min-width="2"
                >
                </el-table-column>


                <el-table-column
                        label="设置新赛区"
                        min-width="6">
                    <template slot-scope="scope">

                        <el-select v-model="current_page_judges[scope.$index].id"
                                   placeholder="请选择新赛区">
                            <el-option
                                    v-for="item in zone_menu"
                                    :key="item.id"
                                    :label="item.value"
                                    :value="item.id"
                            >
                            </el-option>
                        </el-select>
                        <el-button style="padding: 10px 4px" type="success" @click="ChangeZoneSubmit(scope.$index)" plain>确认</el-button>

                    </template>
                </el-table-column>

                <el-table-column
                        label="操作"
                        min-width="1">
                    <template slot-scope="scope">
                        <el-button style="padding: 10px 4px" type="danger" @click="DeleteJudge(scope.$index)" plain>删除</el-button>
                    </template>
                </el-table-column>

            </el-table>


            <el-pagination
                    layout="prev, pager, next"
                    :current-page="current_page"
                    :page-count="total_page"
                    @current-change="CurrentPageChange"
                    @prev-click="PagePrevious"
                    @next-click="PageNext"
                    class="judge-list-page">
            </el-pagination>

            </el-card>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        //'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        name: "JudgeList",
        props:{
            contestid:{
                default:-1
            },
            judgebeginbutton:{
                Type:Boolean,
                default:false
            }
        },
        data:function () {
            return {
                new_judge:{
                    username:'',
                    id:null,          //zone id
                },
                zone_menu: [],
                judges_per_page:8,
                judges:[],
                judges_number:0,
                current_judges:[],
                current_judges_number:0,
                current_page_judges:[],
                current_page_judges_number:0,
                current_page:0,
                total_page:0,
                search_username:'',
                search_zone: '',
                judgenum:1,
            }
        },
        methods:{
            OnSubmit:function () {
                let self = this;
                if(self.new_judge.username === ''){
                    self.$message({
                        message:'名称不可以为空!',
                        type:'error'
                    });
                }
                else if (self.new_judge.id === null){
                    self.$message({
                        message:'评委赛区不可以为空!',
                        type:'error'
                    });
                }
                else {
                    axios.post('/api/admin/setjudge',{
                            username:self.new_judge.username,
                            id:self.new_judge.id,
                            contestid:self.contestid,
                            type:0
                        })
                            .then(function (response) {
                                if(response.data.msg === ''){
                                    self.$message({
                                        message:'创建成功!',
                                        type:'success'
                                    });

                                    let the_zone = self.zone_menu.filter(function (element) {
                                        return element.id === self.new_judge.id;
                                    });
                                    let temp = {
                                        username:self.new_judge.username,
                                        id:self.new_judge.id,
                                        value:the_zone[0].value,
                                    };
                                    self.judges.push(temp);
                                    self.judges_number = self.judges.length;
                                    self.new_judge.username = '';
                                    self.new_judge.id = null;
                                    //default
                                    self.JudgesSearch();
                                }
                                else{
                                    self.$message({
                                        message:`设置评委失败! ${response.data.msg}`,
                                        type:'error'
                                    });
                                    //self.UpdateJudgeList();
                                }
                            });
                }
            },
            ChangeZoneSubmit:function(index){
                let vm  = this;
                let the_zone = vm.zone_menu.filter(function (element) {
                    return element.id === vm.current_page_judges[index].id;
                });
                if (this.current_page_judges[index].value === the_zone[0].value){
                    vm.$message({
                        message:'请选择不同的赛区!',
                        type:'error'
                    });
                    return;
                }

                axios.post('/api/admin/setjudge',{
                    contestid:this.contestid,
                    type: 1,
                    username: this.current_page_judges[index].username,
                    id:this.current_page_judges[index].id
                })
                    .then(response=>{
                       if (response.data.msg === ''){
                           vm.$message({
                               message:'修改评委赛区成功!',
                               type:'success'
                           });

                           let the_zone = vm.zone_menu.filter(function (element) {
                               return element.id === vm.current_page_judges[index].id;
                           });
                           vm.current_page_judges[index].value = the_zone[0].value;
                           vm.CurrentPageChange(vm.current_page);
                       }
                       else{
                           vm.$message({
                               message: `修改评委赛区失败! ${response.data.msg}`,
                               type: 'error'
                           });
                       }
                    });
            },
            CurrentPageChange:function (cur_page) {
                this.current_page = cur_page;
                this.current_page_judges.splice(0);
                let offset = (this.current_page - 1 ) * this.judges_per_page;
                this.current_page_judges_number = this.judges_per_page;
                if (this.current_page === this.total_page)
                    this.current_page_judges_number = this.current_judges_number - (this.current_page - 1) * this.judges_per_page;
                for (let i = 0; i < this.current_page_judges_number; i ++ ){
                    this.current_page_judges.push(this.current_judges[offset + i]);
                }
            },
            PagePrevious:function (cur_page) {
                this.CurrentPageChange(cur_page);
            },
            PageNext:function (cur_page) {
                this.CurrentPageChange(cur_page);
            },
            UpdateJudgeList:function () {
                this.current_page_judges_number = 0;
                this.judges.splice(0);
                this.current_page_judges.splice(0);
                this.current_judges.splice(0);
                this.judges_number = 0;
                this.current_judges_number = 0;
                this.current_page = 0;
                this.total_page = 0;

                let vm = this;
                axios.post('/api/admin/judgelist',{contestid:this.contestid})
                    .then(response=>{
                        if (response.data.msg !== ''){
                            vm.$message({
                                message: `获取评委列表失败! ${response.data.msg}`,
                                type: 'error'
                            });
                        }
                        else{
                            vm.judges = response.data.judges;
                            vm.judges_number = vm.judges.length;
                            for (let i = 0; i < vm.judges_number; i++){
                                 let the_zone = vm.zone_menu.filter(function (element) {
                                     return element.id === vm.judges[i].id;
                                 });
                                 vm.judges[i].value = the_zone[0].value;
                            }

                            //default
                            vm.DefaultDisplay();
                            vm.CurrentPageChange(1);
                        }
                    })
                    .catch(error=>{
                        console.log(error);
                        vm.judges = [
                            {username:'1',id:1},
                            {username:'2',id:1},
                            {username:'3',id:1},
                            {username:'4',id:1},
                            {username:'5',id:1},
                            {username:'6',id:1},
                            {username:'7',id:1},
                            {username:'8',id:1},
                            {username:'9',id:1},
                            {username:'10',id:1},
                            {username:'11',id:1},
                            {username:'12',id:1},
                            ];
                        vm.judges_number = vm.judges.length;
                        for (let i = 0; i < vm.judges_number; i++){
                            let the_zone = vm.zone_menu.filter(function (element) {
                                return element.id === vm.judges[i].id;
                            });
                            vm.judges[i].value = the_zone[0].value;
                        }
                        //default
                        vm.DefaultDisplay();
                        vm.CurrentPageChange(1);
                    });
            },
            DefaultDisplay:function(){
                this.current_judges = [].concat(this.judges);
                this.current_judges_number = this.current_judges.length;
                this.total_page = Math.ceil(this.current_judges_number / this.judges_per_page);
                if (this.current_judges_number === 0 )
                    this.total_page = 1;
            },
            DeleteJudge:function (index) {
                let vm = this;

                axios.post('/api/admin/setjudge',{
                    username:vm.current_page_judges[index].username,
                    id:vm.current_page_judges[index].id,
                    contestid:vm.contestid,
                    type:2
                })
                    .then(function (response) {
                        if(response.data.msg === ''){
                            vm.$message({
                                message:'删除成功!',
                                type:'success'
                            });

                            vm.judges.filter(function (element,i,self) {
                                if(element.username === vm.current_page_judges[index].username)
                                    self.splice(i,1);
                                return false;
                            });
                            vm.judges_number = vm.judges.length;
                            vm.JudgesSearch();
                        }
                        else{
                            vm.$message({
                                message:`删除评委失败! ${response.data.msg}`,
                                type:'error'
                            });
                            //vm.UpdateJudgeList();
                        }
                    });
            },
            JudgesSearch:function () {
                this.current_judges.splice(0);
                this.current_judges_number = 0;
                this.total_page = 0;
                this.current_page = 0;

                //default
                this.current_judges = [].concat(this.judges);
                if (this.search_username !== ''){
                    //select name
                    let vm = this;
                    this.current_judges = this.current_judges.filter(function (element) {
                        return element.username === vm.search_username;
                    });
                }
                if(this.search_zone !== ''){
                    //select zone
                    let vm = this;
                    this.current_judges = this.current_judges.filter(function (element) {
                        return element.value === vm.search_zone;
                    });
                }

                this.current_judges_number = this.current_judges.length;
                this.total_page = Math.ceil(this.current_judges_number / this.judges_per_page);
                if(this.total_page === 0)
                    this.total_page = 1;
                this.CurrentPageChange(1);
            },
            assignproject:function () {
                let self = this;
                axios.post('/api/admin/allot',{
                    contestid:self.contestid,
                    judgenum:self.judgenum
                }).then(function (response) {
                    if(response.data.msg!==''){
                        self.$message({
                            message:response.data.msg,
                            type:'error'
                        })
                    }
                    else {
                        self.$message({
                            message:'评委分配成功！',
                            type:'success'
                        })
                    }
                }).catch(function (error) {
                    self.$message({
                        message:'评委分配失败！',
                        type:'error'
                    })
                })
            }
        },
        mounted:function () {
            let vm = this;
            axios.post('/api/admin/zone',{contestid:this.contestid})
                .then(response=>{
                    if(response.data.msg === ''){
                        let len = response.data.list.length;
                        if (len === 0){
                            vm.zone_menu.splice(0,1,{id:-1,value:'比赛统一赛区'});
                        }
                        else{
                            for (let i = 0 ; i < len; i++){
                                vm.zone_menu.push(response.data.list[i]);
                            }
                        }
                    }
                    else{
                        vm.$message({
                            message: `获取赛区信息失败! ${response.data.msg}`,
                            type: 'error'
                        });
                    }
                })
                .catch(error=>{
                    console.log(error);
                    vm.zone_menu = [
                            {id:0,value:'北京'},
                            {id:1,value:'上海'},
                            {id:2,value:'重庆'},
                        ];
                });
            this.UpdateJudgeList();
        }
    }
</script>

<style>
.judge-list-page{
    margin-top: 30px;
    margin-bottom: 20px;
    text-align: center;
}
.judges-selector-item{
    margin-top: 10px;
    margin-bottom: 10px;
}
.add-judge{
    margin-bottom: 20px;
}
.judges-selector{
    margin-bottom: 20px;
}
</style>