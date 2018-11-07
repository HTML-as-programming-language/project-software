var gulp = require('gulp'),
    uglify = require('gulp-uglify'),
    plumber = require('gulp-plumber'),
    browserSync = require('browser-sync');

var reload = browserSync.reload;
var exec = require('child_process').exec;

//Run Flask server
gulp.task('runserver', function() {
    var proc = exec('python server.py');
});

// Default task: Watch Files For Changes & Reload browser
gulp.task('default', ['runserver'], function () {
  browserSync({
    notify: false,
    proxy: "127.0.0.1:5003"
  });
 
  gulp.watch(['templates/*.*'], reload);
  gulp.watch(['server.py'], reload);

});