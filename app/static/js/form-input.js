
function getRadioVal(name) {
  let tagString = 'input[name=' + name + ']:checked';
  return $(tagString).val();
}

function updateModelImage() {
  let img_src = "/static/img/beam_diagrams/" + $("#struct_type").val() +
    "_" + $("#load_distribution").val() + ".png";
  $("#model-img").attr("src", img_src);
};


function getPointLocation() {
  return new Promise((resolve, reject) => {
    var point_data = {
      load_distribution: $("#load_distribution").val(),
      struct_type: $("#struct_type").val(),
      span_length: $("#span_length").val()
    };

    $.ajax({
        url: '/point-location',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(point_data),
        success: function (response) {
            resolve(response);
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });

  });
}


function getLoadFactor() {
  return new Promise((resolve, reject) => {
    var factor_type = getRadioVal("factor_type")
    var load_case = $("#load_case").val();
    var load_type = $("#load_type").val();
    $.getJSON('/load-factors')
    .done( function(data) {
      var load_factor = data[factor_type][load_case][load_type];
      resolve(load_factor);
    });
  });
}


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
    data: $("form").serialize(),
    success: function(data) {
      formatHTML(data.output);
    }
  });
}


$(document).ready(function() {

  $("#load_location_span").hide();

  $("#load_distribution").change(async function() {
    updateModelImage();
    if ($("#load_distribution").val() == "point") {
      const load_location = await getPointLocation();
      $("#load_location").val(load_location);
      $("#load_location_span").show();
      $("#load_units_span").text("k");
      $("#load_label").text("P: ");
      processForm();
    } else {
      $("#load_units_span").text("k/ft");
      $("#load_location_span").hide();
      if ($("#load_distribution").val() == "triangular") {
        $("#load_label").text("q: ");
      } else {
        $("#load_label").text("w: ");
      }
    }
    processForm();
  });

  $("#struct_type").change(async function() {
    updateModelImage();

    if ($("#load_distribution").val() == "point") {
      // getLoadLocation();
      const load_location = await getPointLocation();
      $("#load_location").val(load_location);

    }

    processForm();
  });

  $("#span_length").keyup(function() {
    if ($("#load_distribution").val() == 'point') {
      getPointLocation();
    }
  });

  $(".load-factor").change(async function() {
    let factor_type = getRadioVal("factor_type")
    const load_factor = await getLoadFactor();
    $("#load_factor").val(load_factor);
    processForm();
  });

  $("input[type=radio]").change(async function() {
    const load_factor = await getLoadFactor();
    $("#load_factor").val(load_factor);
    processForm();
  });

  $("input").keyup(function() {
    processForm();
  });


  // $("form").submit(function(e) {
  //   e.preventDefault();
  //   processForm();
  // });

});
