

function getLoadFactor(load_case, load_type) {
  url = '/' + load_case + '/' + load_type + '/load-factor'
  fetch(url)
  .then(function(response) {
    response.json().then(function(data) {
      $("#load_factor").val(data);
    });
  });
};


function getLoadLocation(load_distribution, struct_type, span_length) {
  url = '/' + load_distribution + '/' + struct_type + '/' + span_length + '/load-location'
  fetch(url)
  .then(function(response) {
    response.json().then(function(data) {
      $("#load_location").val(data);
    });
  });
};


function formatHTML(beam_data) {

  if (beam_data.reaction.length == 1) {
    var reaction = "R1: " + beam_data.reaction[0].toFixed(2) + " kips";
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

  $("#load_location_div").hide();

  $("#load_distribution").change(function() {
    let load_distribution = $("#load_distribution").val();
    let struct_type = $("#struct_type").val();
    let span_length = $("#span_length").val();
    if (load_distribution == 'point') {
      let a = getLoadLocation(load_distribution, struct_type, span_length);
      $("load_location").val(a);
      $("#load_location_div").show();
    } else {
      $("#load_location_div").hide();
    }
  });

  $("#struct_type").change(function() {
    let load_distribution = $("#load_distribution").val();
    let struct_type = $("#struct_type").val();
    let span_length = $("#span_length").val();
    if (load_distribution == 'point') {
      let a = getLoadLocation(load_distribution, struct_type, span_length);
      $("load_location").val(a);
    }
  });

  $("#span_length").keyup(function() {
    let load_distribution = $("#load_distribution").val();
    let struct_type = $("#struct_type").val();
    let span_length = $("#span_length").val();
    if (load_distribution == 'point') {
      let a = getLoadLocation(load_distribution, struct_type, span_length);
      $("load_location").val(a);
    }
  });

  $("#load_case").change(function() {
    let load_case = $("#load_case").val();
    let load_type = $("#load_type").val();
    getLoadFactor(load_case, load_type);
  });

  $("#load_type").change(function() {
    let load_case = $("#load_case").val();
    let load_type = $("#load_type").val();
    getLoadFactor(load_case, load_type);
  });

  $("form").submit(function(e) {
    e.preventDefault();
    processForm();
  });

});
