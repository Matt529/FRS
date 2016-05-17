var gulp = require('gulp'),
    sass = require('gulp-sass'),
    gutil = require('gulp-util'),
    sourcemaps = require('gulp-sourcemaps'),
    clean = require('gulp-clean'),
    typescript = require('gulp-typescript');

// File Watchers (When files change these will build their respective file types)
gulp.task('watch:sass', function(){

});

gulp.task('watch:typescript', function(){

});

gulp.task('watch', ['watch:sass', 'watch:typescript']);

// File Cleaners, should clear any build directories for their respective file types
gulp.task('clean-sass', function(){

});

gulp.task('clean-typescript', function() {

});

gulp.task('clean', ['clean-sass', 'clean-typescript']);


// Builders, should build thier respective file types to their respective build directories
gulp.task('build-sass', function() {

});

gulp.task('build-typescript', function() {

});

gulp.task('build', ['build-sass', 'build-typescript']);

// Clean and Build = Rebuilding files
gulp.task('rebuild', ['clean', 'build']);

// 'default' is what is run when just 'gulp' is entered into the command line with no task name specified
gulp.task('default', ['rebuild', 'watch']);