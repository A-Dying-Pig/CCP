import CompetitionDetailAllinfo from '../../src/components/CompetitionDetailAllInfo.vue'
import moxios from 'moxios'
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI);
import { shallowMount } from '@vue/test-utils'
const { getComputedStyle } = window
window.getComputedStyle = function getComputedStyleStub(el) {
    return {
        ...getComputedStyle(el),
        transitionDelay: '',
        transitionDuration: '',
        animationDelay: '',
        animationDuration: '',
    }
};
describe('props传值是否正确', () => {
    let info = {
            basicinfo:{
                name:'121',
                holders:['1'],
                sponsors:['2'],
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
            }]};
    let type = 1;
    let contestid = 5;
    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });
    it('prop传值成功', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(CompetitionDetailAllinfo, {
                propsData: {
                    info: info,
                    type: type,
                    contestid: contestid
                }
            });
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let enrollnum = 100;
                request.respondWith({
                    status: 200,
                    response: {
                        enrollnum: enrollnum,
                        msg: ''
                    }
                }).then(function () {
                    expect(wrapper.vm.info).toEqual(info);
                    expect(wrapper.vm.type).toEqual(type);
                    expect(wrapper.vm.contestid).toEqual(contestid);
                    done();
                })
            });
        });
    });
});

describe('axios获取已经报名人数正确', () => {
    let info = {
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
        }]};
    let type = 1;
    let contestid = 5;
    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });
    it('获取组队信息的request与结果均正确', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(CompetitionDetailAllinfo, {
                propsData: {
                    info: info,
                    type: type,
                    contestid: contestid
                }
            });
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let enrollnum = 100;
                console.log(request.config.data)
                expect(request.config.data).toEqual(JSON.stringify({"contestid":contestid}));
                request.respondWith({
                    status: 200,
                    response: {
                        enrollnum: enrollnum,
                        msg: ''
                    }
                }).then(function () {
                    expect(wrapper.vm.enrollnum).toEqual(enrollnum);
                    done();
                })
            });
        });
    });
});

describe('timestamp2datestr函数', () => {
    let info = {
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
        }]};
    let type = 1;
    let contestid = 5;
    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });
    it('showdetail模式', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(CompetitionDetailAllinfo, {
                propsData: {
                    info: info,
                    type: type,
                    contestid: contestid
                }
            });
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let enrollnum = 100;
                console.log(request.config.data)
                expect(request.config.data).toEqual(JSON.stringify({"contestid":contestid}));
                request.respondWith({
                    status: 200,
                    response: {
                        enrollnum: enrollnum,
                        msg: ''
                    }
                }).then(function () {
                    let now = new Date(1545651445689);
                    let resstr = wrapper.vm.timestamp2datestr(now.getTime(),true);
                    expect(resstr).toEqual('12月24日19时37分')
                    done();
                })
            });
        });
    });

    it('非showdetail模式', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(CompetitionDetailAllinfo, {
                propsData: {
                    info: info,
                    type: type,
                    contestid: contestid
                }
            });
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let enrollnum = 100;
                console.log(request.config.data)
                expect(request.config.data).toEqual(JSON.stringify({"contestid":contestid}));
                request.respondWith({
                    status: 200,
                    response: {
                        enrollnum: enrollnum,
                        msg: ''
                    }
                }).then(function () {
                    let now = new Date(1545651445689);
                    let resstr = wrapper.vm.timestamp2datestr(now.getTime(),false);
                    expect(resstr).toEqual('12月24日')
                    done();
                })
            });
        });
    });
});

describe('timestamp2datestr函数', () => {
    let info = {
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
        }]};
    let type = 1;
    let contestid = 5;
    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });
    it('showdetail模式', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(CompetitionDetailAllinfo, {
                propsData: {
                    info: info,
                    type: type,
                    contestid: contestid
                }
            });
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let enrollnum = 100;
                console.log(request.config.data);
                expect(request.config.data).toEqual(JSON.stringify({"contestid":contestid}));
                request.respondWith({
                    status: 200,
                    response: {
                        enrollnum: enrollnum,
                        msg: ''
                    }
                }).then(function () {
                    let now = new Date(1545651445689);
                    let resstr = wrapper.vm.timestamp2datestr(now.getTime(),true);
                    expect(resstr).toEqual('12月24日19时37分');
                    done();
                })
            });
        });
    });

    it('非showdetail模式', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(CompetitionDetailAllinfo, {
                propsData: {
                    info: info,
                    type: type,
                    contestid: contestid
                }
            });
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let enrollnum = 100;
                console.log(request.config.data)
                expect(request.config.data).toEqual(JSON.stringify({"contestid":contestid}));
                request.respondWith({
                    status: 200,
                    response: {
                        enrollnum: enrollnum,
                        msg: ''
                    }
                }).then(function () {
                    let now = new Date(1545651445689);
                    let resstr = wrapper.vm.timestamp2datestr(now.getTime(),false);
                    expect(resstr).toEqual('12月24日')
                    done();
                })
            });
        });
    });
});