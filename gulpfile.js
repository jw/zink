// Trimmed down from canvas/gulpfile.js: only the SCSS build for our
// vendored copy of the Canvas template's stylesheet (core/static/scss/).
// Canvas's demo/image/JS tasks are dropped since we don't vendor those.

const gulp = require("gulp");
const sass = require("gulp-sass")(require("sass"));
const rtlcss = require("gulp-rtlcss");
const concat = require("gulp-concat");
const cleanCSS = require("gulp-clean-css");
const autoprefixer = require("autoprefixer");
const postcss = require("gulp-postcss");
const plumber = require("gulp-plumber");
const rename = require("gulp-rename");
const { series } = require("gulp");

const silencedSassDeprecations = [
  "color-functions",
  "global-builtin",
  "import",
  "if-function",
  "abs-percent",
];

const scssSrc = "./core/static/scss/style.scss";
const cssDest = "./core/static/css";

function compileSCSS() {
  return gulp
    .src(scssSrc, { sourcemaps: true })
    .pipe(plumber())
    .pipe(sass({ silenceDeprecations: silencedSassDeprecations }).on("error", sass.logError))
    .pipe(concat("style.css"))
    .pipe(postcss([autoprefixer()]))
    .pipe(gulp.dest(cssDest, { sourcemaps: "." }));
}

function convertRTL() {
  return gulp
    .src(`${cssDest}/style.css`)
    .pipe(plumber())
    .pipe(rtlcss())
    .pipe(concat("style-rtl.css"))
    .pipe(gulp.dest(cssDest));
}

function cssminify() {
  return gulp
    .src(`${cssDest}/style.css`)
    .pipe(plumber())
    .pipe(cleanCSS())
    .pipe(rename({ suffix: ".min" }))
    .pipe(gulp.dest(cssDest));
}

function watch() {
  gulp.watch("./core/static/scss/**/*.scss", series(compileSCSS, convertRTL));
}

exports.scsscompile = series(compileSCSS, convertRTL);
exports.cssminify = cssminify;
exports.watch = watch;
exports.default = exports.scsscompile;
