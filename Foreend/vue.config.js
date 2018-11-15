module.exports = {
  pages: {
      register:{
          entry: 'src/pages/register/main.js',
          template: 'src/pages/register/register.html',
          filename: 'register.html',
      },
      CompetitionCreate:{
          entry: 'src/pages/CompetitionCreate/main.js',
          template: 'src/pages/CompetitionCreate/index.html',
          filename: 'CompetitionCreate.html',
      },
      login:{
          entry: 'src/pages/login/main.js',
          template: 'src/pages/login/login.html',
          filename: 'login.html',
      },
      CompetitionDetail: {
          entry: 'src/pages/CompetitonDetail/main.js',
          template: 'src/pages/CompetitonDetail/index.html',
          filename: 'CompetitonDetail.html',
      },
      enroll: {
          entry: 'src/pages/enroll/main.js',
          template: 'src/pages/enroll/enroll.html',
          filename: 'enroll.html',
      },
      CompetitionList:{
          entry: 'src/pages/CompetitionList/main.js',
          template: 'src/pages/CompetitionList/CompetitionList.html',
          filename: 'CompetitionList.html',
      },
      person:{
          entry: 'src/pages/person/main.js',
          template: 'src/pages/person/person.html',
          filename: 'person.html',
      }
  },
    outputDir:'static',
    baseUrl:'',
}