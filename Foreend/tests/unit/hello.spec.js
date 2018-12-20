import App from '../../src/pages/detail/App.vue'
//import Counter from '../../src/components/Counter.vue'
import moxios from 'moxios'
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI);
import { shallowMount } from '@vue/test-utils'
describe('detail页面App.vue', () => {
    beforeEach(function () {
        // import and pass your custom axios instance to this method
        moxios.install()
    });

    afterEach(function () {
        // import and pass your custom axios instance to this method
        moxios.uninstall()
    });
    console.log(111)
    it('just for a single spec', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(App);
            console.log(wrapper.vm.allinfo)
            wrapper.vm.getInfo();
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                request.respondWith({
                    status: 200,
                    response: {
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
                        }]}
                }).then(function () {
                    done()
                    console.log('111111111111111111111~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                    console.log(wrapper.vm.showlist)
                    console.log(wrapper.vm.allinfo)
                    expect(wrapper.vm.info).toEqual({
                        id: 12345, firstName: 'Fred', lastName: 'Flinstone'
                    })
                    done();
                })
            })
        })
    });

});