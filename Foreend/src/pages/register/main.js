import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI)
Vue.use(VueResource)
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
