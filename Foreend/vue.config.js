const output = {
    globalObject: "this",
};

const publicPath = process.env.WEBPACK_PUBLIC_PATH;
if (publicPath) {
    Object.assign(output, {publicPath});
}
module.exports = {
  pages: {
      register:{
          entry: 'src/pages/register/main.js',
          template: 'src/pages/register/register.html',
          filename: '../../templates/register.html',
      },
      addContest:{
          entry: 'src/pages/addContest/main.js',
          template: 'src/pages/addContest/addContest.html',
          filename: '../../templates/addContest.html',
      },
      login:{
          entry: 'src/pages/login/main.js',
          template: 'src/pages/login/login.html',
          filename: '../../templates/login.html',
      },
      detail: {
          entry: 'src/pages/detail/main.js',
          template: 'src/pages/detail/detail.html',
          filename: 'detail.html',
      },
      enroll: {
          entry: 'src/pages/enroll/main.js',
          template: 'src/pages/enroll/enroll.html',
          filename: '../../templates/enroll.html',
      },
      contest:{
          entry: 'src/pages/contest/main.js',
          template: 'src/pages/contest/contest.html',
          filename: '../../templates/contest.html',
      },
      profile:{
          entry: 'src/pages/profile/main.js',
          template: 'src/pages/profile/profile.html',
          filename: '../../templates/profile.html',
      },
      index:{
          entry: 'src/pages/index/main.js',
          template: 'src/pages/index/index.html',
          filename: '../../templates/index.html',
      },
      superadmin:{
          entry: 'src/pages/superadmin/main.js',
          template: 'src/pages/superadmin/superadmin.html',
          filename: '../../templates/superadmin.html',
      },
      message:{
          entry: 'src/pages/message/main.js',
          template: 'src/pages/message/message.html',
          filename: '../../templates/message.html',
      }
  },
    outputDir:'static/js',
    baseUrl:'',
    configureWebpack:{
        resolve: {
            alias: {
                'vue$': 'vue/dist/vue.esm.js'
            }
        },
        devServer: {
            watchOptions: {
                poll: true,
            },
        },
        output,
    },
    chainWebpack: config => {
        config.module
            .rule('svg')
            .use('file-loader')
            .loader('vue-svg-loader')
    },
}