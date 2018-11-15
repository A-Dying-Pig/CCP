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
          filename: 'CompetitonCreate.html',
      },
      login:{
          entry: 'src/pages/login/main.js',
          template: 'src/pages/login/login.html',
          filename: 'login.html',
      },
      CompetitionDetail:{
          entry: 'src/pages/CompetitonDetail/main.js',
          template: 'src/pages/CompetitonDetail/index.html',
          filename: 'CompetitonDetail.html',
      }
  },
    outputDir:'static',
    baseUrl:'',
}