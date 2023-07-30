const gulp = require('gulp');
const sourcemap = require('gulp-sourcemaps');
const sass = require('gulp-sass')(require('sass'));
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');
const rename = require('gulp-rename');

gulp.task('sass', () => {
  return gulp
    .src('./scss/styles.scss') // SCSS to be compiled to CSS
    .pipe(sourcemap.init())
    .pipe(sass().on('error', sass.logError)) // compile to CSS
    .pipe(postcss([autoprefixer(), cssnano()])) // use autoprefixing and minification
    .pipe(rename('styles.min.css')) // rename to indicate minification and CSS format
    .pipe(sourcemap.write("."))
    .pipe(gulp.dest('./marie_site/static')); // output resulting CSS to project static dir
});

gulp.task('watch', () => {
  gulp.watch('./scss/**/*.scss', gulp.series('sass')); // watch for changes
});

gulp.task('default', gulp.series('sass', 'watch')); // run the above 2 tasks
