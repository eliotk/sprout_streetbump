$(document).ready(function() {
	var markersArray = [];
	
	/* js logic for map interactions and functionality */
	var latlng = new google.maps.LatLng(42.3583333, -71.0602778);
	
	// set start up options
	var myOptions = {
		zoom: 8,
		center: latlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	
	// target map_canvas div
	var map = new google.maps.Map(document.getElementById("map_canvas"),myOptions);

	// add georsslayer of known locations
	var georssLayer = new google.maps.KmlLayer('http://www.assembla.com/code/sprout-sb/subversion/node/blob/jsvis/known-points.kml');
	georssLayer.setMap(map);
	
	// georsslayer for rutherford known locations
	var georssLayer = new google.maps.KmlLayer('http://maps.google.com/maps/ms?ie=UTF8&authuser=0&msa=0&output=nl&msid=211515299457112956568.0004a8e62e763e3f5342c');
	georssLayer.setMap(map);
	
	/*  ajax track upload handling so that we can ulpoad new track without reloading page */
	var options = { 
        // target:        '#div_to_update',   // target element(s) to be updated with server response 
        // beforeSubmit:  ,  // pre-submit callback 
        success:       postResponse  // post-submit callback 
 
        // other available options: 
        //url:       url         // override for form's 'action' attribute 
        //type:      type        // 'get' or 'post', override for form's 'method' attribute 
        //dataType:  null        // 'xml', 'script', or 'json' (expected server response type) 
        //clearForm: true        // clear all form fields after successful submit 
        //resetForm: true        // reset the form after successful submit 
 
        // $.ajax options can be used here too, for example: 
        //timeout:   3000 
    }; 

	function postResponse(responseText) {
		$('#current_track').html(responseText);
		add_filtered_markers(responseText,$('#z_accel_threshold_value').val());
	}
 
    // bind form using 'ajaxForm' 
    $('#track_upload').ajaxForm(options);

	// retrieve json filtered points
	function add_filtered_markers( map_name, zaccel_threshold_value ) {
	 	// check to see if we are working w a file yet
		if( $('#current_track').html() == '') {
			alert('You need to upload a track first.');
			return false;
		}	
		if(map_name == null) {
			map_name = $('#current_track').html()
		}
		
		
		
		// get zaccel threshold value
		zaccel_threshold_value = $('#z_accel_threshold_value').val()
		
		// get z_x_ratio threshold
		z_x_ratio_threshold = $('#z_x_ratio_threshold').val()
		
		// get min speed threshold value
		min_speed_threshold_value = $('#min_speed_threshold_value').val()
		
		// get z vs speed thresh value
		z_vs_speed_threshold_value = $('#z_vs_speed_threshold_value').val()
		
		
		$.getJSON("filter", {	
								z_accel_enabled:$('#z_accel_enabled').attr('checked'),
								z_x_ratio_enabled:$('#z_x_ratio_enabled').attr('checked'),
								min_speed_enabled:$('#min_speed_enabled').attr('checked'),
								z_vs_speed_enabled:$('#z_vs_speed_enabled').attr('checked'),
								csv_file_name:map_name, 
								threshold:zaccel_threshold_value, 
								z_x_ratio_threshold:z_x_ratio_threshold,
								min_speed_threshold_value:min_speed_threshold_value,
								z_vs_speed_threshold_value:z_vs_speed_threshold_value
			}, function(json) {
			$.each(json.pothole, function(i,item){
				// now lets mark em on map
				placeMarker( item.latitude,item.longitude, item.severity );
			});
		});
	}
	
	// place marker function
	function placeMarker(lat, longitude,severity) {
		var latLong = new google.maps.LatLng(lat, longitude);
        var marker = new google.maps.Marker({
            position: latLong,
            map: map,
			title: 'Severity: '+severity
        });
    	
		map.setCenter(latLong);
		map.setZoom(14);
		
		markersArray.push(marker);
		
		var infowindow = new google.maps.InfoWindow({
		    content: 'Severity: '+severity
		});
		
		google.maps.event.addListener(marker, 'click', function() {
		  infowindow.open(map,marker);
		});
		
		
    }
	
	function clearMarkers() {
        if (markersArray) {
            for (i in markersArray) {
                markersArray[i].setMap(null);
            }
            markersArray.length = 0;
        }
    }
	
	// generate slider
	slider_options = { min:1, max:4, step:.01, value:$('#z_accel_threshold_value').val() }
	$( "#slider" ).slider( slider_options );

	// generate z_x_slider
	slider_options = { min:0, max:30, step:.01, value:$('#z_x_ratio_threshold').val()  }
	$( "#z_x_slider" ).slider( slider_options );
	
	// gen min speed slider
	slider_options = { min:0, max:50, step:1, value:$('#min_speed_threshold_value').val()  }
	$( "#min_speed_slider" ).slider( slider_options );
	
	// gen z vs speed slider
	slider_options = { min:0, max:5, step:.01, value:$('#z_vs_speed_threshold_value').val() }
	$( "#z_vs_speed_slider" ).slider( slider_options );
	
	// zAccel threshold callback for slide change
	$( "#slider" ).slider({
	   change: function(event, ui) { 
			clearMarkers();
			add_filtered_markers(null, ui.value);
			$('#z_accel_threshold_value').val(ui.value);
		 }
	});
	
	// z/x for slide change
	$( "#z_x_slider" ).slider({
	   change: function(event, ui) { 
			clearMarkers();
			add_filtered_markers(null);
			$('#z_x_ratio_threshold').val(ui.value);
		 }
	});
	
	// min speed slide change
	$( "#min_speed_slider" ).slider({
	   change: function(event, ui) { 
			clearMarkers();
			add_filtered_markers(null);
			$('#min_speed_threshold_value').val(ui.value);
		 }
	});
	
	// z vs speed slide change
	$( "#z_vs_speed_slider" ).slider({
	   change: function(event, ui) { 
			clearMarkers();
			add_filtered_markers(null);
			$('#z_vs_speed_threshold_value').val(ui.value);
		 }
	});
	
	// if any checkboxes toggled, run add_filtered_markers
	$(':checkbox').change(function() {
		clearMarkers();
		add_filtered_markers(null);
	});
});