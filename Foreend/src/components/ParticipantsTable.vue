<template>
    <div>
        <el-row type="flex" justify="center">
            <el-col>
                本阶段共有{{ allnum }}组晋级，已有{{ submitnum }}份提交。
            </el-col>
        </el-row>
        <el-row type="flex" justify="center">
            <el-col>
                <el-table :data="tableinfo" border style="width: 100%;">
                    <el-table-column prop="name" label="名称" fixed></el-table-column>
                    <el-table-column v-if="mode === 1" prop="email" label="邮箱"></el-table-column>
                    <el-table-column v-for="(item,index) in tableinfo[0].stage" :formatter="stageForm" :label="'阶段'+(index+1)+'分数'" :key="item.key"></el-table-column>
                    <template v-if="mode === 0">
                        <template v-for="(item,index) in tableinfo[0].person">
                            <el-table-column :formatter="nameForm" :label="'成员'+index+'名称'"  :key="item.key"></el-table-column>
                            <el-table-column :formatter="emailForm" :label="'成员'+index+'邮箱'"  :key="item.key"></el-table-column>
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
    //import axios from 'axios'
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
                allnum:0,
                submitnum:0,
            }
        },
        methods:{
            stageForm:function (row, col) {
                if(this.mode < 0 ) return;
                let stagelist = row.stage;
                let idx = this.tableheader.indexOf(col.label)-1;
				if(this.mode===1) idx = idx - 1;
                console.log(col.label,idx);
                console.log(this.tableheader)
                if((idx<0)||(idx>this.tableheader.length)) return;
                return stagelist[idx];
            },
            nameForm:function (row, col) {
                if(!this.tableinfo[0]) return;
                let personlist = row.person;
                let idx = Math.floor((this.tableheader.indexOf(col.label)-1-this.tableinfo[0].stage.length)/2);
                if((idx<0)||(idx>this.tableheader.length)) return;
                console.log(personlist[idx]);
                if(personlist[idx]===undefined){
                    return '无'
                }
                return personlist[idx].name;
            },
            emailForm:function (row, col) {
                if(!this.tableinfo[0]) return;
                let personlist = row.person;
                let idx = Math.floor((this.tableheader.indexOf(col.label)-1-this.tableinfo[0].stage.length)/2);
                if((idx<0)||(idx>this.tableheader.length)) return;
                if(personlist[idx]===undefined){
                    return '无'
                }
                return personlist[idx].email;
            },
            CurrentPageChange:function (val) {
                self.current_page_num=0;
                axios.post('/api/admin/participants',{
                    contestid:self.contestid,
                    pageNum:val,
                }).then(function (response) {
                    self.mode = response.data.mode;
                    self.current_page_num = response.data.current_page_num;
                    self.total_page_num = response.data.total_page_num;
                    self.tableinfo=[];
                    let i=1;
                    if(self.mode===1){
                        //个人赛
                        for(let item of response.data.array){
                            let one = {};
                            one['name']=item.username;
                            one['email']=item.email;
                            one['stage']=[];
							console.log(item);
                            i=1;
                            for(let point of item.points){
                                one['stage'].push(point);
                                i++;
                            }
                            self.tableinfo.push(one);
                        }
                    }
                    else if(self.mode===0){
                        //组队赛
                        for(let item of response.data.array){
                            let one = {};
                            one['name']=item.captainName;
                            one['stage']=[];
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
            this.current_page_num=0;
            this.total_page_num=0;
            this.tableinfo=[];
            axios.post('/api/admin/participants',{
                contestid:self.contestid,
                pageNum:1,
            }).then(function (response) {
                self.mode = response.data.mode;
                self.current_page_num = response.data.current_page_num;
                self.total_page_num = response.data.total_page_num;
                self.tableinfo=[];
                self.tableheader=[];
                let i=1;
                if(self.mode===1){
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
                        let tidx = parseInt(idx) + 1;
                        self.tableheader.push('阶段'+tidx+'分数');
                    }
                }
                else if(self.mode===0){
                    //组队赛
                    for(let item of response.data.array){
                        let one = {};
                        one['name']=item.captainName;
                        one['stage']=[];
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
                        let tidx = parseInt(idx) + 1;
                        self.tableheader.push('阶段'+tidx+'分数');
                    }
                    for(let idx in self.tableinfo[0].person){
                        self.tableheader.push('成员'+idx+'名称');
                        self.tableheader.push('成员'+idx+'邮箱');
                    }
                }
            }).catch(function (error) {
                console.log(error)
            });

            axios.post('/api/admin/getsubmitnum',{
                contestid:self.contestid
            }).then(function (response) {
                if(response.data.msg!==''){
                    self.$message({
                        message:response.data.msg,
                        type:'error'
                    });
                    return
                }
                self.allnum = response.data.allnum;
                self.submitnum = response.data.submitnum;
            }).catch(function () {
                self.$message({
                    message:'获取提交作品数量错误！',
                    type:'error'
                });
            })
        }
    }
</script>

<style scoped>
</style>