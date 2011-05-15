$(document).bind("mobileinit", function(){
    $.mobile.page.prototype.options.backBtnText = "Назад";
    $.mobile.listview.prototype.options.filterPlaceholder = "Найти...";
});

$(function(){
    function switch_flights(target){
        if ( target === "radio-arrival" ){
            $(".Arrival").show();
            $(".Departure").hide();
        }
        else {
            $(".Arrival").hide();
            $(".Departure").show();
        }
    };

    $("input[name=radio-flight-type]").bind("change", function(ev){
        var target = ev.target.id;
        switch_flights(target);
    });

    Flight = Backbone.Model.extend();
    FlightList = Backbone.Collection.extend({
        model: Flight,
        url: '/api/flights.json'
    });

    Flights = new FlightList;

    FlightView = Backbone.View.extend({
        tagName: "li",
        template: _.template($('#item-template').html()),

        initialize: function(){
            _.bindAll(this, 'render');
            this.model.bind('change', this.render);
            this.model.view = this;
        },

        render: function(){
            $(this.el).html(this.template(this.model.toJSON()));
            var flight_type;
            if (this.model.get('flight_type')) flight_type = 'Departure';
            else flight_type = 'Arrival';
            $(this.el).attr({
                'role': 'option',
                'class': flight_type + ' ui-li ui-li-static ui-btn-up-d'
            });
            return this;
        }
    });

    FlightsView = Backbone.View.extend({
        el: $("#flights"),

        initialize: function(){
            _.bindAll(this, 'addOne', 'addAll');
            Flights.bind('add', this.addOne);
            Flights.bind('refresh', this.addAll);
            Flights.fetch();
        },

        addOne: function(flight){
            var view = new FlightView({model: flight});
            this.$("#flight-list").append(view.render().el);
        },

        addAll: function(){
            var onload_flight_type = $("input[name=radio-flight-type]:checked").attr('id');
            Flights.each(this.addOne);
            this.switchVis(onload_flight_type);
        },

        switchVis: function(target){
            if ( target === "radio-arrival" ){
                 $(".Arrival").show();
                $(".Departure").hide();
            }
            else {
                $(".Arrival").hide();
                $(".Departure").show();
            }
        }
    });
    flights = new FlightsView;
});

