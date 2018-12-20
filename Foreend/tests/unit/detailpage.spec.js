import App from '../../src/pages/detail/App.vue'
import moxios from 'moxios'
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI);
import { shallowMount } from '@vue/test-utils'
describe('detail页面App.vue', () => {
    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });
    it('just for a single spec', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(App);
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