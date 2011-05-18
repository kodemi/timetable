$(document).ready(function() {

    function addZero(i) {
        return (i < 10)? "0" + i: i;
    }

    //var flight_date = new Date(2011, 3, 4);
    var flight_datepicker = $("#flight_date").datepicker();
    flight_datepicker.datepicker("setDate", "+0");
    var flight_date = flight_datepicker.datepicker("getDate");
    var dep_arr_templ = _.template("<b class='time'><% print((function(){" +
            "if (!flight_type){ return '--' };" +
            "var t;" +
            "if (time.actual){" +
            "   t = time.actual" +
            "} else {" +
            "   t = time.estimated ? time.estimated : time.scheduled" +
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
            "console.log(airport + flight_type);" +
            "return '(' + airport + (flight_type ? (' ' + terminal) : '') + ')' " +
            "})()); %>");

    var status_templ = _.template("<span class='<% print((function(){" +
            "if (status == 'прилетел'){" +
            "   return 'status4'" +
            "} else if (status == 'не вылетел' || status == 'отменен'){" +
            "   return 'status2'" +
            "} else if (status == 'задержан'){" +
            "   return 'status3'" +
            "} else {" +
            "   return 'status1'" +
            "}" +
            "})()); %>'><%= status %></span>");

    var datetime_templ = _.template("<% print((function(){" +
            "if (actual){ return actual + ' GMT+0000'};" +
            "if (estimated){ return estimated + ' GMT+0000'};" +
            "return scheduled + ' GMT+0000'" +
            "})()); %>");
    var sms_templ = _.template('<a href=""><img border="0" src="static/images/smsicon.jpg"/></a>');

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
                'scheduled': oObj.aData["datetime_scheduled"],
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

    var datetime_templ_func = function(oObj){
        return datetime_templ({
            scheduled: oObj.aData["datetime_scheduled"],
            estimated: oObj.aData["datetime_estimated"],
            actual: oObj.aData["datetime_actual"]
        })
    };

    var dataTable = $('#timetable').dataTable( {
        "bProcessing": true,
        "bPaginate": true,
        //"sScrollY": "350px",
        "iDisplayLength": 6,
        "bLengthChange": false,
        "sPaginationType": "full_numbers",
        //"bScrollCollapse": true,
        "bAutoWidth": false,
        //"asStripClasses": ["artica", "center"],
        "bSort": true,
        "bFilter": false,
        "bInfo": false,
		"sAjaxSource": null,
        "sAjaxDataProp": "",
        "aaSorting": [[6,"asc"]],
        "bSortClasses": false,
        "aoColumns": [
            { "mDataProp": "flight", "sWidth": "6%", "bSortable": false }, // номер рейса
            { "mDataProp": "airline", "bSortable": false }, // авиакомпания
            { "fnRender": function(oObj){ return dep_arr_templ_func(oObj, 1) }, "sWidth": "30%", "bSortable": false}, // вылет
            { "fnRender": function(oObj){ return dep_arr_templ_func(oObj, 0) }, "sWidth": "30%", "bSortable": false}, // прилет
            { "fnRender": function(oObj){ return  status_templ_func(oObj) }, "sWidth": "10%", "bSortable": false}, // статус
            { "fnRender": function(oObj){ return sms_templ() }, "sWidth": "5%", "bSortable": false }, // смс
            { "fnRender": function(oObj){ return datetime_templ_func(oObj) }, bVisible: false, sType: "date" }
        ],
        "aoColumnDefs": [{
            "sClass": "center artica",
            "aTargets": ["_all"]
        }],
        "oLanguage": {
			"sEmptyTable": "Рейсы не найдены",
            "sProcessing": "Производится поиск...",
            "oPaginate": {
                "sFirst": "Первые",
                "sLast": "Последние",
                "sNext": "Следующие",
                "sPrevious": "Предыдущие"
            }
		}
	} );
} );