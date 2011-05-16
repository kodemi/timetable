$(document).ready(function() {

    function addZero(i) {
        return (i < 10)? "0" + i: i;
    }

    //var flight_date = new Date(2011, 3, 4);
    var flight_datepicker = $("#flight_date").datepicker();
    flight_datepicker.datepicker("setDate", "+0");
    var flight_date = flight_datepicker.datepicker("getDate");
    var dep_arr_templ = _.template("<b class='time'><% print((function(){" +
            "if (flight_type){ return '--' };" +
            "var t;" +
            "if (status == 'приземлился'){" +
            "   t = time.actual" +
            "} else {" +
            "   t = time.estimated" +
            "};" +
            "var d = new Date(t+' GMT+0000');" +
            "hours = d.getUTCHours();" +
            "minutes = d.getUTCMinutes();" +
            "timeStr= '' + hours;" +
            "timeStr+= ((minutes < 10) ? ':0' : ':') + minutes;" +
            "return timeStr;" +
            "})()); %></b><br/><%= city %><br/><% print((function(){" +
            "if (!airport){" +
            "   airport = city" +
            "};" +
            "return '(' + airport + (!flight_type ? (' ' + terminal) : '') + ')' " +
            "})()); %>");

    var status_templ = _.template("<%= status %>");
    // _.template("<span class='<% print((function(){" +
            //"if (status == 'приземлился'){" +
            //"   return 'status4'" +
            //"}" +
            //"})()); %>'><%= status %></span>");

    $("#show_timetable").live('click', function(){
        var flight, flight_from, flight_to, flight_filter;
        var flight_date = flight_datepicker.datepicker("getDate");
        var flight_input = $("#flight")[0];
        var flight_from_input = $("#flight_from")[0];
        var flight_to_input = $("#flight_to")[0];
        if (flight_input.value == flight_input.defaultValue){
            flight = "flights"
        } else {
            flight = flight_input.value
        }
        if (flight_from_input.value == flight_from_input.defaultValue){
            flight_from = "all"
        } else {
            flight_from = flight_from_input.value
        }
        if (flight_to_input.value == flight_to_input.defaultValue){
            flight_to = "all"
        } else {
            flight_to = flight_to_input.value
        }
        flight_filter = flight_from + "_" + flight_to + "/" + flight;
        dataTable.fnReloadAjax("/api/" + addZero(flight_date.getMonth() + 1) + "/" + addZero(flight_date.getDate()) + "/" + flight_filter)
    });
    var dep_arr_templ_func = function(oObj, flight_type){
        return dep_arr_templ({
            time: {
                'estimated': oObj.aData["datetime_estimated"],
                'actual': oObj.aData["datetime_actual"]
            },
            status: oObj.aData["flight_status"],
            flight_type: !(flight_type ^ oObj.aData["flight_type"]),

            city: flight_type?oObj.aData["city_of_departure"]:oObj.aData["city_of_arrival"],
            airport: flight_type?oObj.aData["airport_of_departure"]:oObj.aData["airport_of_arrival"],
            terminal: oObj.aData["terminal"]
        })
    };
    var status_templ_func = function(oObj){
        return status_templ({
            status: oObj.aData["flight_status"]
        })
    };
    var dataTable = $('#timetable').dataTable( {
        "bProcessing": true,
        //"bPaginate": true,
        "sScrollY": "350px",
        //"iDisplayLength": 5,
        "bLengthChange": false,
        //"sPaginationType": "full_numbers",
        //"bScrollCollapse": true,
        "bAutoWidth": false,
        //"asStripClasses": ["artica", "center"],
        "bSort": false,
        "bFilter": false,
        "bInfo": false,
		"sAjaxSource": null,
        "sAjaxDataProp": "",
        "aoColumns": [
            { "mDataProp": "flight", "sWidth": "6%" }, // номер рейса
            { "mDataProp": "airline" }, // авиакомпания
            { "fnRender": function(oObj){ return dep_arr_templ_func(oObj, 1) }, "sWidth": "30%"}, // вылет
            { "fnRender": function(oObj){ return dep_arr_templ_func(oObj, 0) }, "sWidth": "30%"}, // прилет
            { "fnRender": function(oObj){ return  status_templ_func(oObj) }, "sWidth": "10%"}, // статус
            { "mDataProp": "flight_type", "sWidth": "5%" } // смс
        ],
        "aoColumnDefs": [{
            "sClass": "center artica",
            "aTargets": ["_all"]
        }],
        "oLanguage": {
			"sEmptyTable": "Рейсы не найдены",
            "sProcessing": "Производится поиск..."
		}
	} );
} );