// Gulp Plugins
var gulp = require('gulp'),
    sass = require('gulp-sass'),
    gutil = require('gulp-util'),
    sourcemaps = require('gulp-sourcemaps'),
    clean = require('gulp-clean'),
    scsslint = require('gulp-scss-lint'),
    tslint = require('gulp-tslint'),
    flatten = require('gulp-flatten'),
    gulpFilter = require('gulp-filter'),
    gulpWebpack = require('gulp-webpack');

var path = require('path');

// Directory Root Constants
const STATIC_ROOT = path.join('.', 'static');
const STATIC_FRS_ROOT = path.join(STATIC_ROOT, 'global');

const COMPILED_ROOT = path.join(STATIC_ROOT, 'compiled');
const COMPILED_FRS_ROOT = path.join(COMPILED_ROOT, 'global');

// TypeScript Constants
const TS_SRC = path.join(STATIC_FRS_ROOT, 'ts', '**', '*.ts');       // Glob for selecting .ts files (for compilation)
const JS_SRC = path.join(STATIC_FRS_ROOT, 'js', '**', '*.js');
const JS_OUT = path.join(COMPILED_FRS_ROOT, 'js');                   // Destination directory

const TS_CLEAN_DTS = path.join(COMPILED_ROOT, '**', '*.ts');            // Glob for cleaning compiled .d.ts files
const JS_CLEAN_DIRS = path.join(COMPILED_ROOT, '**', '*.js');         // Glob for cleaning compiled .js files

// SASS Constants
const SASS_SRC = path.join(STATIC_FRS_ROOT, '**', '*.scss');            // Glob for selecting .scss files (for compilation
const SASS_OUT = path.join(COMPILED_FRS_ROOT, 'css');                   // Destination Directory

function ignorePath(path) {
    return "!" + path;
}

const SCSS_LINT_SELECTS = [
    SASS_SRC,
    ignorePath(path.join(path.dirname(SASS_SRC), '_prefix-mixins.scss'))
];

const JS_WEBPACK_SELECTS = [
    ignorePath(path.join(path.dirname(JS_SRC), '*-analytics.js'))
];

const SASS_CLEAN_CSS = path.join(COMPILED_FRS_ROOT, 'css', '**', '*.css');  // Glob for cleaning compiled css files
const SASS_CLEAN_MAP = path.join(COMPILED_FRS_ROOT, 'css', '**', '*.map');  // Glob for cleaning compiled .map files (sourcemaps)

/**
 * Cleans out compiled SCSS files, inherently this also deletes any css files that exist under global/css
 */
function cleanSass() {
    return gulp.src([SASS_CLEAN_CSS, SASS_CLEAN_MAP])
        .pipe(clean())
        .on('error', gutil.log);
}

function cleanTypescriptDefs() {
    return gulp.src(TS_CLEAN_DTS)
        .pipe(clean())
        .on('error', gutil.log);
}

/**
 * Removes all *.js and *.ts (including *.d.ts) files under global/js
 */
function cleanJavascript() {
    return gulp.src(JS_CLEAN_DIRS)
        .pipe(clean())
        .on('error', gutil.log);
}

/**
 * Lints and transpiles *.scss files to *.js files, storing them under compiled/global/js with relative paths below
 * the ts parent directory.
 */
function buildSass() {
    var copiedIncludes = gulpFilter(SCSS_LINT_SELECTS, {restore: true});

    return gulp.src(SASS_SRC)
        .pipe(copiedIncludes)
        .pipe(scsslint({
            'config': '.scss-lint.yml',             // config file
            'verbose': true
        }))
        .pipe(copiedIncludes.restore)
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))    // Compile scss files and their sourcemaps, printing errors
        .pipe(sourcemaps.write())
        .pipe(flatten({subPath: [3]}))              // Remove 'ts' parent directory by slicing parent directories
        .pipe(gulp.dest(SASS_OUT))
        .on('error', gutil.log);                    // Pretty logging
}

function lintTypescript() {
    return gulp.src([TS_SRC])
        .pipe(tslint({
            configuration: path.join('.', 'tslint.json'),
            formatter: "verbose"
        }))
        .pipe(tslint.report({
            summarizeFailureOutput: true,
            emitError: true
        }));
}

function buildBundle() {
    select = gulpFilter(JS_WEBPACK_SELECTS);
    return gulp.src([TS_SRC, JS_SRC])
        .pipe(select)
        .pipe(gulpWebpack(require('./webpack.config.js'), require('webpack')))
        .pipe(gulp.dest(JS_OUT))
        .on('error', gutil.log);
}

function copyJavascript() {
    return gulp.src(JS_SRC)
        .pipe(flatten({subPath:[3]}))
        .pipe(gulp.dest(JS_OUT))
        .on('error', gutil.log);
}

// Cleaning and Building can be run in parallel, but rebuilding requires cleaning be done before building
var cleanJsAndTs = gulp.parallel(cleanTypescriptDefs, cleanJavascript);
var cleanFn = gulp.parallel(cleanSass, cleanJsAndTs);
var lintFn = gulp.parallel(lintTypescript);
var bundleFn = gulp.series(lintFn, buildBundle);
var buildFn = gulp.parallel(buildSass, copyJavascript, bundleFn);
var rebuildFn = gulp.series(cleanFn, buildFn);


// Task Definitions
gulp.task('buildSass', buildSass);

gulp.task('clean', cleanFn);
gulp.task('build', buildFn);
gulp.task('rebuild', rebuildFn);
gulp.task('default', rebuildFn);
