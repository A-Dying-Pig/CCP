module.exports = {
  pages: {
      test:{
          entry: 'src/pages/test/main.js',
          template:'src/pages/test/test.html',
          filename:'test.html',
      },
      index: {
          entry: 'src/pages/index/main.js',
          template: 'src/pages/index/index.html',
          filename: 'index.html',
      },
      register{
          entry: 'src/pages/register/main.js',
          template: 'src/pages/register/register.html',
          filename: 'register.html',
      }
  },
  outputDir:'static',
  indexPath:'./../templates/index.html',
}