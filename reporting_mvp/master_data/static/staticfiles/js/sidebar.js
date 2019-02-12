
    $(document).ready(function(){
        let getChallan = function(data){
            let html = '';
            let htmlData = '';
            _.forEach(data.results,function(object){
               html += "<li  class='show-challan-modal'>"+
                    "<a data-id="+object.id+">"+object.name+"</a></li>";
               htmlData += '<li  class="show-challan-data">'+
                    '<a  href="http://localhost:8000/data/?challan_id='+object.id+'" data-id='+object.id+'>'+object.name+'</a></li>';
            });
            $('#_challan_list').empty();
            $('#_challan_list').append(html);

            $('#_challan_data_list').empty();
            $('#_challan_data_list').append(htmlData);
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
                                        "<input type='text' name="+object.column+"  class='form-control form-class' required>"+
                                    "</div>"+
                                "</div>";
                    }
                    if(object.type==="textarea"){
                      html +=   "<div class='form-group'>"+
                                    "<label class='control-label col-sm-3' >"+object.column+"</label>"+
                                    "<div class='col-sm-6'>"+
                                        "<textarea class='form-control form-class' name="+object.column+" rows='5' required></textarea>"+
                                    "</div>"+
                                "</div>";
                    }
                    if(object.type==="number"){
                      html +=   "<div class='form-group'>"+
                                    "<label class='control-label col-sm-3' >"+object.column+"</label>"+
                                    "<div class='col-sm-6'>"+
                                        "<input type='number' name="+object.column+"  class='form-control form-class' required>"+
                                    "</div>"+
                                "</div>";
                    }
                });
                html += "<div class='form-group'>"+
                            "<div class='col-sm-offset-3 col-sm-10'>"+
                                "<button type='submit' data-challan="+challlan_id+" id='' class='btn btn-primary _submit-form'>Submit</button>"+
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



        $("#_form-body").submit(function(e) {

            let form = $(this).serialize();
            let form_json = {};
            let form_data = form.split('&');
            for(let i=0; i< form_data.length;i++){
                let keyValue = form_data[i].split('=');
                form_json[keyValue[0]] = keyValue[1].split('%20').join(' ');
            }
            let challan_id = $('._submit-form').parent().find('button').attr('data-challan');
            let dashboard = function(data){
                if(data) {
                    $('#_success-message').removeClass('hidden');
                    setTimeout(function () {
                        $('#_success-message').addClass('hidden');
                                        $('#_modal').modal('hide');

                    }, 2000);
                }
            };
            ajaxCallPost('challan-data/',
                        'POST',
                        'JSON',
                        JSON.stringify({challan_type_id:challan_id,data:form_json}),
                        dashboard
                    );
             e.preventDefault();
    });


    });
