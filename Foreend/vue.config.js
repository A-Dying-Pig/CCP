module.exports = {
  pages: {
      register:{
          entry: 'src/pages/register/main.js',
          template: 'src/pages/register/register.html',
          filename: 'register.html',
      },
      CompetitionCreate:{
          entry: 'src/pages/CompetitonCreate/main.js',
          template: 'src/pages/CompetitonCreate/index.html',
          //filename: 'CompetitonCreate.html',
          filename: 'index.html',
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
      CompetitionList:{
          entry: 'src/pages/CompetitionList/main.js',
          template: 'src/pages/CompetitionList/CompetitionList.html',
          filename: 'CompetitionList.html',
      }
  },
    outputDir:'static',
    baseUrl:'',
}