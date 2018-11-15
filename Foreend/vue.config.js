module.exports = {
  pages: {
	  index: {
          entry: 'src/pages/index/main.js',
          template: 'src/pages/index/index.html',
          filename: 'index.html',
      },
      register:{
          entry: 'src/pages/register/main.js',
          template: 'src/pages/register/register.html',
          filename: 'register.html',
      },
      CompetitionCreate:{
          entry: 'src/pages/CompetitonCreate/main.js',
          template: 'src/pages/CompetitonCreate/index.html',
          filename: 'CompetitonCreate.html',
      },
      login:{
          entry: 'src/pages/login/main.js',
          template: 'src/pages/login/login.html',
          filename: 'login.html',
      },
      enroll:{
          entry: 'src/pages/enroll/main.js',
          template: 'src/pages/enroll/enroll.html',
          filename: 'enroll.html',
      }
  },
    devServer:{
      index:'static/CompetitonCreate.html'
    },
    outputDir:'static',
    baseUrl:'',
  //indexPath:'./../templates/index.html',
}