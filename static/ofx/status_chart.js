        /*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

var yValues = [];
        let client_id = 0;
        let project_id = 0;

        function get_status_data(client_id, project_id) {
            if (project_id > 0) {
                api_url = "/api/production/status_count/?project_id=" + [project_id]
            } else if (client_id > 0) {
                api_url = "/api/production/status_count/?client_id=" + [client_id]
            } else {
                api_url = "/api/production/status_count/"
            }
            const all_status_json = $.ajax({
                type: "GET",
                url: api_url,
                dataType: "application/json",
                async: false,
                error: function (xhr, status, err) {
                },
            }).responseText;
            const all_status = JSON.parse(all_status_json);
            return all_status
        }

        var xValues = ["YTS", "WIP", "OMIT", "HOLD", "DELIVERED", "RETAKE"];

        var barColors = ["#055ff1", "#ef4305", "#05e7ef", "#ee09c8", "#05fd09", "#f20a0a"];

        var canvas = document.getElementById("statChart");
        var ctx = canvas.getContext('2d');
        var chartType = 'bar';
        var myBarChart;

        // Global Options:
        Chart.defaults.global.defaultFontColor = 'grey';
        Chart.defaults.global.defaultFontSize = 16;

        var data = {
            labels: xValues,
            datasets: [{
                fill: true,
                lineTension: 0.1,
                backgroundColor: barColors,
                borderCapStyle: 'square',
                pointBorderColor: "white",
                pointBackgroundColor: "green",
                pointBorderWidth: 1,
                pointHoverRadius: 8,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderColor: "green",
                pointHoverBorderWidth: 2,
                pointRadius: 4,
                pointHitRadius: 10,
                data: yValues,
                spanGaps: true,
            }]
        };

        var options = {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: {
                display: false
            }
        };

        init();

        function init() {
            all_status = get_status_data(0, 0)
            yValues.push(all_status.yts_count, all_status.wip_count, all_status.omit_count, all_status.hold_count, all_status.del_count, all_status.retake_count)
            // Chart declaration:
            myBarChart = new Chart(ctx, {
                type: chartType,
                data: data,
                options: options
            });
        }


        function update_chart(all_status){
            myBarChart.data.datasets[0].data[0] = all_status.yts_count;
            myBarChart.data.datasets[0].data[1] = all_status.wip_count;
            myBarChart.data.datasets[0].data[2] = all_status.omit_count;
            myBarChart.data.datasets[0].data[3] = all_status.hold_count;
            myBarChart.data.datasets[0].data[4] = all_status.del_count;
            myBarChart.data.datasets[0].data[5] = all_status.retake_count;
            myBarChart.update()
        }

        $('#shot_client_select').on('change', function () {
            const client = $('#shot_client_select option:selected').text().trim();
            client_id = $('#shot_client_select option:selected').val();
            if (client_id != 0) {
                const all_projects_json = $.ajax({
                    type: "GET",
                    url: "/api/production/projects/" + client_id + "/",
                    dataType: "application/json",
                    async: false,
                    error: function (xhr, status, err) {
                    },
                }).responseText;
                const all_projects = JSON.parse(all_projects_json);
                $('#shot_project_select').empty()
                $('#shot_project_select').append(`<option value="0">
                                               Project
                                          </option>`);
                all_projects.forEach(function (project) {
                    optionText = project['name'];
                    optionValue = project['id'];
                    $('#shot_project_select').append(`<option value="${optionValue}">
                                               ${optionText}
                                          </option>`);
                })
                all_status = get_status_data(client_id, 0)
                update_chart(all_status)
            } else {
                const all_projects_json = $.ajax({
                    type: "GET",
                    url: "/api/production/projects/",
                    dataType: "application/json",
                    async: false,
                    error: function (xhr, status, err) {
                    },
                }).responseText;
                const all_projects = JSON.parse(all_projects_json);
                $('#shot_project_select').empty()
                $('#shot_project_select').append(`<option value="0">
                                               Project
                                          </option>`);
                all_projects.forEach(function (project) {
                    optionText = project['name'];
                    optionValue = project['id'];
                    $('#shot_project_select').append(`<option value="${optionValue}">
                                               ${optionText}
                                          </option>`);
                })
                all_status = get_status_data(0, 0)
                update_chart(all_status)
            }
        });
        $('#shot_project_select').on('change', function () {
            const project = $("#shot_project_select :selected").text().trim();
            project_id = $('#shot_project_select option:selected').val();
            all_status = get_status_data(client_id, project_id)
            myBarChart.data.datasets[0].data[0] = all_status.yts_count;
            myBarChart.data.datasets[0].data[1] = all_status.wip_count;
            myBarChart.data.datasets[0].data[2] = all_status.omit_count;
            myBarChart.data.datasets[0].data[3] = all_status.hold_count;
            myBarChart.data.datasets[0].data[4] = all_status.del_count;
            myBarChart.data.datasets[0].data[5] = all_status.retake_count;
            myBarChart.update()
        });