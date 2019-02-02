
    $(document).ready(function(){

        let getChallan = function(data){
            let html = '';
            _.forEach(data.results,function(object){
               html += "<li  class='show-challan-modal'>"+
                    "<a data-id="+object.id+">"+object.name+"</a></li>";

            });
            $('#_challan_list').empty();
            $('#_challan_list').append(html);
        };
        ajaxCall('challan','GET','JSON',getChallan);


        $(document).on('click','.show-challan-modal',function(event){

            let getChallanColummns = function(data){
                $('#_form-title').empty();
                $('#_form-title').html(challan_name);
                let html = '';
                _.forEach(data.results,function(object){
                    if(object.type==="text"){
                      html +=   "<div class='form-group'>"+
                                    "<label class='control-label col-sm-3' >"+object.column+"</label>"+
                                    "<div class='col-sm-6'>"+
                                        "<input type='text' class='form-control form-class'>"+
                                    "</div>"+
                                "</div>";
                    }
                    if(object.type==="textarea"){
                      html +=   "<div class='form-group'>"+
                                    "<label class='control-label col-sm-3' >"+object.column+"</label>"+
                                    "<div class='col-sm-6'>"+
                                        "<textarea class='form-control form-class' rows='5' ></textarea>"+
                                    "</div>"+
                                "</div>";
                    }
                });
                html += "<div class='form-group'>"+
                            "<div class='col-sm-offset-3 col-sm-10'>"+
                                "<button type='button' id='_submit-form' class='btn btn-primary'>Submit</button>"+
                            "</div>"+
                        "</div>";
                $('#_form-body').empty();
                $('#_form-body').html(html);

                $('#_modal').modal('toggle');
            };

          let event_data =  $(this);
          let challlan_id = event_data.find('a').attr('data-id');
          let challan_name = event_data.find('a').html();
          ajaxCall('challan-columns/?challan_id='+challlan_id, 'GET','JSON',getChallanColummns);

        });
    });
