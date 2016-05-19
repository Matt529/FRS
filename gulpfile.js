// Gulp Plugins
var gulp = require('gulp'),
    sass = require('gulp-sass'),
    gutil = require('gulp-util'),
    sourcemaps = require('gulp-sourcemaps'),
    clean = require('gulp-clean'),
    typescript = require('gulp-typescript'),
    concat = require('gulp-concat');

var merge = require('merge2');  // Merging Gulp Streams
var path = require('path');

// Directory Root Constants
const STATIC_ROOT = path.join('.', 'static');
const STATIC_FRS_ROOT = path.join(STATIC_ROOT, 'frs');

const COMPILED_ROOT = path.join(STATIC_ROOT, 'compiled');
const COMPILED_FRS_ROOT = path.join(COMPILED_ROOT, 'frs');

// TypeScript Constants
const TS_SRC = path.join(STATIC_FRS_ROOT, 'ts', '**', '*.ts');       // Glob for selecting .ts files (for compilation)
const TS_SRC_DTS = path.join(STATIC_FRS_ROOT, 'ts', '**', '*.d.ts'); // Glob for selecting .d.ts files specifically
const TS_OUT = path.join(COMPILED_FRS_ROOT, 'ts');                   // Destination directory

const TS_CLEAN_DTS = path.join(COMPILED_ROOT, '**', 'ts', '**', '*.ts');    // Glob for cleaning compiled .d.ts files
const TS_CLEAN_OUT_JS = path.join(COMPILED_ROOT, '**', 'ts', '**', '*.js'); // Glob for cleaning compiled .js files

// SASS Constants
const SASS_SRC = path.join(STATIC_FRS_ROOT, 'css', '**', '*.scss');     // Glob for selecting .scss files (for compilation
const SASS_OUT = path.join(COMPILED_FRS_ROOT, 'css');                  // Destination Directory

const SASS_CLEAN_CSS = path.join(COMPILED_FRS_ROOT, 'css', '**', '*.css');  // Glob for cleaning compiled css files
const SASS_CLEAN_MAP = path.join(COMPILED_FRS_ROOT, 'css', '**', '*.map');  // Glob for cleaning compiled .map files (sourcemaps)

function cleanSass() {
    return gulp.src([SASS_CLEAN_CSS, SASS_CLEAN_MAP])
        .pipe(clean())
        .on('error', gutil.log);
}

function cleanTypescript() {
    return gulp.src([TS_CLEAN_DTS, TS_CLEAN_OUT_JS])
        .pipe(clean())
        .on('error', gutil.log);
}

function buildSass() {
    return gulp.src(SASS_SRC)
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(SASS_OUT))
        .on('error', gutil.log);
}

function buildDefinitions() {
    return gulp.src(TS_SRC_DTS)
        .pipe(gulp.dest(TS_OUT))
        .on('error', gutil.log);
}

function buildTypescript() {
    var tsResult = gulp.src(TS_SRC)
        .pipe(sourcemaps.init())
        .pipe(typescript({
            declaration: true,
            noExternalResolve: true,
            target: 'ES5'
        }));
    return merge([
        tsResult.dts.pipe(gulp.dest(TS_OUT)).on('error', gutil.log),
        tsResult.js.pipe(sourcemaps.write()).pipe(gulp.dest(TS_OUT)).on('error', gutil.log)
    ]);
}

// Cleaning and Building can be run in parallel, but rebuilding requires cleaning be done before building
var cleanFn = gulp.parallel(cleanSass, cleanTypescript);
var buildFn = gulp.parallel(buildSass, buildTypescript, buildDefinitions);
var rebuildFn = gulp.series(cleanFn, buildFn);


// Task Definitions
gulp.task('clean', cleanFn);
gulp.task('build', buildFn);
gulp.task('rebuild', rebuildFn);
gulp.task('default', rebuildFn);