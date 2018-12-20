import App from '../../src/pages/detail/App.vue'
import moxios from 'moxios'
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI);
import { shallowMount } from '@vue/test-utils'
describe('detail页面App.vue的info赋值', () => {
    let resdata = {
        info:{
            basicinfo:{
                name:'121',
                holders:[''],
                sponsors:[''],
                comtype:'',
                details:"222",
                beginjudgebutton:false
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
            }]},
        msg:'',
        type:1
    };

    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });

    it('发送ajax请求，检查info的赋值是否正确', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(App);
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                request.respondWith({
                    status: 200,
                    response: resdata
                }).then(function () {
                    expect(wrapper.vm.allinfo).toEqual(resdata.info);
                    done();
                })
            })
        })
    });
});

describe('detail页面App.vue的根据type，指定正确的showlist.游客', () => {
    let resdata = {
        info:{
            basicinfo:{
                name:'121',
                holders:[''],
                sponsors:[''],
                comtype:'',
                details:"222",
                beginjudgebutton:false
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
            }]},
        msg:'',
        type:0
    };

    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });

    resdata.type = 0;
    it('type = 0，游客', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(App);
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let corshow = [{
                    value:'competitionfiles',
                    label:'比赛文件'
                },{
                    value:'discussion',
                    label:'讨论区'
                },];
                request.respondWith({
                    status: 200,
                    response: resdata
                }).then(function () {
                    expect(wrapper.vm.type).toEqual(resdata.type);
                    expect(wrapper.vm.showlist).toEqual(corshow);
                    done();
                })
            })
        })
    });

});

describe('detail页面App.vue的根据type，指定正确的showlist.选手', () => {
    let resdata = {
        info: {
            basicinfo: {
                name: '121',
                holders: [''],
                sponsors: [''],
                comtype: '',
                details: "222",
                beginjudgebutton: false
            },
            signupinfo: {
                time: [1542593167172, 1542593267172],
                mode: '',
                person: [
                    ''
                ],
                group: []
            },
            stageinfo: [{
                name: '',
                details: '',
                stageTimeBegin: 1544827739311,
                handTimeEnd: 1544838739311,
                evaluationTimeEnd: 1544839739311,
                mode: ''
            }]
        },
        msg: '',
        type: 0
    };

    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });

    resdata.type = 1;
    it('type = 1，选手', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(App);
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let corshow = [{
                    value:'competitionfiles',
                    label:'比赛文件'
                },{
                    value:'discussion',
                    label:'讨论区'
                },{
                    value:'submitwork',
                    label:'提交作品'
                },];
                request.respondWith({
                    status: 200,
                    response: resdata
                }).then(function () {
                    expect(wrapper.vm.type).toEqual(resdata.type);
                    expect(wrapper.vm.showlist).toEqual(corshow);
                    done();
                })
            })
        })
    });
});

describe('detail页面App.vue的根据type，指定正确的showlist.选手', () => {
    let resdata = {
        info: {
            basicinfo: {
                name: '121',
                holders: [''],
                sponsors: [''],
                comtype: '',
                details: "222",
                beginjudgebutton: false
            },
            signupinfo: {
                time: [1542593167172, 1542593267172],
                mode: '',
                person: [
                    ''
                ],
                group: []
            },
            stageinfo: [{
                name: '',
                details: '',
                stageTimeBegin: 1544827739311,
                handTimeEnd: 1544838739311,
                evaluationTimeEnd: 1544839739311,
                mode: ''
            }]
        },
        msg: '',
        type: 0
    };

    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });


    resdata.type = 2;
    it('type = 2，评委', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(App);
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let corshow = [{
                    value:'competitionfiles',
                    label:'比赛文件'
                },{
                    value:'discussion',
                    label:'讨论区'
                },{
                    value:'gradework',
                    label:'评委评分'
                },{
                    value:'judgefinish',
                    label:'查看过往评分'
                }];
                request.respondWith({
                    status: 200,
                    response: resdata
                }).then(function () {
                    expect(wrapper.vm.type).toEqual(resdata.type);
                    expect(wrapper.vm.showlist).toEqual(corshow);
                    done();
                })
            })
        })
    });
});

describe('detail页面App.vue的根据type，指定正确的showlist.选手', () => {
    let resdata = {
        info: {
            basicinfo: {
                name: '121',
                holders: [''],
                sponsors: [''],
                comtype: '',
                details: "222",
                beginjudgebutton: false
            },
            signupinfo: {
                time: [1542593167172, 1542593267172],
                mode: '',
                person: [
                    ''
                ],
                group: []
            },
            stageinfo: [{
                name: '',
                details: '',
                stageTimeBegin: 1544827739311,
                handTimeEnd: 1544838739311,
                evaluationTimeEnd: 1544839739311,
                mode: ''
            }]
        },
        msg: '',
        type: 0
    };

    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });

    resdata.type = 3;
    it('type = 3，管理员', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(App);
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let corshow = [{
                    value:'competitionfiles',
                    label:'比赛文件'
                },{
                    value:'discussion',
                    label:'讨论区'
                },{
                    value: 'infochange',
                    label: '修改信息'
                },{
                    value: 'participantstable',
                    label: '选手信息'
                },{
                    value: 'judgelist',
                    label: '评委信息'
                },{
                    value: 'advancedparticipants',
                    label: '设置晋级选手名单'
                }];
                request.respondWith({
                    status: 200,
                    response: resdata
                }).then(function () {
                    expect(wrapper.vm.type).toEqual(resdata.type);
                    expect(wrapper.vm.showlist).toEqual(corshow);
                    done();
                })
            })
        })
    });
});