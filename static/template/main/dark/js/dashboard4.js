/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

/*
Template Name: Monster Admin
Author: Themedesigner
Email: niravjoshi87@gmail.com
File: js
*/
$(function () {
    "use strict";
    // ============================================================== 
    // Total revenue chart
    // ============================================================== 
    new Chartist.Bar('.total-sales', {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept']
        , series: [
        [800000, 1200000, 1400000, 1300000, 1200000, 1400000, 1300000, 1300000, 1200000]
        , [200000, 400000, 500000, 300000, 400000, 500000, 300000, 300000, 400000]
        , [100000, 200000, 400000, 600000, 200000, 400000, 600000, 600000, 200000]
      ]
    }, {
        high: 2500000
        , low: 500000
        , fullWidth: true
        , plugins: [
        Chartist.plugins.tooltip()]
        , stackBars: true
        , axisX: {
            showGrid: false
        }
        , axisY: {
            labelInterpolationFnc: function (value) {
                return (value / 1000) + 'k';
            }
        }
    }).on('draw', function (data) {
        if (data.type === 'bar') {
            data.element.attr({
                style: 'stroke-width: 30px'
            });
        }
    });
    // ============================================================== 
    // sales difference
    // ==============================================================
    new Chartist.Pie('.ct-chart', {
        series: [25, 10]
    }, {
        donut: true
        , donutWidth: 20
        , startAngle: 0
        , showLabel: false
    });
    // ============================================================== 
    // world map
    // ==============================================================
    jQuery('#visitfromworld').vectorMap({
        map: 'world_mill_en'
        , backgroundColor: 'transparent'
        , borderColor: '#ccc'
        , borderOpacity: 0.9
        , borderWidth: 1
        , zoomOnScroll : false
        , color: '#ddd'
        , regionStyle: {
            initial: {
                fill: 'transparent'
            }
        }
        , markerStyle: {
            initial: {
                r: 8
                , 'fill': '#55ce63'
                , 'fill-opacity': 1
                , 'stroke': '#000'
                , 'stroke-width': 0
                , 'stroke-opacity': 1
            }
        , }
        , enableZoom: true
        , hoverColor: '#79e580'
        , markers: [{
            latLng: [21.00, 78.00]
            , name: 'India : 9347'
            , style: {fill: '#55ce63'}
        },
      {
        latLng : [-33.00, 151.00],
        name : 'Australia : 250'
        , style: {fill: '#02b0c3'}
      },
      {
        latLng : [36.77, -119.41],
        name : 'USA : 250'
        , style: {fill: '#11a0f8'}
      },
      {
        latLng : [55.37, -3.41],
        name : 'UK   : 250'
        , style: {fill: '#745af2'}
      },
      {
        latLng : [25.20, 55.27],
        name : 'UAE : 250'
        , style: {fill: '#ffbc34'}
      }]
        , hoverOpacity: null
        , normalizeFunction: 'linear'
        , scaleColors: ['#fff', '#ccc']
        , selectedColor: '#c9dfaf'
        , selectedRegions: []
        , showTooltip: true
        , onRegionClick: function (element, code, region) {
            var message = 'You clicked "' + region + '" which has the code: ' + code.toUpperCase();
            alert(message);
        }
    });
    $('#calendar').fullCalendar('option', 'height', 590);
    // ============================================================== 
    // sparkline chart
    // ==============================================================
    var sparklineLogin = function() { 
        $('#sparklinedash').sparkline([ 0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar',
            height: '50',
            barWidth: '2',
            resize: true,
            barSpacing: '5',
            barColor: '#55ce63'
        });
         $('#sparklinedash2').sparkline([ 0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar',
            height: '50',
            barWidth: '2',
            resize: true,
            barSpacing: '5',
            barColor: '#7460ee'
        });
          $('#sparklinedash3').sparkline([ 0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar',
            height: '50',
            barWidth: '2',
            resize: true,
            barSpacing: '5',
            barColor: '#03a9f3'
        });
           $('#sparklinedash4').sparkline([ 0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar',
            height: '50',
            barWidth: '2',
            resize: true,
            barSpacing: '5',
            barColor: '#f62d51'
        });
        
   
       }
        var sparkResize;

            $(window).resize(function(e) {
                clearTimeout(sparkResize);
                sparkResize = setTimeout(sparklineLogin, 500);
            });
            sparklineLogin();
});
// ============================================================== 
// Gauge chart option
// ============================================================== 
var gaugeChart = echarts.init(document.getElementById('gauge-chart'));
option = {
    tooltip: {
        formatter: "{a} <br/>{b} : {c}%"
    }
    , toolbox: {
        show: false
        , feature: {
            mark: {
                show: true
            }
            , restore: {
                show: true
            }
            , saveAsImage: {
                show: true
            }
        }
    }
    , series: [
        {
            name: ''
            , type: 'gauge'
            , splitNumber: 0, // 分割段数，默认为5
            axisLine: { // 坐标轴线
                lineStyle: { // 属性lineStyle控制线条样式
                    color: [[0.2, '#785ff3'], [0.8, '#8c76f9'], [1, '#9e8bfe']]
                    , width: 20
                }
            }
            , axisTick: { // 坐标轴小标记
                splitNumber: 0, // 每份split细分多少段
                length: 12, // 属性length控制线长
                lineStyle: { // 属性lineStyle控制线条样式
                    color: 'auto'
                }
            }
            , axisLabel: { // 坐标轴文本标签，详见axis.axisLabel
                textStyle: { // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    color: 'auto'
                }
            }
            , splitLine: { // 分隔线
                show: false, // 默认显示，属性show控制显示与否
                length: 50, // 属性length控制线长
                lineStyle: { // 属性lineStyle（详见lineStyle）控制线条样式
                    color: 'auto'
                }
            }
            , pointer: {
                width: 5
                , color: '#54667a'
            }
            , title: {
                show: false
                , offsetCenter: [0, '-40%'], // x, y，单位px
                textStyle: { // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder'
                }
            }
            , detail: {
                textStyle: { // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    color: 'auto'
                    , fontSize: '14'
                    , fontWeight: 'bolder'
                }
            }
            , data: [{
                value: 50
                , name: ''
            }]
        }
    ]
};
timeTicket = setInterval(function () {
        option.series[0].data[0].value = (Math.random() * 100).toFixed(2) - 0;
        gaugeChart.setOption(option, true);
    }, 2000)
    // use configuration item and data specified to show chart
gaugeChart.setOption(option, true), $(function () {
    function resize() {
        setTimeout(function () {
            gaugeChart.resize()
        }, 100)
    }
    $(window).on("resize", resize), $(".sidebartoggler").on("click", resize)
});