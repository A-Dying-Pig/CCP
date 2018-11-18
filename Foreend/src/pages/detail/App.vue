<template><div id="app">
    <el-container>
        <el-header>
            <NavigationBar :username="username"></NavigationBar>
        </el-header>
        <el-main>
            <CompetitionDetailAllInfo :info="info"></CompetitionDetailAllInfo>

            <CompetitionDetailContents :info="info" :showlist="showlist">
                <template slot="details">{{ info.basicinfo.details }}</template>
            </CompetitionDetailContents>
        </el-main>
    </el-container>
    </div>
</template>
<script>

    import NavigationBar from "../../components/NavigationBar";
    import CompetitionDetailAllInfo from '../../components/CompetitionDetailAllInfo';
    import CompetitionDetailContents from '../../components/CompetitionDetailContents';
    import axios from 'axios'
    export default {
        components: {NavigationBar,CompetitionDetailAllInfo,CompetitionDetailContents},
        props:{'contestId':{
            type:Number,
                default:NaN
    },'username':{
            type:String,
                default:''
    }},
        data:function () {
            return{
                info:{
                    basicinfo:{
                        name:'小程序开发',
                        holders:['软件学院'],
                        sponsors:['没有'],
                        comtype:'小程序开发',
                        details:"这里是比赛详情",
                    },
                    signupinfo:{
                        time:[1542272805000,1542273805000],
                        mode:'个人赛',
                        person:[
                            ''
                        ],
                        group:[
                        ]
                    },
                    stageinfo:[{
                        name:'初赛',
                        details:'初赛详情',
                        handTimeEnd:1542284805000,
                        evaluationTimeEnd:1542285805000,
                        mode:'在线预览'
                    }]
                },
                showlist:[{
                    value:'gradework',
                    label:'评委评分'
                },{
                    value:'submitwork',
                    label:'提交作品'
                },{
                    value:'infochange',
                    label:'修改信息'
                }]
            }
        },
        mounted:function () {
            var self = this;
            this.showlist=[];
            for(let item of this.canshowlist){
                if(item==='details'){
                    this.showlist.append({value:'details',label:'详细信息'})
                }
                else if(item === 'gradework'){
                    this.showlist.append({
                        value:'gradework',
                        label:'评委评分'
                })}
                else if(item === 'submitwork'){
                    this.showlist.append({
                        value:'submitwork',
                        label:'提交作品'
                    })}
                else if(item === 'infochange'){
                    this.showlist.append({
                        value:'infochange',
                        label:'修改信息'
                    })}
            }
            //get info
            axios.post('/api/competition/detail',{
                contestId:self.contestId,
            }).then(function (response) {
                this.info = response.data.info;
                let type = resp.data.type;
                //
            }).catch(function (error) {
                console.log('/api/competition/detail?contestId='+this.contestId+'错误！！')
            })
        }
    }
</script>
<style></style>