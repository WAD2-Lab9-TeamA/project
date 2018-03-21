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

import '@fortawesome/fontawesome';
import '@fortawesome/fontawesome-free-solid';
import '@fortawesome/fontawesome-free-brands';

// Images import
const LOGO_IMAGE = require('../images/logo.svg');
const PROFILE_PICTURE_IMAGE = require('../images/profile.svg');

$(() => {
  // Logo loading
  $("#logo").attr('src', LOGO_IMAGE);
  $(".profile_picture").attr('src', PROFILE_PICTURE_IMAGE);

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

  // Mobile side nav toggle
  $("#offpage-nav-toggle").click(() => {
    $("body").addClass("offpage-nav-visible");
  });

  $("#overlay").click(() => {
    $("body").removeClass("offpage-nav-visible");
  });

  window.submitPageForm = () => $('#page-form').submit();

  $(".picture-update").click(function() {
    if(!$(this).hasClass("fixed-overlay"))
      $("#picture-field").click();
  });

  var popPageAlert = message => {
    return () => {
      $("#page-alert")
        .html(message)
        .slideDown()
        .delay(3000)
        .slideUp();
    }
  }

  const ERASER_ICON_GRAPHIC = `<g class="icon" transform="matrix(0.11038793,0,0,0.11038793,89.336974,187.39878)">
  <path d="M 60.197,418.646 H 27.571 c -6.978,0 -12.634,5.657 -12.634,12.634 0,6.977 5.656,12.634 12.634,12.634 h 32.627 c 6.978,0 12.634,-5.657 12.634,-12.634 -10e-4,-6.976 -5.658,-12.634 -12.635,-12.634 z" />
  <path d="m 114.205,467.363 c -4.934,-4.932 -12.933,-4.934 -17.867,0 l -23.07,23.07 c -4.934,4.934 -4.935,12.933 0,17.868 2.467,2.466 5.7,3.701 8.933,3.701 3.233,0 6.467,-1.234 8.933,-3.701 l 23.07,-23.07 c 4.935,-4.934 4.936,-12.933 0.001,-17.868 z" />
  <path d="M 484.431,424.963 H 262.965 L 489.664,198.275 c 9.851,-9.852 9.852,-25.881 0.001,-35.733 L 334.522,7.388 c -9.853,-9.851 -25.882,-9.851 -35.735,0 l -247.99,247.99 c -14.318,14.318 -22.203,33.354 -22.203,53.602 0,20.247 7.885,39.284 22.203,53.602 l 74.701,74.699 c 8.351,8.351 19.455,12.951 31.266,12.951 H 484.43 c 6.978,0 12.634,-5.657 12.634,-12.634 10e-4,-6.977 -5.655,-12.635 -12.633,-12.635 z m -327.666,0 c -5.062,0 -9.82,-1.972 -13.401,-5.551 L 68.665,344.713 c -19.704,-19.704 -19.704,-51.765 0,-71.468 l 40.557,-40.557 133.335,133.336 c 2.467,2.466 5.7,3.7 8.933,3.7 3.233,0 6.467,-1.234 8.933,-3.7 4.934,-4.934 4.935,-12.933 10e-4,-17.868 L 127.09,214.821 316.655,25.254 471.797,180.409 227.23,424.963 Z" />
</g>`;
  const UPLOAD_ICON_GRAPHIC = `<g class="icon" transform="matrix(0.10944013,0,0,0.10944013,90.985971,189.04782)">
  <path d="M 395.5,135.8 C 390.3,104.9 375,76.7 351.6,55.3 c -26,-23.8 -59.8,-36.9 -95,-36.9 -27.2,0 -53.7,7.8 -76.4,22.5 -18.9,12.2 -34.6,28.7 -45.7,48.1 -4.8,-0.9 -9.8,-1.4 -14.8,-1.4 -42.5,0 -77.1,34.6 -77.1,77.1 0,5.5 0.6,10.8 1.6,16 -27.5,20 -44.2,52.2 -44.2,86.5 0,27.7 10.3,54.6 29.1,75.9 19.3,21.8 44.8,34.7 72,36.2 0.3,0 0.5,0 0.8,0 h 86 c 7.5,0 13.5,-6 13.5,-13.5 0,-7.5 -6,-13.5 -13.5,-13.5 H 102.3 C 61.4,349.8 27,310.9 27,267.1 c 0,-28.3 15.2,-54.7 39.7,-69 5.7,-3.3 8.1,-10.2 5.9,-16.4 -2,-5.4 -3,-11.1 -3,-17.2 0,-27.6 22.5,-50.1 50.1,-50.1 5.9,0 11.7,1 17.1,3 6.6,2.4 13.9,-0.6 16.9,-6.9 18.7,-39.7 59.1,-65.3 103,-65.3 59,0 107.7,44.2 113.3,102.8 0.6,6.1 5.2,11 11.2,12 44.5,7.6 78.1,48.7 78.1,95.6 0,49.7 -39.1,92.9 -87.3,96.6 h -73.7 c -7.5,0 -13.5,6 -13.5,13.5 0,7.5 6,13.5 13.5,13.5 h 74.2 c 0.3,0 0.6,0 1,0 30.5,-2.2 59,-16.2 80.2,-39.6 21.1,-23.2 32.6,-53 32.6,-84 -0.1,-56.1 -38.4,-106 -90.8,-119.8 z" />
  <path d="m 324.2,280 c 5.3,-5.3 5.3,-13.8 0,-19.1 l -71.5,-71.5 c -2.5,-2.5 -6,-4 -9.5,-4 -3.5,0 -7,1.4 -9.5,4 l -71.5,71.5 c -5.3,5.3 -5.3,13.8 0,19.1 2.6,2.6 6.1,4 9.5,4 3.4,0 6.9,-1.3 9.5,-4 l 48.5,-48.5 v 222.9 c 0,7.5 6,13.5 13.5,13.5 7.5,0 13.5,-6 13.5,-13.5 V 231.5 l 48.5,48.5 c 5.2,5.3 13.7,5.3 19,0 z" />
</g>`;

  const CIRCLE_SVG = `<svg width="50%" class="loading-circle" viewBox="0 0 112.5 112.5">
  <g transform="translate(-61.346339,-159.40819)">
    <path class="loader" d="m 117.59634,166.70824 a 48.950344,48.950344 0 0 1 0,97.90066 48.950344,48.950344 0 0 1 0,-97.90066" />
    %ICON%
  </g>
</svg>
`;

  var animateLoader = e => {
    if(e.lengthComputable)
      $(".loading-circle .loader")
        .animate({
          'stroke-dashoffset': `${307-e.loaded/e.total*307}`
        }, 600)
        .removeClass("indefinite");
    else
      $(".loading-circle .loader")
        .addClass("indefinite")
        .css("stroke-dashoffset", "");
  };

  $("#picture-field").change(function () {
    if(this.files && this.files.length > 0) {
      let image = new Image();

      image.onload = function () {
        let loading = $(".overlay div", $(".picture-update").addClass("fixed-overlay"));
        loading.attr("data-original", loading.text());
        loading.html(CIRCLE_SVG.replace('%ICON%', UPLOAD_ICON_GRAPHIC));

        $.ajax({
          url: '/my-account/update-picture/',
          data: new FormData($("#update-picture")[0]),
          type: 'POST',
          processData: false,
          contentType: false,
          cache: false,
          xhr: () => {
              let xhr = $.ajaxSettings.xhr();

              xhr.upload.onprogress = animateLoader;
              xhr.onprogress = animateLoader;

              return xhr;
          }
        }).done((response) => {
          $("#profile-picture").attr("src", this.src);
          $("#remove-picture").removeClass("d-none");
        }).fail(
          popPageAlert('An error occurred while uploading the image.')
        ).always(() => {
          $(".picture-update").removeClass("fixed-overlay");
          loading.html(loading.attr("data-original"));
        });
      }

      image.onerror = popPageAlert('The selected image is not valid.')
      image.src = URL.createObjectURL(this.files[0]);
    }
  });

  $("#remove-picture").click(function () {
    let loading = $(".overlay div", $(".picture-update").addClass("fixed-overlay"));
    loading.attr("data-original", loading.text());
    loading.html(CIRCLE_SVG.replace('%ICON%', ERASER_ICON_GRAPHIC));

    $.ajax('/my-account/remove-picture', {
      xhr: () => {
        let xhr = $.ajaxSettings.xhr();
        xhr.onprogress = animateLoader;
        return xhr;
      }
    }).done((response) => {
        $("#profile-picture").attr('src', PROFILE_PICTURE_IMAGE);
        $(this).addClass("d-none");
      }).fail(
        popPageAlert('An error occurred while removing your picture.')
      ).always(() => {
        $(".picture-update").removeClass("fixed-overlay");
        loading.html(loading.attr("data-original"));
      });
  })
});

$(window).on('load', (e) => {
  setTimeout(() => $("body").removeClass("loading"), 200);
});
