function chart(id,type,data) {

    c3.generate({
            bindto: '#'+id,
            size:{
                width:500,
                height:300
            },
        data: {
         columns:data,
            type : type,
            onclick: function (d, i) {  },
            onmouseover: function (d, i) {  },
            onmouseout: function (d, i) {  },
             empty: {
            label:{
                text: "No Data Available"
            }
        },},

        legend: {
            show: true
        },
        bar: {
            width: {
                ratio: 0.3 // this makes bar width 50% of length between ticks
            },
            space:0.2,
            axis: {
                rotated: true,
            }
        }
    });


}