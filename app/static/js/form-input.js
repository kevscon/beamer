
function updateModelImage() {
  let img_src = "/static/img/beam_diagrams/" + $("#struct_type").val() +
    "_" + $("#load_distribution").val() + ".png";
  $("#model-img").attr("src", img_src);
};


function getLoadLocation() {
  url = '/' + $("#load_distribution").val() + '/' + $("#struct_type").val() +
    '/' + $("#span_length").val() + '/load-location';
  fetch(url)
  .then(function(response) {
    response.json().then(function(data) {
      $("#load_location").val(data);
    });
  });
};


function getLoadFactor(factor_type) {
  url = '/' + $("#load_case").val() + '/' + $("#load_type").val() + '/' + factor_type + '/load-factor';
  fetch(url)
  .then(function(response) {
    response.json().then(function(data) {
      $("#load_factor").val(data);
    });
  });
};


function formatHTML(beam_data) {

  if (beam_data.reaction.length == 1) {
    var reaction = "R: " + beam_data.reaction[0].toFixed(2) + " kips";
    $("#reaction-1").html(reaction);
    $("#reaction-2").html("");
  } else {
    var reaction1 = "R1: " + beam_data.reaction[0].toFixed(2) + " kips";
    var reaction2 = "R2: " + beam_data.reaction[1].toFixed(2) + " kips";
    $("#reaction-1").html(reaction1);
    $("#reaction-2").html(reaction2);
  }

  var shear = "Max Shear: " + beam_data.shear.toFixed(2) + " kips";
  $("#shear").html(shear);

  if (beam_data.moment.length == 1) {
    var moment = "Max Moment: " + beam_data.moment[0].toFixed(2) + " k-ft";
    $("#moment-1").html(moment);
    $("#moment-2").html("");
  } else {
    var moment1 = "Moment 1: " + beam_data.moment[0].toFixed(2) + " k-ft";
    var moment2 = "Moment 2: " + beam_data.moment[1].toFixed(2) + " k-ft";
    $("#moment-1").html(moment1);
    $("#moment-2").html(moment2);
  }

  var deflection = "Max Deflection: " + beam_data.deflection.toFixed(4) + " inches";
  $("#deflection").html(deflection);

};


function processForm() {
  $.ajax({
    type : "POST",
    url : "/", // linked to routes.py page
    data: {
      struct_type : $("#struct_type").val(), // linked to html id
      span_length : $("#span_length").val(),
      load_distribution: $("#load_distribution").val(),
      load: $("#load").val(),
      load_location: $("#load_location").val(),
      E: $("#E").val(),
      I: $("#I").val(),
      load_case: $("#load_case").val(),
      load_type: $("#load_type").val(),
      load_factor: $("#load_factor").val()
    },
    success:function(data) {
      formatHTML(data.output);
    }
  });
};



$(document).ready(function() {

  $("#load_location_span").hide();

  $("#load_distribution").change(function() {
    updateModelImage();
    if ($("#load_distribution").val() == "point") {
      getLoadLocation();
      $("#load_location_span").show();
      $("#load_units_span").text("k");
      $("#load_label").text("P: ");
    } else {
      $("#load_units_span").text("k/ft");
      $("#load_location_span").hide();
      if ($("#load_distribution").val() == "triangular") {
        $("#load_label").text("q: ");
      } else {
        $("#load_label").text("w: ");
      }
    }
  });

  $("#struct_type").change(function() {
    updateModelImage();

    if ($("#load_distribution").val() == "point") {
      getLoadLocation();
    }
  });

  $("#span_length").keyup(function() {
    if ($("#load_distribution").val() == 'point') {
      getLoadLocation();
    }
  });

  $(".load-factor").change(function() {
    let factor_type = $('input[name="factor_type"]:checked').val();
    getLoadFactor(factor_type);
  });

  $("input[type=radio]").change(function() {
    let factor_type = $('input[name="factor_type"]:checked').val();
    getLoadFactor(factor_type);
  });

  $("form").submit(function(e) {
    e.preventDefault();
    processForm();
  });

});
