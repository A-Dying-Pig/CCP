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
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

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
                showlist:[]
            }
        },
        created:function () {
            var self = this;
            //get info

            axios.post('/api/competition/detail',{
                contestId:self.contestId,
            }).then(function (response) {
                self.info = response.data.info;
                let type = response.data.type;
                //
                self.showlist=[];
                if(type==1){
                    self.showlist.push({
                        value:'submitwork',
                        label:'提交作品'
                    });
                }
                else if(type==2){
                    self.showlist.push({
                        value:'gradework',
                        label:'评委评分'
                    });
                }
                else if(type==3){
                    self.showlist.push({
                        value:'infochange',
                        label:'修改信息'
                    });
                }
            }).catch(function (error) {
                console.log('/api/competition/detail'+'错误！！')
            })
        }
    }
</script>
<style></style>