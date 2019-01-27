
    $(document).ready(function(){
        let workspace_id  = '';
        let integration_id = '';
        let status_response = function(data){
                    if (data.results[0].type=='workspaces') {
                        if (data.results[0].status == 'processing') {
                            $("#_workspace-sidebar-dropdown").empty();
                            $('#_workspace-sidebar-dropdown').append("<li>Sink in progres</li>");
                            setTimeout(function () {
                                checkStatus(data.results[0].job_id);
                            }, 2000);
                        }
                        else {
                            let workspaces = function (data) {
                                list_workspace(data.workspace)
                            };
                            ajaxCall('workspace/get-workspace/get-workspace',
                                'GET',
                                'JSON',
                                workspaces
                            );
                        }
                    }
                    if(data.results[0].type=='projects'){

                        if (data.results[0].status == 'processing') {
                            $("#_project-sidebar-dropdown").empty();
                            $('#_project-sidebar-dropdown').append("<li>Sink in progres</li>");
                            setTimeout(function () {
                                checkStatus(data.results[0].job_id);
                            }, 2000);
                        }
                        else {

                            ajaxCall('projects',
                                'GET',
                                'JSON',
                                list_projects
                            );
                        }
                    }
        };

        function list_projects(data) {
            let html = '';
                 _.forEach(data.results, function (object) {
                     html += "<li>" + object.name + " <span class='sink_project glyphicon glyphicon-refresh' data-integration_id="+object.integration_id+" data-id="+object.id+"></span></li>"
                 });
                 $("#_project-sidebar-dropdown").empty();
                 $('#_project-sidebar-dropdown').append(html);

        }

         ajaxCall('projects',
             'GET',
             'JSON',
             list_projects
         );

        function checkStatus(task_id) {
                    ajaxCall('job_status?task_id=' + task_id,
                        'GET',
                        'JSON',
                        status_response
                    );
        }

        function list_workspace(workspace) {
             let html = '';
                 _.forEach(workspace, function (object) {
                     html += "<li>" + object.name + " <span class='sink_workspace glyphicon glyphicon-refresh' data-integration_id="+object.integration_id+" data-id="+object.id+"></span></li>"
                 });
                 $("#_workspace-sidebar-dropdown").empty();
                 $('#_workspace-sidebar-dropdown').append(html);
         }

        let list_integrations = function (data){
            $('#_integration_modal_data').empty();
            let html = '';
           _.forEach(data.results,function (value) {
            value.oauthName = value.service_name
            if (value.service_name == "jira")
                value.oauthName = "atlassian"
                html += "<div class='row padding_bottom'>"+
                        "<div class='col-sm-6 col-sm-offset-2'>"+
                            "<div class='form-group'>"+
                                "<label class='text-capitalize'>"+value.service_name+"</label>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-4'>"+
                            "<a class='btn btn-info' href=/connect/login/"+value.oauthName+ "/?integration_id="+value.id+">Connect</a>"+
                        "</div>"+
                    "</div>";
           });
           $('#_integration_modal_data').append(html)
        };

        ajaxCall('list_integrations/',
                'GET',
                'JSON',
                list_integrations
        );

         let workspaces = function(data){
             if (data.task_id.length < 1 || data.task_id == undefined){
                    list_workspace(data.workspace)
             }
             else{
                checkStatus(data.task_id)
             }
        };
        ajaxCall('workspace/get-workspace/get-workspace',
                'GET',
                'JSON',
                workspaces
        );

        let sink_projects = function(data){
           checkStatus(data)

        };

        $(document).on("click",'.sink_workspace',function(event) {
            workspace_id = $(this).attr('data-id');
            integration_id = $(this).attr('data-integration_id');
            ajaxCall('projects/sink-projects/sink-projects?workspace_id='+$(this).attr('data-id')+"&&integration_id="+$(this).attr('data-integration_id'),
                'GET',
                'JSON',
                sink_projects
            );
        });

        let sink_project_data = function(data){

        };
        $(document).on("click",'.sink_project',function(event) {
            workspace_id = $(this).attr('data-id');
            integration_id = $(this).attr('data-integration_id');
            ajaxCall('projects/sink-project-data/sink-project-data?project_id='+$(this).attr('data-id')+"&&integration_id="+$(this).attr('data-integration_id'),
                'GET',
                'JSON',
                sink_project_data
            );
        })
    });
