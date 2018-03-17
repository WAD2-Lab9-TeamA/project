/**
  * JavaScript main file
  *
  * Author: Luca Vizzarro <2252593v@student.gla.ac.uk>
  * Dev Team: WAD2 Lab 9 Team A
  */

// JS frameworks
window.Popper = require('popper.js').default;
try {
    window.$ = window.jQuery = require('jquery');
    require('bootstrap');
} catch (e) {}

// SCSS import
import '../sass/index.scss';

// Fonts import

import fontawesome from '@fortawesome/fontawesome';
import { faHome, faUser } from '@fortawesome/fontawesome-free-solid';
fontawesome.library.add(faHome, faUser);

$(() => {
  // Logo loading
  $("#logo").attr('src', require('../images/logo.svg'));

  // Geolocation check
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((pos) => {
      if(process.env.NODE_ENV == "development")
        console.info("Position detected", pos);

      $("body").addClass("geolocation-enabled");
    }, () => {
      if(process.env.NODE_ENV == "development")
        console.warn('Geolocation not working on this device.')

      $(".geolocation").remove();
    });
  } else {
    if(process.env.NODE_ENV == "development")
      console.warn('Geolocation not supported or disabled on this device.');

    $(".geolocation").remove();
  }

  $("#offpage-nav-toggle").click(() => {
    $("body").addClass("offpage-nav-visible");
  });

  $("#overlay").click(() => {
    $("body").removeClass("offpage-nav-visible");
  });
});

$(window).on('load', (e) => {
  setTimeout(() => $("body").removeClass("loading"), 200);
});
