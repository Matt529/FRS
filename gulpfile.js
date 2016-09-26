// Gulp Plugins
var gulp = require('gulp'),
    sass = require('gulp-sass'),
    gutil = require('gulp-util'),
    sourcemaps = require('gulp-sourcemaps'),
    clean = require('gulp-clean'),
    typescript = require('gulp-typescript'),
    concat = require('gulp-concat'),
    scsslint = require('gulp-scss-lint'),
    tslint = require('gulp-tslint'),
    flatten = require('gulp-flatten');

var merge = require('merge2');  // Merging Gulp Streams
var path = require('path');

// Directory Root Constants
const STATIC_ROOT = path.join('.', 'static');
const STATIC_FRS_ROOT = path.join(STATIC_ROOT, 'global');

const COMPILED_ROOT = path.join(STATIC_ROOT, 'compiled');
const COMPILED_FRS_ROOT = path.join(COMPILED_ROOT, 'global');

// TypeScript Constants
const TS_SRC = path.join(STATIC_FRS_ROOT, 'ts', '**', '*.ts');       // Glob for selecting .ts files (for compilation)
const TS_SRC_DTS = path.join(STATIC_FRS_ROOT, 'ts', '**', '*.d.ts'); // Glob for selecting .d.ts files specifically
const TS_OUT = path.join(COMPILED_FRS_ROOT, 'js');                   // Destination directory

const TS_CLEAN_DTS = path.join(COMPILED_ROOT, '**', '*.ts');            // Glob for cleaning compiled .d.ts files
const TS_CLEAN_OUT_JS = path.join(COMPILED_ROOT, '**', '*.js');         // Glob for cleaning compiled .js files

// SASS Constants
const SASS_SRC = path.join(STATIC_FRS_ROOT, '**', '*.scss');            // Glob for selecting .scss files (for compilation
const SASS_OUT = path.join(COMPILED_FRS_ROOT, 'css');                   // Destination Directory

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

/**
 * Removes all *.js and *.ts (including *.d.ts) files under global/js
 */
function cleanTypescript() {
    return gulp.src([TS_CLEAN_DTS, TS_CLEAN_OUT_JS])
        .pipe(clean())
        .on('error', gutil.log);
}

/**
 * Lints and transpiles *.scss files to *.js files, storing them under compiled/global/js with relative paths below
 * the ts parent directory.
 */
function buildSass() {
    return gulp.src(SASS_SRC)
        .pipe(scsslint({
            'config': '.scss-lint.yml',             // config file
            'verbose': true
        }))
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))    // Compile scss files and their sourcemaps, printing errors
        .pipe(sourcemaps.write())
        .pipe(flatten({subPath: [1]}))              // Remove 'ts' parent directory by slicing parent directories
        .pipe(gulp.dest(SASS_OUT))
        .on('error', gutil.log);                    // Pretty logging
}

/**
 * Copies all library *.d.ts files like jquery.d.ts to the compiled/global/js directory.
 */
function buildDefinitions() {
    return gulp.src(TS_SRC_DTS)
        .pipe(gulp.dest(TS_OUT))
        .on('error', gutil.log);
}

/**
 * Lints and builds all *.ts and *.d.ts files and stores them under compiled/global/js.
 */
function buildTypescript() {
    var tsResult = gulp.src(TS_SRC)
        .pipe(tslint())
        .pipe(tslint.report("verbose"))
        .pipe(sourcemaps.init())
        .pipe(typescript({
            declaration: true,
            noExternalResolve: true,
            target: 'ES5'
        }));

    // Need to merge the dts and js streams since typescript does not yield a single stream.
    return merge([
        tsResult.dts.pipe(flatten({subPath: [1]})).pipe(gulp.dest(TS_OUT)).on('error', gutil.log),
        tsResult.js.pipe(flatten({subPath: [1]})).pipe(sourcemaps.write()).pipe(gulp.dest(TS_OUT)).on('error', gutil.log)
    ]);
}

// Cleaning and Building can be run in parallel, but rebuilding requires cleaning be done before building
var cleanFn = gulp.parallel(cleanSass, cleanTypescript);
var buildFn = gulp.parallel(buildSass, buildTypescript, buildDefinitions);
var rebuildFn = gulp.series(cleanFn, buildFn);


// Task Definitions
gulp.task('buildSass', buildSass);

gulp.task('clean', cleanFn);
gulp.task('build', buildFn);
gulp.task('rebuild', rebuildFn);
gulp.task('default', rebuildFn);
