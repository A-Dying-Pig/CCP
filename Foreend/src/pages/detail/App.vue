<template><div id="app">
    <el-container>
        <el-header>
            <NavigationBar :username="username"></NavigationBar>
        </el-header>
        <el-main>
            <CompetitionDetailAllInfo :info="info" :type="type" :contestid="contestid"></CompetitionDetailAllInfo>

            <CompetitionDetailContents :info="info" :showlist="showlist" :contestid="contestid" :type="type">
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
        props:{'contestid':{
            type:Number,
                default:-1
    },'username':{
            type:String,
                default:''
    }},
        data:function () {
            return{
                info:{
                    basicinfo:{
                        name:'111',
                        holders:[''],
                        sponsors:[''],
                        comtype:'',
                        details:"222",
                    },
                    signupinfo:{
                        time:[1542593167172,1542593267172],
                        mode:'',
                        person:[
                            ''
                        ],
                        group:[
                        ]
                    },
                    stageinfo:[{
                        name:'',
                        details:'',
                        stageTimeBegin:1544827739311,
                        handTimeEnd:1544838739311,
                        evaluationTimeEnd:1544839739311,
                        mode:''
                    }]
                },
                showlist:[],
                type:0,
            }
        },

        created:function () {
            let self = this;
            //get info

            self.type = 0;
            let now = Date.now();

            self.showlist=[];
            self.showlist.push({
                value:'competitionfiles',
                label:'比赛文件'
            })
            if(self.type===1){
                //当不在提交阶段时，不可以提交作品
                let showsubmit = false;
                let begin = self.info.signupinfo.time[1];
                for(let stage of self.info.stageinfo){
                    if((now>begin)&&(now<stage.handTimeEnd)){
                        showsubmit = true;
                    }
                    begin = stage.evaluationTimeEnd;
                }
                if(showsubmit){
                    self.showlist.push({
                        value:'submitwork',
                        label:'提交作品'
                    });
                }
            }
            else if(self.type===2){
                //当不在评测阶段时，不可以评测作品
                //let showgrade = false;
                let showgrade = true;
                for(let stage of self.info.stageinfo){
                    if((now<stage.evaluationTimeEnd)&&(now>stage.handTimeEnd)){
                        showgrade = true;
                    }
                }
                if(showgrade){
                    self.showlist.push({
                        value:'gradework',
                        label:'评委评分'
                    },{
                        value:'judgefinish',
                        label:'查看过往评分'
                    });
                }
            }
            else if(self.type===3){
                self.showlist.push({
                    value:'infochange',
                    label:'修改信息'
                },{
                    value:'participantstable',
                    label:'队员信息'
                });
            }
            console.log(self.contestid);
            axios.post('/api/competition/detail',{
                contestid:self.contestid,
            }).then(function (response) {
                self.info=[];
                self.info = response.data.info;
                self.type = response.data.type;
                let now = Date.now();
                self.showlist=[];
                if(self.type===1){
                    //当不在提交阶段时，不可以提交作品
                    let showsubmit = false;
                    let begin = self.info.signupinfo.time[1];
                    for(let stage of self.info.stageinfo){
                        if((now>begin)&&(now<stage.handTimeEnd)){
                            showsubmit = true;
                        }
                        begin = stage.evaluationTimeEnd;
                    }
                    if(showsubmit){
                        self.showlist.push({
                            value:'submitwork',
                            label:'提交作品'
                        });
                    }
                }
                else if(self.type===2){
                    //当不在评测阶段时，不可以评测作品
                    let showgrade = false;
                    for(let stage of self.info.stageinfo){
                        if((now<stage.evaluationTimeEnd)&&(now>stage.handTimeEnd)){
                            showgrade = true;
                        }
                    }
                    if(showgrade){
                        self.showlist.push({
                            value:'gradework',
                            label:'评委评分'
                        },{
                            value:'judgefinish',
                            label:'查看过往评分'
                        });
                    }
                }
                else if(self.type===3){
                    console.log(333);
                    self.showlist.push({
                        value:'infochange',
                        label:'修改信息'
                    });
                    self.showlist.push({
                        value:'participantstable',
                        label:'选手信息'
                    });
                    self.showlist.push({
                        value:'judgelist',
                        label:'评委信息'
                    });
                }
            }).catch(function (error) {
                console.log('/api/competition/detail'+'错误！！')
            })
        }
    }
</script>
<style></style>