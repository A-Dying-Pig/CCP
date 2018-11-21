<template>
    <div>
        <el-row type="flex" justify="center">
            <el-col>
                <el-table :data="tableinfo" border style="width: 100%;">
                    <el-table-column prop="name" label="名称" fixed></el-table-column>
                    <el-table-column v-if="mode == 1" prop="email" label="邮箱"></el-table-column>
                    <el-table-column v-for="(item,index) in tableinfo[0].stage" :formatter="stageForm" :label="'阶段'+index+'分数'" :key="item.key"></el-table-column>
                    <template v-if="mode == 0">
                        <template v-for="(item,index) in tableinfo[0].person">
                            <el-table-column :formatter="nameForm" :label="'成员'+index+'姓名'" :key="item.key"></el-table-column>
                            <el-table-column :formatter="emailForm" :label="'成员'+index+'邮箱'" :key="item.key"></el-table-column>
                        </template>
                    </template>
                </el-table>
            </el-col>
        </el-row>
        <el-row type="flex" justify="center">
            <el-col>
                <el-pagination
                        @current-change="CurrentPageChange"
                        :current-page="1"
                        layout="prev, pager, next, jumper"
                        :total="total_page_num">
                </el-pagination>
            </el-col>
        </el-row>
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
        name: "ParticipantsTable",
        props:['contestid'],
        data:function () {
            return {
                mode:-1,
                current_page_num:1,
                total_page_num:-1,
                tableinfo:[],
                tableheader:[],
            }
        },
        methods:{
            stageForm:function (row, col) {
                let stagelist = row.stage;
                let idx = this.tableheader.indexOf(col.label)-1;
                if((idx<0)||(idx>this.tableheader.length)) return;
                return stagelist[idx];
            },
            nameForm:function (row, col) {
                if(!this.tableinfo[0]) return;
                let personlist = row.person;
                let idx = Math.floor((this.tableheader.indexOf(col.label)-1-this.tableinfo[0].stage.length)/2);
                if((idx<0)||(idx>this.tableheader.length)) return;
                return personlist[idx].name;
            },
            emailForm:function (row, col) {
                if(!this.tableinfo[0]) return;
                let personlist = row.person;
                let idx = Math.floor((this.tableheader.indexOf(col.label)-1-this.tableinfo[0].stage.length)/2);
                if((idx<0)||(idx>this.tableheader.length)) return;
                return personlist[idx].email;
            },
            CurrentPageChange:function (val) {
                self.current_page_num=2;
                this.tableinfo=[{
                    name:'wzw',
                    email:'ffffyouxiang',
                    stage:[1,2,3],
                    person:[{
                        name:'chengyuan0',
                        email:'0email'
                    },{
                        name:'chengyuan1',
                        email:'1email'
                    }]
                }];
                axios.post('/api/admin/participants',{
                    contestid:self.contestid,
                    pageNum:val,
                }).then(function (response) {
                    self.mode = response.data.mode;
                    self.current_page_num = response.data.current_page_num;
                    self.total_page_num = response.data.total_page_num;
                    self.tableinfo=[];
                    var i=1;
                    if(self.mode==1){
                        //个人赛
                        for(let item of response.data.array){
                            let one = {};
                            one['name']=item.username;
                            one['email']=item.email;
                            one['stage']=[];
                            i=1
                            for(let point of item.points){
                                one['stage'].push(point);
                                i++;
                            }
                            self.tableinfo.push(one);
                        }
                    }
                    else if(self.mode==0){
                        //组队赛
                        for(let item of response.data.array){
                            let one = {};
                            one['name']=item.captainName;
                            one['stage']={};
                            i=1;
                            for(let point of item.captainPoints){
                                one['stage'].push(point);
                                i++;
                            }
                            i=1;
                            one['person']=[];
                            for(let person of item.group){
                                one['person'].push({
                                    name:person.username,
                                    email:person.email,
                                });
                            }
                            self.tableinfo.push(one);
                        }
                    }
                }).catch(function (error) {
                    console.log(error)
                });
            }
        },
        created:function () {
            var self = this;
            this.mode = 0;
            this.current_page_num=1;
            this.total_page_num=50;
            this.tableinfo=[{
                name:'王兆伟',
                email:'fyouxiang',
                stage:[1,2,3],
                person:[{
                    name:'chengyuan0',
                    email:'0email'
                },{
                    name:'chengyuan1',
                    email:'1email'
                }]
            }]
            self.tableheader=[];
            self.tableheader.push('名称');
            //self.tableheader.push('邮箱');
            self.tableheader.push('阶段0分数');
            self.tableheader.push('阶段1分数');
            self.tableheader.push('阶段2分数');
            self.tableheader.push('成员0姓名');
            self.tableheader.push('成员0邮箱');
            self.tableheader.push('成员1姓名');
            self.tableheader.push('成员1邮箱');

            axios.post('/api/admin/participants',{
                contestid:self.contestid,
                pageNum:1,
            }).then(function (response) {
                self.mode = response.data.mode;
                self.current_page_num = response.data.current_page_num;
                self.total_page_num = response.data.total_page_num;
                self.tableinfo=[];
                self.tableheader=[];
                var i=1;
                if(self.mode==1){
                    //个人赛
                    for(let item of response.data.array){
                        let one = {};
                        one['name']=item.username;
                        one['email']=item.email;
                        one['stage']=[];
                        i=1;
                        for(let point of item.points){
                            one['stage'].push(point);
                            i++;
                        }

                        self.tableinfo.push(one);
                    }
                    self.tableheader.push('名称');
                    self.tableheader.push('邮箱');
                    for(let idx in self.tableinfo[0].stage){
                        self.tableheader.push('阶段'+idx+'分数');
                    }
                }
                else if(self.mode==0){
                    //组队赛
                    for(let item of response.data.array){
                        let one = {};
                        one['name']=item.captainName;
                        one['stage']={};
                        i=1;
                        for(let point of item.captainPoints){
                            one['stage'].push(point);
                            i++;
                        }
                        i=1;
                        one['person']=[];
                        for(let person of item.group){
                            one['person'].push({
                                name:person.username,
                                email:person.email,
                            });
                        }
                        self.tableinfo.push(one);
                    }
                    self.tableheader.push('名称');
                    for(let idx in self.tableinfo[0].stage){
                        self.tableheader.push('阶段'+idx+'分数');
                    }
                    for(let idx in self.tableinfo[0].person){
                        self.tableheader.push('成员'+idx+'名称');
                        self.tableheader.push('成员'+idx+'邮箱');
                    }
                }
            }).catch(function (error) {
                console.log(error)
            });
        }
    }
</script>

<style scoped>
</style>