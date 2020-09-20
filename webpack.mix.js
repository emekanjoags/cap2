const mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 */

mix.js('resources/js/main.js', 'static/js')
    .sass('resources/scss/make-donation.scss', 'static/css/core')
